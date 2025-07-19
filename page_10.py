import streamlit as st  # Streamlit Software
from initialise_variables import initialize_variables  # Application Function
from mongo_connection import Recommendation  # Database Function
from evaluation import add_samples, update_sample, delete_samples  # Application Function

if 'page' not in st.session_state:
    st.session_state.page = 1  # Will set the layout the application will open

if 'current_passcode' not in st.session_state:
    st.session_state.current_passcode = 1  # Will register the user operating the application

if 'error' not in st.session_state:
    st.session_state.error = ''  # Will store error logs for functions called

if 'error_status' not in st.session_state:
    st.session_state.error_status = None  # Will indicate whether there is an error to show


def layout_10():
    user, today, yesterday, index, recommendation = initialize_variables(st.session_state.current_passcode,
                                                                         1)

    if user is not None and index != -1 and user['Role'] != 'User':

        st.title("Wellcome to the evaluation page!")

        see_samples()

        update_samples()

        generate_matching_samples()

    elif user is not None and index != -1:

        st.session_state.error_status = False

        if user is None and index == -1 and user['Role'] == 'User':
            st.session_state.error = 'Something went wrong, User not signed in and no Status found'
        elif user is None:
            st.session_state.error = 'Something went wrong, no Status found'
        elif index == -1:
            st.session_state.error = 'Something went wrong, User not signed in'
        else:
            st.session_state.error = 'You do not have access to this page'


def see_samples():
    st.header("1. See your Gemini samples")

    with st.container(border=True):  # Seperate this section from the others

        number = int(Recommendation.count_documents(
            {'Passcode': "Gemini", 'Prompt': {'$exists': True}, 'Answer': {'$exists': True}}))

        st.write(f"You have {number} Gemini Samples")  # See how many samples you have

        if number < 100:  # See if the samples are enough
            st.write(f"You need {100 - number} more Gemini Samples to qualify for an evaluation")


def update_samples():
    st.header("2. Update the Gemini samples")

    with st.container(border=True):  # Separate this section visually

        list_of_samples = list(
            Recommendation.find({'Passcode': "Gemini", 'Prompt': {'$exists': True}, 'Answer': {'$exists': True},
                                 }))  # Count documents that have all three fields

        number = len(list_of_samples)

        # Use a set to find unique Pointer values
        unique_pointers = {entry['Pointer'] for entry in list_of_samples if 'Pointer' in entry}
        unique_count = len(unique_pointers)

        st.write(f"You now have {number} Gemini Samples with {unique_count} unique pointers.")

        if number != unique_count:
            st.button('Update Gemini Samples', use_container_width=True, on_click=update_sample, args=[],
                      key="update_gemini_samples")


def generate_matching_samples():
    st.header("3. See how many Groq samples you have")

    with st.container(border=True):  # Separate this section visually

        groq_samples = int(Recommendation.count_documents(
            {'Passcode': "Groq", 'Prompt': {'$exists': True}, 'Answer': {'$exists': True},
             'Pointer': {'$exists': True}}))

        gemini_samples = int(Recommendation.count_documents(
            {'Passcode': "Gemini", 'Prompt': {'$exists': True}, 'Answer': {'$exists': True},
             'Pointer': {'$exists': True}}))

        st.write(f"There are {groq_samples} Groq Samples for the {gemini_samples} Gemini Samples")

        if groq_samples < gemini_samples:
            st.button('Generate Groq Samples', use_container_width=True, on_click=add_samples, args=[],
                      key="add_groq_samples")

        st.button('Delete Groq Samples', use_container_width=True, on_click=delete_samples, args=[],
                  key="delete_groq_samples")
