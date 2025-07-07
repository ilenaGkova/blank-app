import streamlit as st  # Streamlit Software
from initialise_variables import initialize_variables, question_username, question_age, \
    question_focus_area, question_time_available, min_time_limit, max_limit, \
    question_suggestions, min_limit, max_recommendation_limit, ages, focus_areas, \
    question_gender, genders  # Application Function
from user_information import update_user, change_recommendation_preference_for_user  # Database Function
from check_and_balance import record_question  # Database Function
from change_page import change_page, open_recommendation  # Application Function
from make_record_recommendations import create_recommendation_history

if 'page' not in st.session_state:
    st.session_state.page = 1  # Will set the layout the application will open

if 'current_passcode' not in st.session_state:
    st.session_state.current_passcode = 1  # Will register the user operating the application

if 'error' not in st.session_state:
    st.session_state.error = ''  # Will store error logs for functions called

if 'error_status' not in st.session_state:
    st.session_state.error_status = None  # Will indicate whether there is an error to show


def update_user_here(update_username, update_passcode, update_age, update_gender, update_focus_area,
                     update_time_available, update_suggestions,
                     update_repeat, repeat_question):  # Called when the user wants to update their profile information

    st.session_state.error_status, st.session_state.error = update_user(update_passcode, update_username,
                                                                        update_repeat, update_age,
                                                                        update_focus_area,
                                                                        update_time_available,
                                                                        update_suggestions,
                                                                        update_gender)  # Will update the session error variables and maybe change user information if appropriate

    if st.session_state.error_status:  # Warning: The status variable is in reverse

        # We need record the answer the user gave to a question everytime the user enters something in a field or selects an answer out of a radio button
        record_question(question_gender, update_gender, update_passcode)
        record_question(question_username, update_username, update_passcode)
        record_question(question_age, update_age, update_passcode)
        record_question(question_focus_area, update_focus_area, update_passcode)
        record_question(question_time_available, update_time_available, update_passcode)
        record_question(question_suggestions, update_suggestions, update_passcode)
        record_question(repeat_question, update_repeat, update_passcode)

        change_page(st.session_state.page)  # Will change the page to itself to reload and see the result


def layout_4():
    user, today, yesterday, index, recommendation = initialize_variables(st.session_state.current_passcode,
                                                                         1)
    if user is not None and index != -1:

        # Section 1: The User Profile and Update Profile Function

        update_user_layout(user)

        # Section 2: User Preferences for Tasks

        make_record()
    else:

        st.session_state.error_status = False

        if user is None and index == -1:
            st.session_state.error = 'Something went wrong, User not signed in and no Status found'
        elif user is None:
            st.session_state.error = 'Something went wrong, no Status found'
        else:
            st.session_state.error = 'Something went wrong, User not signed in'


def make_record():
    # The Title
    st.title('Your Preferences')
    # Step 1: Select categories
    st.header('Step 1: Select the Categories - Mandatory')  # Explain what the user needs to do
    with st.container(border=True):

        # Each column is named after the category it shows
        # Each column will have a checkbox. Checkboxes return either True or False

        column_for_favorite_in_user_preferences, column_for_rejected_in_user_preferences, column_for_recommendations_given_in_user_preferences = st.columns(
            [2, 2, 2])

        with column_for_favorite_in_user_preferences:
            favorite_status_for_user_preferences = st.checkbox(
                "See your favorite tasks")  # Adds Favorite Collection

        with column_for_rejected_in_user_preferences:
            removed_status_for_user_preferences = st.checkbox(
                "See what tasks you rejected")  # Adds Removed_Recommendation Collection

        with column_for_recommendations_given_in_user_preferences:
            person_status_for_user_preferences = st.checkbox(
                "See what tasks have been given to you")  # Adds Recommendation_Per_Person Collection
    # Step 2: Select Sorting Method
    st.header('Step 2: Pick a sorting method - optional')  # Explain what the user needs to do
    # Columns are named after the content they show. Here it is a radio question.
    column_for_order_of_results_in_user_preferences, column_for_recommendation_status = st.columns([3, 3])
    with column_for_order_of_results_in_user_preferences:

        with st.container(border=True):
            order_question_for_user_preferences = st.radio(
                "Show from",
                ("A to Z", "Z to A"),
                index=None
            )  # Unlike other radio buttons this won't have a preselected answer

            order_for_user_preferences = -1

            if order_question_for_user_preferences == "A to Z":
                order_for_user_preferences = 1
    with column_for_recommendation_status:

        with st.container(border=True):

            recommendation_status_for_user_preferences = st.radio(
                "Include only",
                ("Completed Tasks", "Incomplete Tasks"),
                index=None
            )  # Unlike other radio buttons this won't have a preselected answer

            final_recommendation_status_for_user_preferences = None  # With no option selected all recommendations are shown

            if recommendation_status_for_user_preferences == "Completed Tasks":

                final_recommendation_status_for_user_preferences = False  # Mirrors how the recommendation_per_person stores recommendation outcomes

            elif recommendation_status_for_user_preferences == "Incomplete Tasks":

                final_recommendation_status_for_user_preferences = True  # Mirrors how the recommendation_per_person stores recommendation outcomes, default for incomplete recommendations is True
    # Step 3: Show Result
    st.header('See your record')
    if favorite_status_for_user_preferences or removed_status_for_user_preferences or person_status_for_user_preferences:

        # Built record if user has selected a category
        # The function will receive seperate boolean values and the additional preference to order (integer) and recommendation status (boolean)

        list_of_recommendations_based_on_filter_given_by_user_built, list_of_recommendations_based_on_filter_given_by_user, list_of_recommendations_based_on_filter_given_by_user_message = create_recommendation_history(
            st.session_state.current_passcode, order_for_user_preferences, favorite_status_for_user_preferences,
            removed_status_for_user_preferences,
            person_status_for_user_preferences, final_recommendation_status_for_user_preferences)

        st.write(
            list_of_recommendations_based_on_filter_given_by_user_message)  # Show the message given by the function

        list_of_recommendations_based_on_filter_given_by_user_pointer = 1  # The pointer will be a unique identifier for the buttons generated and for the user

        if list_of_recommendations_based_on_filter_given_by_user_built:  # Write the result of the function above, see mongo file for more

            if len(list_of_recommendations_based_on_filter_given_by_user) == 1:  # Show the number of results with the appropriate message

                st.write('You have ', len(list_of_recommendations_based_on_filter_given_by_user), ' result')

            else:

                st.write('You have ', len(list_of_recommendations_based_on_filter_given_by_user), ' results')

            for entry_for_list_of_recommendations_based_on_filter_given_by_user in list_of_recommendations_based_on_filter_given_by_user:

                with st.container(border=True):  # Puts a border around each entry to seperate

                    # Columns are named after the content they show

                    column_for_pointer_in_list_of_recommendations_based_on_filter_given_by_user, column_for_collection_and_status_in_list_of_recommendations_based_on_filter_given_by_user, column_for_timestamp_for_list_of_recommendations_based_on_filter_given_by_user, column_for_title_and_description_for_list_of_recommendations_based_on_filter_given_by_user, column_for_buttons_for_list_of_recommendations_based_on_filter_given_by_user = st.columns(
                        [1, 1, 1, 4, 1])

                    with st.container(border=True):  # Puts a border around each entry to seperate

                        with column_for_pointer_in_list_of_recommendations_based_on_filter_given_by_user:

                            st.write(
                                list_of_recommendations_based_on_filter_given_by_user_pointer)  # Show pointer to seperate entries

                        with column_for_collection_and_status_in_list_of_recommendations_based_on_filter_given_by_user:  # Shows the category each entry is

                            if entry_for_list_of_recommendations_based_on_filter_given_by_user[
                                'Type'] == "Favorite_Recommendation":

                                st.header(':material/thumb_up:')  # Category Favorites and Favorite Collection

                            elif entry_for_list_of_recommendations_based_on_filter_given_by_user[
                                'Type'] == "Removed_Recommendation":

                                st.header(
                                    ':material/thumb_down:')  # Category Removed and Removed_Recommendation Collection

                            if entry_for_list_of_recommendations_based_on_filter_given_by_user[
                                'Outcome'] is not None:  # The below are in the Recommendation_per_person Collection

                                st.header(
                                    ':material/badge:')  # Category given, mirrors how the recommendation_per_person stores recommendation outcomes, default for incomplete recommendations is True

                                if entry_for_list_of_recommendations_based_on_filter_given_by_user[
                                    'Outcome'] is False:
                                    st.header(
                                        ':material/done_outline:')  # Category given, complete recommendations

                        with column_for_timestamp_for_list_of_recommendations_based_on_filter_given_by_user:

                            st.write(entry_for_list_of_recommendations_based_on_filter_given_by_user[
                                         'Created_At'])  # Warning : for different collection this is when the recommendation was added, not created

                        with column_for_title_and_description_for_list_of_recommendations_based_on_filter_given_by_user:

                            st.markdown(
                                f"<div style='text-align: center; font-weight: bold;'>{entry_for_list_of_recommendations_based_on_filter_given_by_user['Title']}</div>",
                                unsafe_allow_html=True)

                            if len(entry_for_list_of_recommendations_based_on_filter_given_by_user[
                                       'Description']) > 150:  # If description is big enough it won't show. It can be shown by extending the recommendation to full screen

                                st.markdown(
                                    "<div style='text-align: center;'>Open Task to see description</div>",
                                    unsafe_allow_html=True)

                            else:

                                st.markdown(
                                    f"<div style='text-align: center;'>{entry_for_list_of_recommendations_based_on_filter_given_by_user['Description']}</div>",
                                    unsafe_allow_html=True)

                        with column_for_buttons_for_list_of_recommendations_based_on_filter_given_by_user:

                            # In case a recommendation has been deleted or not found it will still show but there are 2 additional attributes added to make sure they are not opened or deleted

                            if entry_for_list_of_recommendations_based_on_filter_given_by_user['Extend']:
                                st.button("", icon=":material/open_in_full:", use_container_width=True,
                                          on_click=open_recommendation, args=[
                                        entry_for_list_of_recommendations_based_on_filter_given_by_user['ID']],
                                          key=f"open_recommendation_for_list_of_recommendations_based_on_filter_given_by_user_{list_of_recommendations_based_on_filter_given_by_user_pointer}")

                            if entry_for_list_of_recommendations_based_on_filter_given_by_user['Remove']:
                                st.button("", icon=":material/delete:", use_container_width=True,
                                          on_click=change_recommendation_preference_for_user,
                                          args=[1, st.session_state.current_passcode,
                                                entry_for_list_of_recommendations_based_on_filter_given_by_user[
                                                    'ID'], True],
                                          key=f"remove_recommendation_for_list_of_recommendations_based_on_filter_given_by_user_{list_of_recommendations_based_on_filter_given_by_user_pointer}")

                list_of_recommendations_based_on_filter_given_by_user_pointer += 1

    else:

        st.write("You haven't selected a category")  # It won't create a record with no categories


def update_user_layout(user):
    # The Title
    st.title('Your Profile')
    # The Profile Information
    with st.container(border=True):

        # This section will show the user their information and change it by putting in their new information and click a button
        # The text labels are shared from page 1

        column_for_username, column_for_passcode = st.columns(
            [3, 3])  # Each column is named after the attribute if the user it shows

        column_for_age, column_for_gender, column_for_focus_area = st.columns(
            [2, 2, 2])  # Each column is named after the attribute if the user it shows

        column_for_time_available, column_for_number_of_suggestions, column_for_repeat = st.columns(
            [2, 2, 2])  # Each column is named after the attribute if the user it shows

        with column_for_username:
            update_username = st.text_input(question_username, key="update_username", value=user['Username'])

        with column_for_passcode:
            update_passcode = st.text_input("Your Passcode - Not available for Alteration",
                                            key="update_passcode", value=user['Passcode'], disabled=True)

        with column_for_age:
            update_age = st.selectbox(
                question_age,
                ages,
                index=ages.index(user['Age_Category']) if user['Age_Category'] in ages else 0,
                placeholder="Select an age category..."
            )

            if not user[
                       'Age_Category'] in ages:  # The value comes defaulted as the user's but if the options have changed, we write it down
                st.write('Current Age Category: ', user['Age_Category'])

        with column_for_gender:
            update_gender = st.selectbox(
                question_gender,
                genders,
                index=genders.index(user['Gender']) if user['Gender'] in genders else 4,
                placeholder="Select an age category..."
            )

            if not user['Gender'] in genders:
                st.write('Current Gender: ', user['Gender'])

        with column_for_focus_area:

            default_focus = [x for x in user['Focus_Area'] if x in focus_areas]

            update_focus_area = st.multiselect(
                question_focus_area,
                focus_areas,
                default=default_focus)

        with column_for_time_available:
            update_time_available = st.number_input(question_time_available, min_value=min_time_limit,
                                                    max_value=max_limit,
                                                    value=user[
                                                        'Time_Available'])  # Limits for each number input are shared from page 1

        with column_for_number_of_suggestions:
            update_suggestions = st.number_input(question_suggestions, min_value=min_limit,
                                                 max_value=max_recommendation_limit,
                                                 value=user[
                                                     'Suggestions'])  # Max limit is the number of suggestions found in the database

        with column_for_repeat:

            question = f"You will not see the same task in (choose below) days"
            update_repeat = st.number_input(
                question,
                min_value=min_limit, max_value=7,
                value=user['Repeat_Preference'])  # Limits for each number input are shared from page 1

        st.write("")  # Add a blank line for space

        st.write(
            "Warning: by clicking the button below will update every field of your profile, make sure you are altering only the fields you wish to alter")  # Add a disclaimer for the user

        st.button("Save Changes", icon=":material/save_as:", use_container_width=True,
                  on_click=update_user_here,
                  args=[update_username, update_passcode, update_age, update_gender, update_focus_area,
                        update_time_available, update_suggestions, update_repeat, question],
                  key="update_user_button")  # When user clicks here the information they have entered will update every field of theo user profile