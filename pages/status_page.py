import streamlit as st
from mongo_connection import get_user, record_status, record_question, update_user_streak
from Tables import Users

st.title("Tell us how you're doing today!")

if "menu" not in st.session_state:
    st.session_state.menu = False

if "current_username" not in st.session_state:
    st.session_state.current_username = "username"

if not st.session_state.current_username == "username":
    st.write("Hello", st.session_state.current_username, "Please answer the questions below")
else:
    st.write('Something went wrong, user not registered.')

index = get_user(st.session_state.current_username)

min_limit = 1
max_limit = 10

question_focus_area = "Where would you like to focus today?"
question_stress_level = "How would you rate your stress level?"
question_time_available = "How much time are you willing to spend in reducing stress today?"
question_suggestions = "How many suggestions do you want?"

def make_status(focus_area,stress_level,time_available,suggestions):
    if not index == -1:
        move_on, message = record_status(st.session_state.current_username,focus_area,stress_level,time_available,suggestions)
        st.session_state.menu = move_on
        if move_on:
            record_question(question_focus_area,focus_area,st.session_state.current_username)
            record_question(question_stress_level,stress_level,st.session_state.current_username)
            record_question(question_suggestions,suggestions,st.session_state.current_username)
            record_question(question_time_available,time_available,st.session_state.current_username)
        st.sidebar.write(message)

focus_area = st.radio(question_focus_area,("Work/Career", "Finances", "Health & Well-being", "Relationships", "Time Management", "Personal Identity", "Major Life Changes", "Social Media & Technology", "Uncertainty & Future Planning"))
stress_level = st.number_input(question_stress_level, min_value=min_limit, max_value=max_limit)
time_available = st.number_input(question_time_available, min_value=min_limit+2, max_value=2*max_limit)
suggestions = st.number_input(question_suggestions, min_value=min_limit, max_value=max_limit)
status_button = st.button('Let us get started', on_click=make_status, args=[focus_area,stress_level,time_available,suggestions])

if st.session_state.menu and status_button and not index == -1:
    st.switch_page("pages/main.py")

if not index == -1:
    st.sidebar.write(update_user_streak(Users[index]['Username']))
    st.sidebar.write('Name:', Users[index]['Name'])
    st.sidebar.write('Surname:', Users[index]['Surname'])
    st.sidebar.write('Level:', Users[index]['Level'])
    st.sidebar.write('Score:', Users[index]['Score'])
    st.sidebar.write('Days connected:', Users[index]['Days_Summed'])
    st.sidebar.write('Streak:', Users[index]['Streak'])
    st.sidebar.write("Don't show me the same saggestion for ", Users[index]['Repeat_Preference'], ' day(s) after') 
else:
    st.sidebar.write('Something went wrong, user not registered.')
