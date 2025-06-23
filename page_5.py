import streamlit as st  # Streamlit Software
from initialise_variables import initialize_variables  # Application Function
from change_page import open_recommendation  # Database Function
from make_record import create_history, delete_entry  # Database Function

if 'current_passcode' not in st.session_state:
    st.session_state.current_passcode = 1  # Will register the user operating the application

if 'error' not in st.session_state:
    st.session_state.error = ''  # Will store error logs for functions called

if 'error_status' not in st.session_state:
    st.session_state.error_status = None  # Will indicate whether there is an error to show

if 'open_recommendation' not in st.session_state:
    st.session_state.open_recommendation = -1  # Will select a recommendation to open in full


def layout_5():
    user, today, yesterday, index, recommendation = initialize_variables(st.session_state.current_passcode,
                                                                         st.session_state.open_recommendation)

    if user is not None and index != -1:

        # The Title

        st.title('Your Record')

        # Step 1: Select categories

        st.header('Step 1: Select the Categories - Mandatory')  # Explain what the user needs to do

        with st.container(border=True):

            # Each column is named after the category it shows
            # Each category is a collection in the mongo server.
            # Each column is named after the category it shows
            # Each column will have a checkbox. Checkboxes return either True or False

            column_for_user_category, column_for_question_category, column_for_record_category = st.columns(
                [2, 2, 2])
            column_for_status_category, column_for_recommendation_category, column_for_tag_category = st.columns(
                [2, 2, 2])
            column_for_favorite_category, column_for_removed_category, column_for_per_person_category = st.columns(
                [2, 2, 2])
            column_for_Questionnaire, column_for_score, column_for_uniformity_in_outline = st.columns([2, 2, 2])

            with column_for_user_category:

                user_status = st.checkbox("See when your profile was generated")  # Include User Collection

            with column_for_question_category:

                question_status = st.checkbox("See what questions you have answered")  # Include Question Collection

            with column_for_record_category:

                record_status = st.checkbox(
                    "See what actions the application has done on your behalf")  # Include Record Collection

            with column_for_status_category:

                status_status = st.checkbox(
                    "See when you answered the Stress Daily Stress Questionnaire")  # Include Status Collection

            with column_for_recommendation_category:

                recommendation_status = False

                if user['Role'] != 'User':
                    recommendation_status = st.checkbox(
                        "See what tasks you have entered")  # Include Recommendation Collection

            with column_for_tag_category:

                tag_status = False

                if user['Role'] != 'User':
                    tag_status = st.checkbox("See what Tags you have added to Tasks")  # Include Tag Collection

            with column_for_favorite_category:

                favorite_status = st.checkbox("See your favorite tasks")  # Include Favorite Collection

            with column_for_removed_category:

                removed_status = st.checkbox(
                    "See what tasks you rejected")  # Include Removed_Recommendation Collection

            with column_for_per_person_category:

                person_status = st.checkbox(
                    "See what tasks have been given to you")  # Include Recommendation_Per_Person Collection

            with column_for_Questionnaire:

                if user['Role'] != 'User':
                    Questionnaire_status = st.checkbox(
                        "See what questions have entered in the Daily Stress Questionnaire")  # Include Questionnaire Collection

            with column_for_score:

                score_status = st.checkbox(
                    "See your score history")  # Include Score_History Collection

        # Step 2: Selecting a Shorting Method

        st.header('Step 2: Pick a sorting method - optional')  # Explain what the user needs to do

        column_for_priority_for_user_record, column_for_order_for_user_record = st.columns(
            [3, 3])  # Each column is named after the content they show.

        with column_for_priority_for_user_record:  # This will choose whether the results will be sorted by time created or the text of the record entries

            with st.container(border=True):
                priority = st.radio(
                    "Sort By",
                    ("Time", "Substance"),
                    index=None
                )  # Unlike other radio buttons this won't have a preselected answer

        with column_for_order_for_user_record:

            with st.container(border=True):
                order_question = st.radio(
                    "Show from",
                    ("A to Z", "Z to A"),
                    index=None
                )  # Unlike other radio buttons this won't have a preselected answer

                order = -1

                if order_question == "A to Z":
                    order = 1

        # User can enter any user passcode to search if given the Admin role

        user_passcode_search = st.text_input("Search for user", key="user_username_for_search",
                                             value=st.session_state.current_passcode,
                                             disabled=(user['Role'] == 'User'))

        st.header('See your record')  # See the result

        if user_status or question_status or record_status or status_status or recommendation_status or tag_status or favorite_status or removed_status or person_status or Questionnaire_status or score_status:

            # Send the user's choices and make the record
            # The function takes a boolean value for each collection, a priority value (Time/Substance) and order (1/-1)

            user_history_list_built, user_history_list, user_history_list_message = create_history(
                user_passcode_search, priority, order,
                user_status, question_status,
                record_status,
                status_status, recommendation_status,
                tag_status,
                favorite_status, removed_status,
                person_status,
                Questionnaire_status, score_status,
                st.session_state.current_passcode)

            st.write(user_history_list_message)  # Show the message given by the function

            user_history_list_pointer = 1  # The pointer will be a unique identifier for the buttons generated and for the user

            if user_history_list_built:  # Write the result of the function above, see mongo file for more

                if len(user_history_list) == 1:  # Show the number of results with the appropriate message

                    st.write('You have ', len(user_history_list), ' result')

                else:

                    st.write('You have ', len(user_history_list), ' results')

                for entry in user_history_list:

                    with st.container(border=True):  # Puts a border around each entry to seperate

                        if user['Role'] == 'User':  # This page has dual usage for and user or an admin. As a result we have 2 different tables

                            column_for_pointer_for_user_history_list_user_menu, column_for_timestamp_for_user_history_list_user_menu, column_for_message_for_user_history_list_user_menu, column_for_buttons_for_user_history_list_user_menu = st.columns(
                                [2, 2, 4, 1])  # Columns are named after the content they show

                            with column_for_pointer_for_user_history_list_user_menu:

                                st.write(user_history_list_pointer)  # Show pointer to seperate entries

                            with column_for_timestamp_for_user_history_list_user_menu:

                                st.write(entry[
                                             'Created_At'])  # Warning : For different collection this is when the entry to the collection was added, not created

                            with column_for_message_for_user_history_list_user_menu:

                                st.write(entry['Message'])  # Each Collection gets a different message

                            with column_for_buttons_for_user_history_list_user_menu:

                                # Each entry comes with 1 or 2 secret keys that combined with the collection name will find the entry
                                # For a recommendation related collection either have Key 1 or 2 as the ID of the recommendation which we can use to open the recommendation in full
                                # We see if it's one of the appropriate collections and send the right key to the open recommendation

                                if entry['Type'] == "Recommendation" or entry['Type'] == "Tag" or entry['Type'] == "Favorite_Recommendation" or entry['Type'] == "Removed_Recommendation":

                                    st.button("", icon=":material/open_in_full:", use_container_width=True,
                                              on_click=open_recommendation, args=[entry['Key']],
                                              key=f"open_recommendation_user_history_list_{user_history_list_pointer}_user")

                                elif entry['Type'] == "Recommendation_Per_Person":

                                    st.button("", icon=":material/open_in_full:", use_container_width=True,
                                              on_click=open_recommendation, args=[entry['Key2']],
                                              key=f"open_recommendation_user_history_list_{user_history_list_pointer}_user")

                        else:

                            column_for_pointer_for_user_history_list_admin_menu, column_for_timestamp_for_user_history_list_admin_menu, column_for_type_for_user_history_list_admin_menu, column_for_message_for_admin_history_list_user_menu, column_for_buttons_for_user_history_list_admin_menu = st.columns(
                                [2, 2, 2, 4, 1])  # Columns are named after the content they show

                            with column_for_pointer_for_user_history_list_admin_menu:

                                st.write(user_history_list_pointer)  # Show pointer to seperate entries

                            with column_for_timestamp_for_user_history_list_admin_menu:

                                st.write(entry[
                                             'Created_At'])  # Warning : For different collection this is when the entry to the collection was added, not created

                            with column_for_type_for_user_history_list_admin_menu:  # This is admin specific information

                                st.write(entry['Type'])  # Will show the collection the entry is from

                            with column_for_message_for_admin_history_list_user_menu:

                                st.write(entry['Message'])  # Each Collection gets a different message

                            with column_for_buttons_for_user_history_list_admin_menu:

                                # Each entry comes with 1 or 2 secret keys that combined with the collection name will find the entry
                                # For a recommendation related collection either have Key 1 or 2 as the ID of the recommendation which we can use to open the recommendation in full
                                # We see if it's one of the appropriate collections and send the right key to the open recommendation
                                # The Keys are used so the admin can delete peaces of the record, by sending the collection name and the keys to a delete function
                                # That function is explain in the mongo file

                                if entry['Type'] == "Recommendation" or entry['Type'] == "Tag" or entry['Type'] == "Favorite_Recommendation" or entry['Type'] == "Removed_Recommendation":

                                    st.button("", icon=":material/open_in_full:", use_container_width=True,
                                              on_click=open_recommendation, args=[entry['Key']],
                                              key=f"open_recommendation_user_history_list_{user_history_list_pointer}_admin")

                                elif entry['Type'] == "Recommendation_Per_Person":

                                    st.button("", icon=":material/open_in_full:", use_container_width=True,
                                              on_click=open_recommendation, args=[entry['Key2']],
                                              key=f"open_recommendation_from_user_history_list_{user_history_list_pointer}_admin")

                                st.button("", icon=":material/delete:", use_container_width=True,
                                          on_click=delete_entry,
                                          args=[entry['Passcode'], entry['Key'], entry['Key2'], entry['Created_At'],
                                                entry['Type'], st.session_state.current_passcode],
                                          key=f"delete_{user_history_list_pointer}")

                    user_history_list_pointer += 1

        else:

            st.write("You haven't selected a category")  # It won't create a record with no categories

    else:

        st.session_state.error_status = False

        if user is None and index == -1:
            st.session_state.error = 'Something went wrong, User not signed in and no Status found'
        elif user is None:
            st.session_state.error = 'Something went wrong, no Status found'
        else:
            st.session_state.error = 'Something went wrong, User not signed in'
