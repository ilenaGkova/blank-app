import streamlit as st  # Streamlit Software
from initialise_variables import initialize_variables  # Application Function

if "current_passcode" not in st.session_state:
    st.session_state.current_passcode = 1  # Will register the user operating the application

if "open_recommendation" not in st.session_state:
    st.session_state.open_recommendation = -1  # Will select a recommendation to open in full

if 'error' not in st.session_state:
    st.session_state.error = ''  # Will store error logs for functions called

if 'error_status' not in st.session_state:
    st.session_state.error_status = None  # Will indicate whether there is an error to show


def layout():

    user, today, yesterday, index, recommendation = initialize_variables(st.session_state.current_passcode,
                                                                         st.session_state.open_recommendation)

    if user is not None and index != -1:
        # Below is the tutorial, broken in small chapters.
        # The titles of the chapters are the st.header assets
        # Section starts with the 'with st.container(border=True):' command

        # The Title

        st.title('Welcome to our application')

        st.write('Here’s a quick guide on how to navigate the application.')

        # The sections

        with st.container(border=True):  # Hug each section in a square to seperate them

            st.header('Signing In')

            st.write('To sign in, enter your unique 10-digit code ', user['Passcode'],
                     ' into the Passcode field on the login section on the initial page.')

        with st.container(border=True):  # Hug each section in a square to seperate them

            st.header('Daily Stress Questionnaire')

            st.write('Every day, you’ll need to fill out a Questionnaire to rate your daily stress.')
            st.write('You only need to complete this once per day, not every time you log in.')

        with st.container(border=True):  # Hug each section in a square to seperate them

            st.header('Recommendations')

            st.write(
                'Based on your Stress Questionnaire answers and the number of suggestions you choose, you will receive tasks on the Home page.')
            st.write(
                'To complete a task and earn points click the button with the :material/done_outline: icon next to it.')
            st.write(
                'To mark your favorites click the button with the :material/thumb_up: icon next to the task you like.')
            st.write(
                'To avoid future suggestions click the button with the :material/thumb_down: icon next to the task you don’t want to see again.')
            st.write(
                'To remove any of the :material/thumb_up: or :material/thumb_down: registration click the button with the :material/delete: icon.')
            st.write(
                'That option is available at the Home page or the ‘Profile and Preferences’ page at the navigation menu.')
            st.write('To see a task in detail click the :material/open_in_full: button next to it.')
            st.write("Want another task? Click on the 'Get another task' button under the tasks given to you")
            st.write(
                'If you want new tasks all together? To the Daily Stress Questionnaire again by clicking on the ‘Daily Stress Questionnaire’. You will locate it in our navigation menu on your left.')

        with st.container(border=True):  # Hug each section in a square to seperate them

            st.header('Scores and Levels')

            st.write('You earn points by completing recommendations. Every Monday, your score will determine:')
            st.write('Whether you move up to a new level.')
            st.write('Whether you stay at your current level.')
            st.write('Whether you are demoted to a lower level.')
            st.write(
                'You can track your progress and check when the next level assessment is on the home page. After each assessment your score will reset to 0.')
            st.write(
                'Your level affects how many points you earn per recommendation and the scores needed to advance or get demoted.')

        with st.container(border=True):  # Hug each section in a square to seperate them

            st.header('Score History')

            st.write(
                "At the home page you will find a box called 'See your record history'. if you click that you will see how your score has progressed during you time in the application in a graph.")
            st.write("The dots represent a record of your score changing.")
            st.write(
                "Red is for scores that would get demoted, Blue is for unaffected scores and Green is for scores that get promoted.")
            st.write('To close the score history click the box again.')

        with st.container(border=True):  # Hug each section in a square to seperate them

            st.header('Your Preferences')

            st.write(
                'Go to the ‘Profile and Preferences’ page in the navigation menu to view your profile and preferences.')
            st.write('See the tasks you have marked as favorites or not favorites.')
            st.write(
                'Adjust your tasks and follow the instructions on the page to filter the types of tasks you want to see.')
            st.write('To navigate the results by keeping track of the icons next to the results:')
            st.write('Look for the :material/badge: icon to find a task given to you.')
            st.write('Look for the :material/done_outline: icon to find a completed task.')
            st.write('Look for the :material/thumb_down: icon to find a removed task.')
            st.write('Look for the :material/thumb_up: icon to find a favorite task.')
            st.write(
                'Look for the :material/delete: icon to remove a recommendation from the :material/thumb_down: or :material/thumb_up: category.')
            st.write('Click on the :material/open_in_full: icon to open the recommendation in full.')

        with st.container(border=True):  # Hug each section in a square to seperate them

            st.header('Your Record')

            st.write('Click the ‘See Record’ button in the navigation menu to view your application history.')
            st.write(
                'Filter by categories and follow the instructions on the page to track specific actions you’ve taken in the app.')

        with st.container(border=True):  # Hug each section in a square to seperate them

            st.header('Confessions')

            st.write(
                "Feel like journaling? Click in the 'Make a confession' page in the navigation menu and make a confession.")
            st.write(
                'You will also be able to manage your confessions on that page. To delete a confession click on the button with the :material/delete: icon.')

        # Closing the Tutorial

        st.write('We hope this helps you navigate the app with ease! Let us know if you need further assistance.')
