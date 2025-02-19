import streamlit as st

# Configeration Command

st.set_page_config(
    page_title="StressTest",
    page_icon="👋",
)

# Part A: The Initial Session Variables

if "page" not in st.session_state:
    st.session_state.page = 1

if "current_passcode" not in st.session_state:
    st.session_state.current_passcode = 1

# Part B: The Imports

from datetime import datetime
from mongo_connection import generate_animal_username, generate_unique_passcode, get_status, init_connection, record_status, update_user_streak, validate_user, new_user, record_question

# Part C: The Functions

client = init_connection()
db = client.StressTest
Status = db["Status"]
User = db["User"]

user = User.find_one({"Passcode": st.session_state.current_passcode})

def set_username(passcode):
    st.session_state.current_passcode = passcode
    latest_status = Status.find_one({"Passcode": passcode}, sort=[("Created_At", -1)])
    if not latest_status: 
        st.session_state.page = 2
    else:
        last_status_time = datetime.strptime(latest_status['Created_At'], '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        if (now.date() == last_status_time.date()):
            st.session_state.page = 3
        else:
            st.session_state.page = 2

def log_in_user(passcode):
    move_on, message = validate_user(passcode)
    if not move_on:
        st.sidebar.write(message)
    else:
        record_question(question_passcode,passcode,passcode)
        set_username(passcode)
    

def create_user(user_username,user_passcode,age,focus_area,time_available,suggestions):
    move_on, message = new_user(user_username,user_passcode,age,focus_area,time_available,suggestions)
    if not move_on:
        st.sidebar.write(message)
    else:
        record_question(question_username,user_username,passcode)
        record_question(question_passcode,user_passcode,passcode)
        record_question(question_age,age,passcode)
        record_question(question_focus_area,focus_area,passcode)
        record_question(question_time_available,time_available,passcode)
        record_question(question_suggestions,suggestions,passcode)
        set_username(user_passcode)
    

def make_status(stress_level):
    if not user == None:
        move_on, message = record_status(st.session_state.current_passcode,stress_level)
        if not move_on:
            st.sidebar.write(message)
        else:
            record_question(question_stress_level,stress_level,st.session_state.current_passcode)
            st.session_state.page = 3
        

# Part D: The layouts

if st.session_state.page == 1:

    # The SideBar - User Signs In With Passcode
    st.sidebar.write ('Already have an account? Sign it!')
    question_passcode = "What's your passcode?"
    passcode = st.sidebar.text_input(question_passcode, key="passcode")
    log_in_button = st.sidebar.button('Log in', on_click=log_in_user, args=[passcode])

    # The Title
    """
    # Wellcome to Stress Test!
    Please answer the following questions and we'll create your account
    """

    # The Initial Questions Section
    question_username = "What's your username?"
    question_age = "Age"
    question_focus_area = "Where would you like to focus?"
    question_time_available = "How much time are you willing to spend in reducing stress?"
    question_suggestions = "How many suggestions do you want?"
    min_limit = 1
    max_limit = 10
    user_username = st.text_input(question_username, key="user_username", value=generate_animal_username())
    user_passcode = st.text_input(question_passcode, key="user_password", value=generate_unique_passcode(), disabled=True)
    age = st.radio(question_age,("18-25", "26-35", "36-55", "56-70", "70+"))
    focus_area = st.radio(question_focus_area,("Work/Career", "Finances", "Health & Well-being", "Relationships", "Time Management", "Personal Identity", "Major Life Changes", "Social Media & Technology", "Uncertainty & Future Planning"))
    time_available = st.number_input(question_time_available, min_value=min_limit+2, max_value=2*max_limit)
    suggestions = st.number_input(question_suggestions, min_value=min_limit, max_value=max_limit)
    sign_in_button = st.button('Let us get started', on_click=create_user, args=[user_username,user_passcode,age, focus_area, time_available, suggestions])

elif st.session_state.page == 2:

    # The SideBar - User Information
    if not user == None:
        st.sidebar.write(update_user_streak(user['Passcode']))
        st.sidebar.write('Username:', user['Username'])
        st.sidebar.write('Focus Area:', user['Focus_Area'])
        st.sidebar.write('Number of Suggestions:', user['Suggestions'])
        st.sidebar.write('Time Available:', user['Time_Available'])
        st.sidebar.write('Days Connected:', user['Days_Summed'])
        st.sidebar.write('Streak:', user['Streak'])
        st.sidebar.write("Don't show me the same saggestion for ", user['Repeat_Preference'], ' day(s) after') 
    else:
        st.sidebar.write('Something went wrong, user not registered.')

    # The Title
    if not user == None:
        st.sidebar.write("Hello", user['Username']) 
        """Please answer the questions below"""
    else:
        st.write('Something went wrong, user not registered.')

    # The Daily Question Section
    min_limit = 1
    max_limit = 10
    question_stress_level = "How would you rate your stress level?"
    stress_level = st.number_input(question_stress_level, min_value=min_limit, max_value=max_limit)
    status_button = st.button('Let us get started', on_click=make_status, args=[stress_level])

elif st.session_state.page == 3:

    st.write('The page is now', st.session_state.page)
