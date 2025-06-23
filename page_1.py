import streamlit as st  # Streamlit Software
from change_page import change_page  # Application Function
from log_in_page_create_user_page import validate_user, new_user  # Database Function
from initialise_variables import question_passcode, question_username, question_age, question_focus_area, \
    question_time_available, min_time_limit, question_suggestions, max_recommendation_limit, min_limit, max_limit, \
    focus_areas, ages, genders, question_gender
from generate_items import generate_unique_passcode, generate_animal_username  # Application Function
from check_and_balance import record_question, get_status  # Database Function
from mongo_connection import Recommendation  # Database Function

if 'page' not in st.session_state:
    st.session_state.page = 1  # Will set the layout the application will open

if 'current_passcode' not in st.session_state:
    st.session_state.current_passcode = 1  # Will register the user operating the application

if 'error' not in st.session_state:
    st.session_state.error = ''  # Will store error logs for functions called

if 'error_status' not in st.session_state:
    st.session_state.error_status = None  # Will indicate whether there is an error to show

from streamlit_cookies_controller import CookieController  # Needs to be downloaded

controller = CookieController()
cookies = controller.getAll()


def set_username(passcode_for_setting_username):  # Called when user signs in or makes a new account

    st.session_state.current_passcode = passcode_for_setting_username  # Will register the user as the current user for this session

    today_for_setting_username, yesterday_for_setting_username, index_for_setting_username = get_status(
        st.session_state.current_passcode)  # Will see when the user made a last status

    if index_for_setting_username == -1:

        change_page(2)  # If the user hasn't made a status at all they need to make one

    elif today_for_setting_username:

        change_page(3)  # If the user hast made a status they go to the home page

    else:

        change_page(2)  # If the user hasn't made a status today the need to make one


def log_in_user(passcode_for_signing_in_user, question_passcode_for_log_in_user):  # Called when user tries to long in

    st.session_state.error_status, st.session_state.error = validate_user(
        passcode_for_signing_in_user)  # Will update the session error variables

    if st.session_state.error_status:  # Warning: The status variable is in reverse

        controller.set("previous_user_passcode",
                       str(passcode_for_signing_in_user))  # Will remember the passcode for the future so the user won't have to enter it

        # We need record the answer the user gave to a question everytime the user enters something in a field or selects an answer out of a radio button
        record_question(question_passcode_for_log_in_user, passcode_for_signing_in_user, passcode_for_signing_in_user)

        set_username(
            passcode_for_signing_in_user)  # Will call the function to register the user as the current user and move on to the next page


def create_user(user_username, user_passcode, age, gender, focus_area, time_available, suggestions,
                            question_username,
                            question_age, question_focus_area, question_time_available, question_suggestions, question_gender,
                            question_passcode):  # Called when a user wants to make a new account

    st.session_state.error_status, st.session_state.error = new_user(user_username, user_passcode, age,
                                                                     focus_area,
                                                                     time_available,
                                                                     suggestions, gender)  # Will update the session error variables and maybe create new user if appropriate

    if st.session_state.error_status:  # Warning: The status variable is in reverse

        controller.set("previous_user_passcode",
                       str(user_passcode))  # Will remember the passcode for the future so the user won't have to enter it

        # We need record the answer the user gave to a question everytime the user enters something in a field or selects an answer out of a radio button
        record_question(question_gender, gender, user_passcode)
        record_question(question_username, user_username, user_passcode)
        record_question(question_passcode, user_passcode, user_passcode)
        record_question(question_age, age, user_passcode)
        record_question(question_focus_area, str(focus_area), user_passcode)
        record_question(question_time_available, time_available, user_passcode)
        record_question(question_suggestions, suggestions, user_passcode)

        set_username(
            user_passcode)  # Will call the function to register the user as the current user and move on to the next page


def layout():

    # The SideBar - User Signs In With Passcode

    st.sidebar.header('Already have an account? Sign in!')

    passcode = st.sidebar.text_input(question_passcode, key="passcode", value=cookies.get("previous_user_passcode", ""))  # Save the previous passcode on the session variable

    st.sidebar.button('Log in', use_container_width=True, on_click=log_in_user, args=[passcode, question_passcode],
                      key="sign_in_user")

    # The Title

    st.title('Wellcome to Stressless Living!')

    st.header(
        'If you have an account sign in on the left - find the :material/arrow_forward_ios: icon to find the sign in form.')

    st.write("New here? Please answer the following questions and we'll create your account.")

    with st.container(border=True):  # Add a square around the section to seperate

        # Step 1: User enters a username - randomly generated at first

        generated_username = cookies.get("previous_user_username", "")
        if generated_username == "":
            generated_username = str(generate_animal_username())
            

        user_username = st.text_input(question_username, key="user_username", value=generated_username)

        controller.set("previous_user_passcode", str(user_username))

        make_profile = st.checkbox("Make profile") 

        if Recommendation.count_documents({}) >= 1 and make_profile :  # The application won't sign on new users if there are no recommendations to be given
            
            # The Initial Questions Section

            # Step 2: Generate a password randomly with 10 digits

            user_passcode = generate_unique_passcode()

            # Step 3: User enters an Age category and focus area to personalise the experience

            age = st.selectbox(question_age, ages, index=0, placeholder="Select an age category...")

            gender = st.selectbox(question_gender, genders, index=3, placeholder="Select an age category...")

            focus_area = st.multiselect(question_focus_area, focus_areas)

            # Step 4: User enters their free time amount and the amount of suggestion they wish to see

            time_available = st.number_input(question_time_available, min_value=min_time_limit, max_value=max_limit)

            suggestions = st.number_input(question_suggestions, min_value=min_limit,
                                          max_value=max_recommendation_limit)  # Set maximum at the amount of suggestions available

            # Step 5: User clicks button to create an account

            st.button('Let us get started', use_container_width=True, on_click=create_user,
                      args=[user_username, user_passcode, age, gender, focus_area, time_available, suggestions,
                            question_username,
                            question_age, question_focus_area, question_time_available, question_suggestions, question_gender,
                            question_passcode], key="create_user")
