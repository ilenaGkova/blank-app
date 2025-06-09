import streamlit as st  # Streamlit Software
from initialise_variables import initialize_variables, min_limit, stress_max_limit, max_limit, \
    focus_areas, ages, question_about_recommendation_id, question_about_points, \
    question_about_title, question_about_description, question_about_link, \
    question_about_passcode, question_age, question_focus_area, Question_ID, question_input, \
    question_gender, genders, question_about_duration  # Application Function
from mongo_connection import Question_Questionnaire, Recommendation  # Database Function
from add_data_in_collection import add_recommendation, add_question_to_Questionnaire, add_tag  # Database Function
from check_and_balance import record_question  # Database Function
from change_page import change_page  # Application Function
from generate_items import generate_recommendation_id  # Database Function

if 'page' not in st.session_state:
    st.session_state.page = 1  # Will set the layout the application will open

if 'current_passcode' not in st.session_state:
    st.session_state.current_passcode = 1  # Will register the user operating the application

if 'open_recommendation' not in st.session_state:
    st.session_state.open_recommendation = -1  # Will select a recommendation to open in full

if 'error' not in st.session_state:
    st.session_state.error = ''  # Will store error logs for functions called

if 'error_status' not in st.session_state:
    st.session_state.error_status = None  # Will indicate whether there is an error to show


def generate_question_id():  # Called what an admin wants to add a question to the Daily Stress Questionnaire

    # Step 1: Get bigger ID in Questionnaire collection
    last_entry = Question_Questionnaire.find_one({}, sort=[("ID", -1)])

    if last_entry:

        generated_id = int(last_entry['ID']) + 1

    else:

        generated_id = 1

    # Step 2: Increase by 1 until the new id doesn't exist
    while Question_Questionnaire.find_one({"ID": generated_id}):
        generated_id += 1

    return generated_id


def add_recommendation_here(your_passcode_here, this_generated_id_here, points_here, title_here, description_here,
                            link_here, question_about_recommendation_id_here, question_about_points_here,
                            question_about_title_here, question_about_description_here,
                            question_about_link_here, duration, question_about_duration_here):  # Called when the user wants to make a new recommendation

    st.session_state.error_status, st.session_state.error = add_recommendation(this_generated_id_here,
                                                                               your_passcode_here, title_here,
                                                                               description_here, link_here,
                                                                               points_here, duration)  # Will update the session error variables and maybe add a recommendation if appropriate
    if st.session_state.error_status:  # Warning: The status variable is in reverse

        # We need record the answer the user gave to a question everytime the user enters something in a field or selects an answer out of a radio button
        record_question(question_about_duration_here, duration, your_passcode_here)
        record_question(question_about_recommendation_id_here, this_generated_id_here, your_passcode_here)
        record_question(question_about_points_here, points_here, your_passcode_here)
        record_question(question_about_title_here, title_here, your_passcode_here)
        record_question(question_about_description_here, description_here, your_passcode_here)
        record_question(question_about_link_here, link_here, your_passcode_here)

        change_page(st.session_state.page)  # Will change the page to itself to reload and see the result


def add_question(ID, passcode_for_question, question_input_here, question_for_question_input, question_for_id):
    st.session_state.error_status, st.session_state.error = add_question_to_Questionnaire(ID, passcode_for_question,
                                                                                          question_input_here)  # Will update the session error variables and maybe add a recommendation if appropriate

    if st.session_state.error_status:  # Warning: The status variable is in reverse

        # We need record the answer the user gave to a question everytime the user enters something in a field or selects an answer out of a radio button
        record_question(question_for_id, ID, passcode_for_question)
        record_question(question_for_question_input, question_input_here, passcode_for_question)

        change_page(st.session_state.page)  # Will change the page to itself to reload and see the result


def add_tag_here(recommendation_id_here, passcode_here, title_here, category,
                 question_about_recommendation_id_here):  # Called when the user wants to add a tag to a recommendation

    st.session_state.error_status, st.session_state.error = add_tag(recommendation_id_here, passcode_here, title_here,
                                                                    category)  # Will update the session error variables and maybe add a tag to a recommendation if appropriate

    if st.session_state.error_status:
        # We need record the answer the user gave to a question everytime the user enters something in a field or selects an answer out of a radio button
        record_question(question_about_recommendation_id_here, recommendation_id_here, passcode_here)
        record_question(title_here, category, passcode_here)

        change_page(st.session_state.page)  # Will change the page to itself to reload and see the result


def layout_9():
    user, today, yesterday, index, recommendation = initialize_variables(st.session_state.current_passcode,
                                                                         st.session_state.open_recommendation)

    if user is not None and index != -1 and user['Role'] != 'User':

        # The Title

        st.title('Add Entries to DataBase')

        add_a_recommendation_layout()

        add_tags_layout()

        add_a_question_layout()

    elif user is not None and index != -1:

        st.session_state.error_status = False
        st.session_state.error = 'You do not have access to this page'


def add_a_question_layout():
    # Section 3: Questions in Daily Stress Questionnaire
    # The Title
    st.header('Add a Question')
    with st.container(border=True):  # Seperate this section from the others

        column_for_question_ID, column_for_user_passcode = st.columns(
            [4, 4])  # Columns named after the content they show

        with column_for_question_ID:
            # This is auto field by finding and ID that is not in the Questionnaire collection and can't change
            # Warning: While this is a text input the text in converted into a number before being entered with the recommendation

            this_generated_id = st.text_input(Question_ID, key="question_id",
                                              value=generate_question_id(),
                                              disabled=True)  # This ID is generated on the spot

        with column_for_user_passcode:  # This is set as the current user's passcode, and it can't be changed

            your_passcode_for_question = st.text_input(question_about_passcode,
                                                       key="your_passcode_for_question",
                                                       value=st.session_state.current_passcode,
                                                       disabled=True)

        question = st.text_area(question_input, height=100,
                                key="question")  # Warning: Alike other input text filed this type need control+enter to save the new information

        st.button('Add Question To Daily Stress Questionnaire', icon=":material/question_mark:",
                  use_container_width=True,
                  on_click=add_question,
                  args=[this_generated_id, your_passcode_for_question, question, question_input, Question_ID],
                  key="add_question_entry_button")


def add_tags_layout():
    # Section 2: Add a Tag
    # Tags are restrictive attributes that limit what kind of users will see this recommendation
    # Tags can be placed on time_available, stress_level, focus_area and age of a user
    # Warning: Too many tags means the recommendation may never be appropriate
    if Recommendation.count_documents({}) >= 1:

        # The Title

        st.header('Add a tag')

        # The Tag Start Information

        # This is vital information for any Tag, the passcode of the user adding it and the recommendation to goes to

        column_for_tag_passcode, column_for_id_tag = st.columns(
            [3, 3])  # Columns named after the content they show

        with column_for_tag_passcode:  # This is set as the current user's passcode, and it can't be changed

            your_passcode_for_tag = st.text_input(question_about_passcode, key="your_passcode_for_tag",
                                                  value=st.session_state.current_passcode, disabled=True)

        with column_for_id_tag:  # This is the ID of the recommendation we want to add the Tag to

            id_for_tag = st.number_input(question_about_recommendation_id, min_value=1)

        # There are 4 kinds of tags placed: Stress Level, Time Available, Age Category and Focus Area

        # SubSection A: Stress Level Tag

        with st.container(border=True):  # Seperate from sections below by putting this in a square

            column_for_stress_level_tag_title, column_for_stress_level_tag_value, column_for_stress_level_tag_done = st.columns(
                [2, 4, 0.5])  # Columns named after the content they show

            with column_for_stress_level_tag_title:  # Write the kind of tag the user is entering

                st.write("Add a Stress Level Tag")

            with column_for_stress_level_tag_value:  # User selects the Tag Value

                stress_level = st.number_input("Stress Level", min_value=min_limit,
                                               max_value=stress_max_limit)  # Limits match the limits of the answer in the Daily Stress Questioner

            with column_for_stress_level_tag_done:
                if Recommendation.find_one(
                        {"ID": id_for_tag}):  # User can only enter Tag to existing recommendation

                    st.button('', icon=":material/check:", use_container_width=True,
                              on_click=add_tag_here,
                              args=[id_for_tag, your_passcode_for_tag, "Stress Level", stress_level,
                                    question_about_recommendation_id],
                              key="add_stress_level_tag_button")  # This function is local to record the questions and add the Tag

        # Subsection B: Time Available Tag

        with st.container(border=True):  # Seperate from sections below by putting this in a square

            column_for_time_available_tag_title, column_for_time_available_tag_value, column_for_time_available_tag_done = st.columns(
                [2, 4, 0.5])  # Columns named after the content they show

            with column_for_time_available_tag_title:  # Write the kind of tag the user is entering

                st.write("Add a Time Available Tag")

            with column_for_time_available_tag_value:  # User selects the Tag Value

                time_available = st.number_input("Time Available", min_value=min_limit,
                                                 max_value=max_limit)  # Limits match the user's margin for answer

            with column_for_time_available_tag_done:
                if Recommendation.find_one(
                        {"ID": id_for_tag}):  # User can only enter Tag to existing recommendation

                    st.button('', icon=":material/check:", use_container_width=True,
                              on_click=add_tag_here,
                              args=[id_for_tag, your_passcode_for_tag, "Time Available", time_available,
                                    question_about_recommendation_id],
                              key="add_time_available_tag_button")  # This function is local to record the questions and add the Tag

        # Subsection C: Focus Area

        with st.container(border=True):  # Seperate from sections below by putting this in a square

            column_for_focus_area_tag_title, column_for_focus_area_tag_value, column_for_focus_area_tag_done = st.columns(
                [2, 4, 0.5])  # Columns named after the content they show

            with column_for_focus_area_tag_title:  # Write the kind of tag the user is entering

                st.write("Add a Focus Area Tag")

            with column_for_focus_area_tag_value:  # User selects the Tag Value

                focus_area = st.selectbox(question_focus_area, focus_areas, index=0,
                                          placeholder="Select a focus area...")  # Options match the ones given to user

            with column_for_focus_area_tag_done:
                if Recommendation.find_one(
                        {"ID": id_for_tag}):  # User can only enter Tag to existing recommendation

                    st.button('', icon=":material/check:", use_container_width=True,
                              on_click=add_tag_here,
                              args=[id_for_tag, your_passcode_for_tag, "Focus Area", focus_area,
                                    question_about_recommendation_id],
                              key="add_focus_area_tag_button")  # This function is local to record the questions and add the Tag

        # Subsection D: Age Variant

        with st.container(border=True):  # Seperate from sections below by putting this in a square

            column_for_age_tag_title, column_for_age_tag_value, column_for_age_tag_done = st.columns(
                [2, 4, 0.5])  # Columns named after the content they show

            with column_for_age_tag_title:  # Write the kind of tag the user is entering

                st.write("Add a Age Variant Tag")

            with column_for_age_tag_value:  # User selects the Tag Value

                age_variant = st.selectbox(question_age, ages, index=0,
                                           placeholder="Select an age category...")  # Options match the ones given to user

            with column_for_age_tag_done:
                if Recommendation.find_one(
                        {"ID": id_for_tag}):  # User can only enter Tag to existing recommendation

                    st.button('', icon=":material/check:", use_container_width=True,
                              on_click=add_tag_here,
                              args=[id_for_tag, your_passcode_for_tag, "Age Variant", age_variant,
                                    question_about_recommendation_id],
                              key="add_age_variant_tag_button")  # This function is local to record the questions and add the Tag

        # Subsection E: Show for Levels Above or Below

        with st.container(border=True):  # Seperate from sections below by putting this in a square

            column_for_level_tag_title, column_for_level_tag_value, column_for_level_tag_done = st.columns(
                [2.1, 4, 0.5])  # Columns named after the content they show

            with column_for_level_tag_title:  # Write the kind of tag the user is entering

                level_variant = st.selectbox("Tag Name", (
                    "Show for levels above", "Show for levels below", "Show for levels equal"), index=0,
                                             placeholder="Select a Tag...")

            with column_for_level_tag_value:  # User selects the Tag Value

                level_level = st.number_input("Level", min_value=min_limit)

            with column_for_level_tag_done:
                if Recommendation.find_one(
                        {"ID": id_for_tag}):  # User can only enter Tag to existing recommendation

                    st.button('', icon=":material/check:", use_container_width=True,
                              on_click=add_tag_here,
                              args=[id_for_tag, your_passcode_for_tag, level_variant, level_level,
                                    question_about_recommendation_id],
                              key="add_level_tag_button")  # This function is local to record the questions and add the Tag

        # Subsection F: Show for Levels Above or Below

        with st.container(border=True):  # Seperate from sections below by putting this in a square

            column_for_gender_tag_title, column_for_gender_tag_value, column_for_gender_tag_done = st.columns(
                [2.1, 4, 0.5])  # Columns named after the content they show

            with column_for_gender_tag_title:  # Write the kind of tag the user is entering

                st.write("Add a Age Variant Tag")

            with column_for_gender_tag_value:  # User selects the Tag Value

                gender = st.selectbox(question_gender, genders, index=0,
                                      placeholder="Select a focus area...")  # Options match the ones given to user

            with column_for_gender_tag_done:
                if Recommendation.find_one({"ID": id_for_tag}):  # User can only enter Tag to existing recommendation

                    st.button('', icon=":material/check:", use_container_width=True,
                              on_click=add_tag_here,
                              args=[id_for_tag, your_passcode_for_tag, "Gender", gender,
                                    question_about_recommendation_id],
                              key="add_gender_tag_button")  # This function is local to record the questions and add the Tag
    else:

        # You can't add tags to a recommendation-less database

        st.session_state.error_status = False
        st.session_state.error = 'There are no recommendations in the data base'


def add_a_recommendation_layout():
    # Section 1: Add a Recommendation
    # The Title
    st.header('Add a recommendation')

    # Step 2: Write the recommendation
    with st.container(border=True):  # Seperate from sections below by putting this in a square

        # Part 1: General Information

        column_for_new_recommendation_ID, column_for_new_recommendation_passcode, column_for_point_for_new_recommendation = st.columns(
            [2, 2, 2])  # Columns are named after the Recommendation information they show

        with column_for_new_recommendation_passcode:  # This is auto field by the current user's passcode and can't change

            your_passcode_for_recommendation = st.text_input(question_about_passcode,
                                                             key="your_passcode_for_recommendation",
                                                             value=st.session_state.current_passcode,
                                                             disabled=True)

        with column_for_new_recommendation_ID:
            # This is auto field by finding and ID that is not in the recommendation collection and can't change
            # Warning: While this is a text input the text in converted into a number before being entered with the recommendation

            this_generated_id = st.text_input(question_about_recommendation_id, key="recommendation_id",
                                              value=generate_recommendation_id(),
                                              disabled=True)  # This ID is generated on the spot

        # Part 2a: The recommendation

        title = st.text_input(question_about_title, key="title")  # Recommendation title

        description = st.text_area(question_about_description, height=300,
                                   key="description")  # Warning: Alike other input text filed this type need control+enter to save the new information

        # Part 3: The Recommendation Link

        column_for_duration, column_for_url_link, column_for_url_link_disclaimer = st.columns(
            [2, 4, 3])  # Columns are named after the Recommendation information they show

        with column_for_duration:
            duration = st.number_input(question_about_duration, min_value=5, max_value=max_limit)

        with column_for_url_link:
            link_input = st.text_input(question_about_link,
                                       key="link")  # This is a link the user will be able to go and see more information

        with column_for_url_link_disclaimer:
            link_condition = st.checkbox(
                "Include link - User takes full responsibility that the link has been verified and is secure")  # This disclaimer makes the user think to check the link before entering it

        link = None

        if link_condition:  # You only get the link included if you have checked the checkbox

            link = link_input

        # Part 2b: The recommendation

        with column_for_point_for_new_recommendation:
            # The minimum points a recommendation can get is 10 points
            # The maximum points is 150 which is the cap points for a user in level 1

            points = st.number_input(question_about_points, min_value=duration*2, max_value=150)  # duration needed to exist before the value was registered so this is set up here

        # Step 3: Add the recommendation
        # To add the recommendation the user needs to click this button
        # The function it calls is a local one that will add the recommendation and record the questions

        st.button('Add Recommendation', icon=":material/fact_check:", use_container_width=True,
                  on_click=add_recommendation_here,
                  args=[your_passcode_for_recommendation, this_generated_id, points, title, description, link,
                        question_about_recommendation_id, question_about_points, question_about_title,
                        question_about_description, question_about_link, duration, question_about_description],
                  key="add_recommendation_entry_button")
