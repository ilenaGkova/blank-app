import streamlit as st  # Streamlit Software
from mongo_connection import Tag, User  # Database Function
from initialise_variables import initialize_variables  # Application Function

if "page" not in st.session_state:
    st.session_state.page = 1  # Will set the layout the application will open

if "current_passcode" not in st.session_state:
    st.session_state.current_passcode = 1  # Will register the user operating the application

if 'error' not in st.session_state:
    st.session_state.error = ''  # Will store error logs for functions called

if 'error_status' not in st.session_state:
    st.session_state.error_status = None  # Will indicate whether there is an error to show

if "open_recommendation" not in st.session_state:
    st.session_state.open_recommendation = -1  # Will select a recommendation to open in full


def layout():

    user, today, yesterday, index, recommendation = initialize_variables(st.session_state.current_passcode,
                                                                         st.session_state.open_recommendation)

    if recommendation is not None and user is not None and index != -1:

        # The Title

        with st.container(border=True):

            st.markdown(
                f"<div style='text-align: center;font-size: 40px;font-weight: bold;'>{recommendation['Title']}</div>",
                unsafe_allow_html=True)

        st.write("")  # Add a blank line for space
        st.write("")  # Add a blank line for space
        st.write("")  # Add a blank line for space
        st.write("")  # Add a blank line for space

        # Section 2: The Recommendation

        # Here we will show the description of the recommendation and the tags related
        # Tags are restrictive attributes that limit what kind of users will see this recommendation
        # Tags can be placed on time_available, stress_level, focus_area and age of a user
        # Too many tags means the recommendation may never be appropriate

        if Tag.count_documents(
                {"ID": recommendation['ID']}) == 0:  # If there are 0 tags we can just show the description

            with st.container(border=True):  # Add a square around the information

                st.write(recommendation['Description'])  # Show the description

                if recommendation['Link'] is not None:
                    st.write('See more information on ', recommendation['Link'])  # Show a link if one exists

        else:

            column_for_description_of_recommendation, column_for_tags_of_recommendation = st.columns(
                [5, 2])  # Seperate the line into 2 columns and name them after the content they hold

            with column_for_description_of_recommendation:

                with st.container(border=True):  # Add a square around the information

                    st.write(recommendation['Description'])

                    if recommendation['Link'] is not None:
                        st.write('See more information on ', recommendation['Link'])  # Show a link if one exists

                with column_for_tags_of_recommendation:

                    # Here we will show all tags related since they exist now
                    # We will include the category they are in and their value and well as the username of the person who added them

                    st.write("Tags related to this recommendation:")

                    tags = list(Tag.find({"ID": recommendation['ID']}))  # Get list of tags related

                    for entry_in_tags in tags:
                        # Warning: The creator is stored by passcode, but the passcode is how users sign in the application
                        # Showing it here would give everyone the ability to take on the admins identity

                        st.write(entry_in_tags['Title_Of_Criteria'], ': ', entry_in_tags['Category'],
                                 'as assigned by, ',
                                 User.find_one({"Passcode": entry_in_tags['Passcode']})[
                                     'Username'])  # To avoid data leakage we will show the creator by username

    elif user is not None and index != -1:

        st.session_state.error_status = False
        st.session_state.error = f"Something went wrong, Recommendation with ID number {st.session_state.open_recommendation} not found."
