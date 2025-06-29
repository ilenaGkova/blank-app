import streamlit as st  # Streamlit Software
from initialise_variables import initialize_variables, options  # Application Function
from check_and_balance import record_question, record_status  # Database Function
from change_page import change_page  # Application Function
from mongo_connection import Question_Questionnaire  # Database Function
# Application Function

if 'page' not in st.session_state:
    st.session_state.page = 1  # Will set the layout the application will open

if 'current_passcode' not in st.session_state:
    st.session_state.current_passcode = 1  # Will register the user operating the application

if 'error' not in st.session_state:
    st.session_state.error = ''  # Will store error logs for functions called

if 'error_status' not in st.session_state:
    st.session_state.error_status = None  # Will indicate whether there is an error to show

if 'answers' not in st.session_state:
    st.session_state.answers = {}  # Will store answers to the Daily Stress Questioner


def submit_questionnaire():  # Called when the user completes the questioner
    # Create a list of question-answer pairs
    question_answer_pairs = [(question, answer) for question, answer in st.session_state.answers.items()]

    stress_level = 0  # Set Stress Level as 0, so we can add to it

    for question, answer in question_answer_pairs:
        stress_level += catalog_question(question, answer,
                                         st.session_state.current_passcode)  # Record the question-answer pairs and increase the stress level

    make_status(int(stress_level/len(question_answer_pairs)))  # Submit to final stress level to move on


def catalog_question(question, answer, passcode):  # Called for each question in the Daily Stress Questionnaire

    record_question(question, answer, passcode)  # We need record the answer the user gave to a question everytime the user enters something in a field or selects an answer out of a radio button

    return options.get(answer)  # Depending on the answer the stress level will rise by 0 through 4


def make_status(
        user_stress_level):  # Called when the user makes a status by answering questions about their stress level

    st.session_state.error_status, st.session_state.error = record_status(st.session_state.current_passcode,
                                                                          user_stress_level)  # Will update the session error variables and maybe create new status for user if appropriate

    if st.session_state.error_status:  # Warning: The status variable is in reverse

        change_page(3)  # Will can function to move to Home page


def layout_2():

    user, today, yesterday, index, recommendation = initialize_variables(st.session_state.current_passcode,
                                                                         1)

    if user is not None:

        # The SideBar - User Information

        # Show the user information and preferences

        st.sidebar.write("Questions generated after studying the symptoms of stress")
        st.sidebar.write("Citation provided:")
        st.sidebar.write("C. Acred, Anxiety and stress. Cambridge: Independence Educational Publishers, 2015.")

        if today:  # Sometimes users do multable statuses a day, if one has been done the user doesn't need to make another unless they want to

            st.sidebar.button('Skip', on_click=change_page, args=[3], use_container_width=True, key="skip")

        # The Title

        st.title(f"Hello {user['Username']}")
        """Please answer the Daily Stress Questioner"""

        # The Daily Question Section

        questionnaire_list = Question_Questionnaire.find()  # Get the questioner questions

        for entry in questionnaire_list:
            key = f"Question_{entry['ID']}"  # Make a unique key for each input field.

            # For each question we will have a slider for the user to answer
            st.select_slider(entry['Question'], list(options.keys()), key=key)

            st.session_state.answers[entry['Question']] = st.session_state[key]  # Store the answer to the question via the key

        st.button("Submit", on_click=submit_questionnaire, args=[], use_container_width=True, key="make_status")  # Step 2: Click button to submit answers

    else:

        # Page won't open unless user is registered

        st.session_state.error_status = False
        st.session_state.error_status = "Something went wrong, user not registered."
