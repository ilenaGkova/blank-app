import streamlit as st
from mongo_connection import init_connection, record_status, record_question, update_user_streak

st.title("Tell us how you're doing today!")

if "menu" not in st.session_state:
    st.session_state.menu = False

if "current_passcode" not in st.session_state:
    st.session_state.current_passcode = 1

client = init_connection()
db = client.StressTest
User = db["User"]
current_user = User.find_one({"Passcode": st.session_state.current_passcode})

if not current_user == None:
    st.write("Hello", current_user['Username'], "Please answer the questions below")
else:
    st.write('Something went wrong, user not registered.')

min_limit = 1
max_limit = 10
question_stress_level = "How would you rate your stress level?"


def make_status(stress_level):
    if not current_user == None:
        move_on, message = record_status(st.session_state.current_passcode,stress_level)
        st.session_state.menu = move_on
        if move_on: record_question(question_stress_level,stress_level,st.session_state.current_passcode)
        st.sidebar.write(message)


stress_level = st.number_input(question_stress_level, min_value=min_limit, max_value=max_limit)
status_button = st.button('Let us get started', on_click=make_status, args=[stress_level])

if st.session_state.menu and status_button and not current_user == None:
    st.switch_page("pages/main.py")

if not current_user == None:
    st.sidebar.write(update_user_streak(st.session_state.current_passcode))
    st.sidebar.write('Username:', current_user['Username'])
    st.sidebar.write('Focus Area:', current_user['Focus_Area'])
    st.sidebar.write('Number of Suggestions:', current_user['Suggestions'])
    st.sidebar.write('Time Available:', current_user['Time_Available'])
    st.sidebar.write('Days Connected:', current_user['Days_Summed'])
    st.sidebar.write('Streak:', current_user['Streak'])
    st.sidebar.write("Don't show me the same saggestion for ", current_user['Repeat_Preference'], ' day(s) after') 
else:
    st.sidebar.write('Something went wrong, user not registered.')
