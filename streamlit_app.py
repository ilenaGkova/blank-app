import streamlit as st

# Configuration Command

st.set_page_config(
    page_title="StressTest",
    page_icon="👋",
)

# Additional Imports
import plotly.graph_objects as go  # Needs to be downloaded
from datetime import datetime, timedelta
from streamlit_cookies_controller import CookieController  # Needs to be downloaded
from Tables import Recommendations, Tags, Users  # Import from files
from mongo_connection import add_points, change_recommendation_preference_for_user, determine_level_change, \
    generate_animal_username, generate_unique_passcode, get_limits, get_recommendations, get_record, get_status, \
    init_connection, make_recommendation_table, record_status, update_user_streak, validate_user, new_user, \
    record_question, create_history, delete_entry, create_recommendation_history, update_user, add_recommendation, \
    add_tag  # Import from files

# Part A: The Initial Session Variables

if "page" not in st.session_state:
    st.session_state.page = 1  # Will set the layout the application will open

if "current_passcode" not in st.session_state:
    st.session_state.current_passcode = 1  # Will register the user operating the application

if "open_recommendation" not in st.session_state:
    st.session_state.open_recommendation = -1  # Will select a recommendation to open in full

if 'previous_passcode' not in st.session_state:
    st.session_state.previous_passcode = ''  # Will register the last passcode used so the used doesn't have to remember it

if 'error' not in st.session_state:
    st.session_state.error = ''  # Will store error logs for functions called

if 'error_status' not in st.session_state:
    st.session_state.error_status = False  # Will indicate whether there is an error to show

if "username" not in st.session_state:
    st.session_state.username = generate_animal_username()  # Will store temporary username so user can sign up without generating a new one each time they select an option

# Part B: The Global But Not Session Variables

# Step 1: Get database connection and collections

client = init_connection()  # Will establish connection with the database
db = client.StressTest  # Will locate the database
User = db["User"]  # Will get collection user to find the user registered when needed
Tag = db["Tag"]  # Will get the collection Tag to show tags related to recommendations
Recommendation = db[
    "Recommendation"]  # Will get the collection Recommendation to generate a new recommendation ID OR count entries when needed
Question = db["Question"]  # Will get the collection Question to get a user's confessions when needed
Status = db["Status"]  # Will get the collection Status to see to count entries made by the user and see if they are new

# Step 2: Initialise collections with data if needed

if not User.find_one({"Username": "Admin"}):  # Will initialise collection User with default data
    User.insert_many(Users)

if not Tag.find_one({"ID": 1}):  # Will initialise collection Tag with default data
    Tag.insert_many(Tags)

if not Recommendation.find_one({"ID": 1}):  # Will initialise collection Recommendation with default data
    Recommendation.insert_many(Recommendations)

# Step 3: User cookies to get a previous password

controller = CookieController()
cookies = controller.getAll()
st.session_state.previous_passcode = cookies.get("previous_user_passcode",
                                                 "")  # Save the previous passcode on the session variable

# Step 4: Get the conditions needed to open pages and to make sure the user doesn't skip necessary pages

user = User.find_one(
    {"Passcode": st.session_state.current_passcode})  # Will be the user using the application currently
today, yesterday, index = get_status(
    st.session_state.current_passcode)  # Will tell us if the user needs to make a status today
recommendation = Recommendation.find_one(
    {"ID": st.session_state.open_recommendation})  # Will tell us if the user picked a recommendation to open

# Step 5: Initialise variables used in multable pages

question_username = "What's your username?"
question_age = "Age"
question_focus_area = "Where would you like to focus?"
question_time_available = "How much time are you willing to spend in reducing stress?"
question_suggestions = "How many suggestions do you want?"
question_passcode = "What's your passcode?"
min_limit = 1
max_limit = 20
stress_max_limit = 10


# Part C: The Functions

def change_page(new_page):  # This function will change the page

    st.session_state.page = new_page  # By changing the page number we change the layout
    st.session_state.error_status = True  # Will reset the status of the error message so it doesn't follow the user


# Layouts and numbers assigned
# 1 is the page where the user makes a new account or signs in with their passcode
# 2 is the page where the user can answer questions about stress levels
# 3 is the home page where the user can see and complete recommendations
# 4 is the profile and preferences page where the user can update their profile and manage their preferences
# 5 is the Record page where the user can see their application history
# 6 is the page where the user can see a recommendation in full
# 7 is the tutorial page where the user can see how the application works
# 8 is the page where the user can make a confession and manage their confessions
# 9 is the page where an admin can add a recommendation or tag


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


def create_user(user_user_username, user_user_passcode, user_age, user_focus_area, user_time_available,
                user_suggestions, question_username_for_create_user, question_age_for_create_user,
                question_focus_area_for_create_user, question_time_available_for_create_user,
                question_suggestions_for_create_user,
                question_passcode_for_create_user):  # Called when a user wants to make a new account

    st.session_state.error_status, st.session_state.error = new_user(user_user_username, user_user_passcode, user_age,
                                                                     user_focus_area,
                                                                     user_time_available,
                                                                     user_suggestions)  # Will update the session error variables and maybe create new user if appropriate

    if st.session_state.error_status:  # Warning: The status variable is in reverse

        controller.set("previous_user_passcode",
                       str(user_user_passcode))  # Will remember the passcode for the future so the user won't have to enter it

        # We need record the answer the user gave to a question everytime the user enters something in a field or selects an answer out of a radio button
        record_question(question_username_for_create_user, user_user_username, passcode)
        record_question(question_passcode_for_create_user, user_user_passcode, passcode)
        record_question(question_age_for_create_user, user_age, passcode)
        record_question(question_focus_area_for_create_user, user_focus_area, passcode)
        record_question(question_time_available_for_create_user, user_time_available, passcode)
        record_question(question_suggestions_for_create_user, user_suggestions, passcode)

        set_username(
            user_user_passcode)  # Will call the function to register the user as the current user and move on to the next page


def make_status(
        user_stress_level):  # Called when the user makes a status by answering questions about their stress level

    st.session_state.error_status, st.session_state.error = record_status(st.session_state.current_passcode,
                                                                          user_stress_level)  # Will update the session error variables and maybe create new status for user if appropriate

    if st.session_state.error_status:  # Warning: The status variable is in reverse

        # We need record the answer the user gave to a question everytime the user enters something in a field or selects an answer out of a radio button
        record_question(question_stress_level, user_stress_level, st.session_state.current_passcode)

        change_page(3)  # Will can function to move to Home page


def create_custom_slider(min_value, max_value, down_barrier, up_barrier,
                         score):  # Called with the home page, will visualise the user's score to make it easy to track progress

    scale = go.Figure()

    scale.add_shape(type="line", x0=min_value, y0=0, x1=max_value, y1=0,
                    line=dict(color="RoyalBlue", width=4))  # Step 1: Make the line in blue

    # Step 2: Add the numbers to see
    scale.add_trace(go.Scatter(
        x=[down_barrier],
        y=[0],
        mode="markers",  # The coordinates will be shown as a dot
        marker=dict(size=15, color="red"),  # Scores below this number will be demoted so the dot will be in red
        name="Demotion Point",  # Will name the dot
        hovertemplate="Demotion Point: %{x}<extra></extra>"  # When hovering will show number, not coordinates
    ))

    scale.add_trace(go.Scatter(
        x=[up_barrier],
        y=[0],
        mode="markers",  # The coordinates will be shown as a dot
        marker=dict(size=15, color="green"),  # Scores above this number will be promoted so the dot will be in green
        name="Promotion Point",  # Will name the dot
        hovertemplate="Promotion Point: %{x}<extra></extra>"  # When hovering will show number, not coordinates
    ))

    scale.add_trace(go.Scatter(
        x=[score],
        y=[0],
        mode="markers",  # The coordinates will be shown as a dot
        marker=dict(size=15, color="RoyalBlue"),  # The user's score is a dot that will be blue like the line
        name="Your Score",  # Will name the dot
        hovertemplate="Your Score: %{x}<extra></extra>"  # When hovering will show number, not coordinates
    ))

    # Step 3: Make the scale
    scale.update_layout(
        height=150,
        xaxis=dict(range=[min_value, max_value], title=None),
        # Will start showing the numbers from 0 and up until the maximum value
        yaxis=dict(visible=False, range=[-1, 1]),
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="white",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x"
    )

    return scale


def get_time():  # Called with the home page to get the count-down towards the next level assessment

    now = datetime.now()  # Step 1: Get current day / time

    # Step 2: Get next level assessment. Level assessment happen every monday morning.
    days_until_sunday = (6 - now.weekday()) % 7
    next_sunday_midnight = (now + timedelta(days=days_until_sunday)).replace(hour=23, minute=59, second=59,
                                                                             microsecond=999999)

    # Step 3: Get time remaining and separate into days, hours, minutes and seconds
    time_remaining = next_sunday_midnight - now
    hours, remainder = divmod(time_remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{days_until_sunday}:{hours:02}:{minutes:02}:{seconds:02}"  # Will return time remaining repeated


def completed_recommendation(index_for_completed_recommendation,
                             status):  # Called when the user completes a recommendation

    st.session_state.error_status, st.session_state.error = add_points(index_for_completed_recommendation,
                                                                       st.session_state.current_passcode,
                                                                       status)  # Will update the session error variables and maybe increase the user's score if appropriate

    if st.session_state.error_status:  # Warning: The status variable is in reverse

        change_page(st.session_state.page)  # Will change the page to itself to reload and see the result


def change_recommendation_status(preference, index_for_change_recommendation_status,
                                 function=None):  # Will be called if the user wants to add / remove a recommendation form the favorite / removed category

    # Will update the session error variables and remove a recommendation from the favorite / removed category
    # Depending on whether the function parameter is None it will also add the recommendation either into the favorite or removed collection
    st.session_state.error_status, st.session_state.error = change_recommendation_preference_for_user(preference,
                                                                                                      st.session_state.current_passcode,
                                                                                                      index_for_change_recommendation_status,
                                                                                                      function)
    if st.session_state.error_status:  # Warning: The status variable is in reverse

        change_page(st.session_state.page)  # Will change the page to itself to reload and see the result


def update_user_here(new_username, passcode_for_update_employee, new_age, new_focus_area, new_time_available,
                     new_suggestions, new_repeat, question_username_for_update_user, question_age_for_update_user,
                     question_focus_area_for_update_user, question_time_available_for_update_user,
                     question_suggestions_for_update_user,
                     repeat_question):  # Called when the user wants to update their profile information

    st.session_state.error_status, st.session_state.error = update_user(passcode_for_update_employee, new_username,
                                                                        new_repeat, new_age,
                                                                        new_focus_area,
                                                                        new_time_available,
                                                                        new_suggestions)  # Will update the session error variables and maybe change user information if appropriate

    if st.session_state.error_status:  # Warning: The status variable is in reverse

        # We need record the answer the user gave to a question everytime the user enters something in a field or selects an answer out of a radio button
        record_question(question_username_for_update_user, new_username, passcode_for_update_employee)
        record_question(question_age_for_update_user, new_age, passcode_for_update_employee)
        record_question(question_focus_area_for_update_user, new_focus_area, passcode_for_update_employee)
        record_question(question_time_available_for_update_user, new_time_available, passcode_for_update_employee)
        record_question(question_suggestions_for_update_user, new_suggestions, passcode_for_update_employee)
        record_question(repeat_question, new_repeat, passcode_for_update_employee)

        change_page(st.session_state.page)  # Will change the page to itself to reload and see the result


def open_recommendation(index_for_open_recommendation):  # Called when user wants to see a recommendation in full

    st.session_state.open_recommendation = index_for_open_recommendation  # Will set the recommendation to be opened

    change_page(6)  # Will change page layout to show the recommendation


def generate_recommendation_id():  # Called what an admin wants to make a new recommendation

    # Step 1: Get bigger ID in recommendation collection
    last_entry = Recommendation.find_one({}, sort=[("ID", -1)])

    if last_entry:

        generated_id = int(last_entry['ID']) + 1

    else:

        generated_id = 1

    # Step 2: Increase by 1 until the new id doesn't exist
    while Recommendation.find_one({"ID": generated_id}):
        generated_id += 1

    return generated_id


def add_recommendation_here(your_passcode_here, this_generated_id_here, points_here, title_here, description_here,
                            link_here, question_about_recommendation_id_here, question_about_points_here,
                            question_about_title_here, question_about_description_here,
                            question_about_link_here):  # Called when the user wants to make a new recommendation

    st.session_state.error_status, st.session_state.error = add_recommendation(this_generated_id_here,
                                                                               your_passcode_here, title_here,
                                                                               description_here, link_here,
                                                                               points_here)  # Will update the session error variables and maybe add a recommendation if appropriate
    if st.session_state.error_status:  # Warning: The status variable is in reverse

        # We need record the answer the user gave to a question everytime the user enters something in a field or selects an answer out of a radio button
        record_question(question_about_recommendation_id_here, this_generated_id_here, your_passcode_here)
        record_question(question_about_points_here, points_here, your_passcode_here)
        record_question(question_about_title_here, title_here, your_passcode_here)
        record_question(question_about_description_here, description_here, your_passcode_here)
        record_question(question_about_link_here, link_here, your_passcode_here)

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


# Part D: The layouts

# Step 1: Show the error if needed

if not st.session_state.error_status:
    with st.container(border=True):
        st.header(st.session_state.error)

# Step 2: Show the rest of the page

# Layouts and numbers assigned
# 1 is the page where the user makes a new account or signs in with their passcode
# 2 is the page where the user can answer questions about stress levels
# 3 is the home page where the user can see and complete recommendations
# 4 is the profile and preferences page where the user can update their profile and manage their preferences
# 5 is the Record page where the user can see their application history
# 6 is the page where the user can see a recommendation in full
# 7 is the tutorial page where the user can see how the application works
# 8 is the page where the user can make a confession and manage their confessions
# 9 is the page where an admin can add a recommendation or tag

# Layout logistics
# There is a conditional statement. Depending on the number of the st.session_state.page value different assets will be generated.
# Each asset however needs their own quick name to be identified.
# Except page 1 every page needs a valid user to be signed in. Pages 1 and 2 are the only pages that don't require a status to be made by the user and page 6 needs a valid recommendation number.
# The above conditions are initialised in Part B Step 4 every time the page loads.
# From now on any button needs a distinct key, it will be found as the key="XXX" in the button parameters, input fields are the same
# Buttons have other parameters like on_click= XXXXX is the function called when the button is clicked or args = [XXXXX, YYYYY] are the parameters of the function
# Text can be show either by a streamlit option, st.write/header/title... or use html in st.markdown. Both are utilised here.

if st.session_state.page == 1:  # 1 is the page where the user makes a new account or signs in with their passcode

    # The SideBar - User Signs In With Passcode

    st.sidebar.write('Already have an account? Sign in!')
    passcode = st.sidebar.text_input(question_passcode, key="passcode", value=st.session_state.previous_passcode)
    st.sidebar.button('Log in', on_click=log_in_user, args=[passcode, question_passcode], key="sign_in_user")

    # The Title

    """
    # Wellcome to Stressless Living!
    New here? Please answer the following questions and we'll create your account. If you have an account sign in on the left.
    """

    # The Initial Questions Section

    if Recommendation.count_documents(
            {}) >= 1:  # The application won't sign on new users if there are no recommendations to be given

        # Step 1: User enters a username - randomly generated at first

        user_username = st.text_input(question_username, key="user_username", value=st.session_state.username)

        if user_username != st.session_state.username:
            st.session_state.username = user_username  # Save the username the user gave to avoid generating another later

        # Step 2: Generate a password randomly with 10 digits

        user_passcode = generate_unique_passcode()

        # Step 3: User enters an Age category and focus area to personalise the experience

        age = st.radio(question_age, ("18-25", "26-35", "36-55", "56-70", "70+"))

        focus_area = st.radio(question_focus_area, (
            "Work/Career", "Finances", "Health & Well-being", "Relationships", "Time Management", "Personal Identity",
            "Major Life Changes", "Social Media & Technology", "Uncertainty & Future Planning"))

        # Step 4: User enters their free time amount and the amount of suggestion they wish to see

        time_available = st.number_input(question_time_available, min_value=min_limit, max_value=max_limit)

        suggestions = st.number_input(question_suggestions, min_value=min_limit,
                                      max_value=Recommendation.count_documents(
                                          {}))  # Set maximum at the amount of suggestions available

        # Step 5: User clicks button to create an account

        st.button('Let us get started', on_click=create_user,
                  args=[user_username, user_passcode, age, focus_area, time_available, suggestions, question_username,
                        question_age, question_focus_area, question_time_available, question_suggestions,
                        question_passcode], key="create_user")

elif st.session_state.page == 2:  # 2 is the page where the user can answer questions about stress levels

    if user is not None:

        # The SideBar - User Information

        # User streaks and day connected are only altered once a day, the function has safeguards to avoid altering them a second time
        # Look into the mongo file for more

        st.sidebar.write(update_user_streak(user['Passcode']))

        # Show the user information and preferences

        st.sidebar.write('Username:', user['Username'])
        st.sidebar.write('Focus Area:', user['Focus_Area'])
        st.sidebar.write('Number of Suggestions:', user['Suggestions'])
        st.sidebar.write('Time Available:', user['Time_Available'])
        st.sidebar.write('Days Connected:', user['Days_Summed'])
        st.sidebar.write('Streak:', user['Streak'])
        st.sidebar.write("Don't show me the same suggestion for ", user['Repeat_Preference'], ' day(s) after')

        if today:  # Sometimes users do multable statuses a day, if one has been done the user doesn't need to make another unless they want to

            st.sidebar.button('Skip', on_click=change_page, args=[3], key="skip")

        # The Title

        st.title(f"Hello {user['Username']}")
        """Please answer the questions below"""

        # The Daily Question Section

        question_stress_level = "How would you rate your stress level?"  # Step 1: Answer question(s) to rate stress levels

        stress_level = st.number_input(question_stress_level, min_value=min_limit, max_value=stress_max_limit)

        st.button('Let us get started', on_click=make_status, args=[stress_level],
                  key="make_status")  # Step 2: Click button to submit answers

    else:

        # Page won't open unless user is registered

        st.session_state.error_status = False
        st.session_state.error_status = "Something went wrong, user not registered."

else:

    # After the point the user sees the same menu in each of the next pages

    # Layouts and numbers assigned
    # 1 is the page where the user makes a new account or signs in with their passcode
    # 2 is the page where the user can answer questions about stress levels
    # 3 is the home page where the user can see and complete recommendations
    # 4 is the profile and preferences page where the user can update their profile and manage their preferences
    # 5 is the Record page where the user can see their application history
    # 6 is the page where the user can see a recommendation in full
    # 7 is the tutorial page where the user can see how the application works
    # 8 is the page where the user can make a confession and manage their confessions
    # 9 is the page where an admin can add a recommendation or tag

    st.sidebar.markdown(f"<div style='text-align: center;font-size: 20px; font-weight: bold;'>Navigation Menu</div>",
                        unsafe_allow_html=True)

    st.sidebar.write("")  # Add blank line

    if user is not None and index != -1 and user['Role'] == 'User':  # Users have a more limited menu than an admin

        st.sidebar.button("Home", icon=":material/home:", use_container_width=True, on_click=change_page, args=[3],
                          key="main_page")
        st.sidebar.button("Profile and Preferences", icon=":material/person_3:", use_container_width=True,
                          on_click=change_page, args=[4], key="profile_page")
        st.sidebar.button("Still stressed? Try again", icon=":material/add:", use_container_width=True, on_click=change_page,
                          args=[2], key="status_page")
        st.sidebar.button("See Record", icon=":material/clinical_notes:", use_container_width=True,
                          on_click=change_page, args=[5], key="record_page")
        st.sidebar.button('Make a confession', icon=":material/draw:", use_container_width=True,
                          on_click=change_page,
                          args=[8], key="make_confession")
        st.sidebar.button("See Tutorial", icon=":material/auto_stories:", use_container_width=True,
                          on_click=change_page, args=[7], key="tutorial_page")
        st.sidebar.button("Exit", icon=":material/logout:", use_container_width=True, on_click=change_page, args=[1],
                          key="log_out")

    elif user is not None and index != -1:

        st.sidebar.button("Home", icon=":material/home:", use_container_width=True, on_click=change_page, args=[3],
                          key="main_page_admin")
        st.sidebar.button("Profile and Preferences", icon=":material/person_3:", use_container_width=True,
                          on_click=change_page, args=[4], key="profile_page_admin")
        st.sidebar.button("Still stressed? Try again", icon=":material/add:", use_container_width=True, on_click=change_page,
                          args=[2], key="status_page_admin")
        st.sidebar.button("See Record", icon=":material/clinical_notes:", use_container_width=True,
                          on_click=change_page, args=[5], key="record_page_admin")
        st.sidebar.button('Add Recommendation', icon=":material/add_circle:", use_container_width=True,
                          on_click=change_page,
                          args=[9], key="admin_add_page_admin")
        st.sidebar.button('Make a confession', icon=":material/draw:", use_container_width=True,
                          on_click=change_page,
                          args=[8], key="admin_make_confession_admin")
        st.sidebar.button("See Tutorial", icon=":material/auto_stories:", use_container_width=True,
                          on_click=change_page, args=[7], key="tutorial_page_admin")
        st.sidebar.button("Exit", icon=":material/logout:", use_container_width=True, on_click=change_page, args=[1],
                          key="log_out_admin")

    elif user is None:

        # Page won't open unless user is registered

        st.session_state.error_status = False
        st.session_state.error_status = "Something went wrong, user not registered."

    else:

        # Page won't open unless user has made a status  is registered

        st.session_state.error_status = False
        st.session_state.error_status = "Something went wrong, status not found."

    if st.session_state.page == 3:  # 3 is the home page where the user can see and complete recommendations

        if user is not None and index != -1:

            # The Title

            st.markdown(
                f"<div style='text-align: center;font-size: 60px;font-weight: bold;'>Hello {user['Username']}, we are happy to see you!</div>",
                unsafe_allow_html=True)

            # Section 1: Streak and Days Connected

            with st.container(border=True):

                show_streak, show_days_connected = st.columns([2, 2])  # Show the information side by side

                with show_streak:

                    st.markdown(
                        f"<div style='text-align: center;font-size: 30px;'>Streak</div>",
                        unsafe_allow_html=True)

                    st.markdown(
                        f"<div style='text-align: center;font-size: 60px;font-weight: bold;'>{user['Streak']}</div>",
                        unsafe_allow_html=True)

                with show_days_connected:

                    st.markdown(
                        f"<div style='text-align: center;font-size: 30px;'>Days connected</div>",
                        unsafe_allow_html=True)

                    st.markdown(
                        f"<div style='text-align: center;font-size: 60px;font-weight: bold;'>{user['Days_Summed']}</div>",
                        unsafe_allow_html=True)

            # Section 2: User Score and Level

            st.subheader('Your Level / Score')

            with st.container(border=True):

                # Step 1: Check if the level or score need to be altered

                if get_record(st.session_state.current_passcode):  # Levels and scores are altered 1 a week
                    st.header(determine_level_change(st.session_state.current_passcode))  # Will do the alteration
                    user = User.find_one({"Passcode": st.session_state.current_passcode})  # Will update the user after the alteration

                # Step 2: Show level and score

                show_level, show_score = st.columns([1, 5]) # Show the information side by side

                with show_level:

                    st.markdown(
                        f"<div style='text-align: center;font-size: 60px;font-weight: bold;'>{user['Level']}</div>",
                        unsafe_allow_html=True)

                with show_score:

                    # Depending on the lever the promotion/demotion points are different
                    # See the mongo file for more

                    up, down = get_limits(user)

                    # Create the slider to show the user score, promotion and demotion points

                    fig = create_custom_slider(0, up + 50, down, up, user['Score'])
                    st.plotly_chart(fig, use_container_width=True)

                # Step 3: Show message

                st.markdown(
                    f"<div style='text-align: left;'>Next level assessments in {get_time()}. Stay above the demotion score to remain to this level or reach the advancement score to move up!</div>",
                    unsafe_allow_html=True)

            if Status.count_documents({"Passcode": st.session_state.current_passcode}) == 1: # For new user, add a message to direct them to the tutorial
                st.header(
                    "New here? Check out our tutorial to better navigate this application! You will locate it in our navigation menu on your left.")

            # Section 3: User Recommendations

            st.subheader('Our recommendations for you today')

            condition, user_recommendations, message = get_recommendations(st.session_state.current_passcode)  # Step 1: Create the recommendation table based on the user's information

            st.write(message)  # Write the result of the function above, see mongo file for more

            if condition:

                condition, user_recommendations = make_recommendation_table(user_recommendations,
                                                                            st.session_state.current_passcode)  # Step 2: Structure the recommendation table in a way that is helpful

                if condition:

                    # Step 3: Assuming nothing went wrong we can show the table

                    for entry in user_recommendations:

                        with (st.container(border=True)):

                            column_for_pointer, column_for_title_or_description, column_for_outcome, column_for_category_in_home_page, column_for_extension_button = st.columns([0.2, 2, 1, 0.5, 0.5])

                            with column_for_pointer:

                                st.markdown(f"<div style='text-align: center;'>{entry['Pointer']}</div>",
                                            unsafe_allow_html=True)

                            with column_for_title_or_description:

                                st.markdown(f"<div style='text-align: center; font-weight: bold;'>{entry['Title']}</div>",
                                            unsafe_allow_html=True)

                                if len(entry['Description']) > 150:  # If description is big enough it won't show. It can be shown by extending the recommendation to full screen

                                    st.markdown(
                                        "<div style='text-align: center;'>Open Recommendation to see description</div>",
                                        unsafe_allow_html=True)
                                else:

                                    st.markdown(f"<div style='text-align: center;'>{entry['Description']}</div>",
                                                unsafe_allow_html=True)
                            with column_for_outcome:

                                # Depending on the outcome the user either sees the points the recommendation curies or what they completed it

                                if entry['Outcome']:

                                    st.markdown(
                                        f"<div style='text-align: center;'>Complete this and gain {user['Level'] * entry['Points']}!</div>",
                                        unsafe_allow_html=True)

                                else:

                                    st.markdown(
                                        f"<div style='text-align: center;'>Recommendation completed {entry['Completed_At']}!</div>",
                                        unsafe_allow_html=True)

                            with column_for_category_in_home_page:

                                # Preference indicates if the recommendation is in the favorite/removed or no section for this user.
                                # Depending on that the user will see a different combination of buttons
                                # A recommendation can't be both in the favorite and removed section. To be in one it will be removed from the other.

                                if entry['Preference'] is False:

                                    st.button("", icon=":material/favorite:", use_container_width=True,
                                              on_click=change_recommendation_status, args=[1, entry['ID']],
                                              key=f"love_{entry['Pointer']}")

                                    st.button("", icon=":material/delete:", use_container_width=True,
                                              on_click=change_recommendation_preference_for_user,
                                              args=[1, st.session_state.current_passcode, entry['ID'], True],
                                              key=f"remove_recommendation_XZa_{entry['Pointer']}")

                                if entry['Preference'] is True:

                                    st.button("", icon=":material/delete:", use_container_width=True,
                                              on_click=change_recommendation_preference_for_user,
                                              args=[1, st.session_state.current_passcode, entry['ID'], True],
                                              key=f"remove_recommendation_XZX_{entry['Pointer']}")

                                    st.button("", icon=":material/heart_broken:", use_container_width=True,
                                              on_click=change_recommendation_status, args=[-1, entry['ID']],
                                              key=f"hate_{entry['Pointer']}")

                                if entry['Preference'] is None:

                                    st.button("", icon=":material/favorite:", use_container_width=True,
                                              on_click=change_recommendation_status, args=[1, entry['ID']],
                                              key=f"love_{entry['Pointer']}_X")

                                    st.button("", icon=":material/heart_broken:", use_container_width=True,
                                              on_click=change_recommendation_status, args=[-1, entry['ID']],
                                              key=f"hate_{entry['Pointer']}_X")

                            with column_for_extension_button:

                                if entry['Outcome']: #

                                    st.button("", icon=":material/done_outline:", use_container_width=True,
                                              on_click=completed_recommendation,
                                              args=[entry['ID'], entry['Status_Created_At']],
                                              key=f"complete_{entry['Pointer']}")

                                st.button("", icon=":material/open_in_full:", use_container_width=True,
                                          on_click=open_recommendation, args=[entry['ID']], key=f"open_{entry['Pointer']}")

    elif st.session_state.page == 4:

        if user is not None and index != -1:

            # The Section Title
            st.title('Your Profile')

            # The Profile Information
            with st.container(border=True):

                column131, column132, column133 = st.columns([2, 2, 2])

                with column131:
                    update_username = st.text_input(question_username, key="update_username", value=user['Username'])
                with column132:
                    update_passcode = st.text_input(question_username, key="update_passcode", value=user['Passcode'])

                column134, column135, column136 = st.columns([2, 2, 2])

                with column134:
                    update_age = st.radio(question_age, ("18-25", "26-35", "36-55", "56-70", "70+"))
                with column135:
                    update_focus_area = st.radio(question_focus_area, (
                        "Work/Career", "Finances", "Health & Well-being", "Relationships", "Time Management",
                        "Personal Identity",
                        "Major Life Changes", "Social Media & Technology", "Uncertainty & Future Planning"))
                with column136:
                    st.write('Current Age Category: ', user['Age_Category'])
                    st.write('Current Focus Area: ', user['Focus_Area'])

                column137, column138, column139 = st.columns([2, 2, 2])

                with column137:
                    update_time_available = st.number_input(question_time_available, min_value=min_limit,
                                                            max_value=max_limit,
                                                            value=user['Time_Available'])
                with column138:
                    update_suggestions = st.number_input(question_suggestions, min_value=min_limit,
                                                         max_value=Recommendation.count_documents({}),
                                                         value=user['Suggestions'])
                with column139:
                    update_repeat = st.number_input(
                        f"You will not see tha same suggestion in {user['Repeat_Preference']} days",
                        min_value=min_limit, max_value=max_limit,
                        value=user['Repeat_Preference'])
                with column133:
                    st.write("")
                    st.button("Save Alterations", icon=":material/save_as:", use_container_width=True,
                              on_click=update_user_here,
                              args=[update_username, update_passcode, update_age, update_focus_area,
                                    update_time_available, update_suggestions, update_repeat,
                                    question_username,
                                    question_age, question_focus_area, question_time_available, question_suggestions,
                                    f"You will not see tha same suggestion in {user['Repeat_Preference']} days"],
                              key="update_user_button")

            # The Section Title
            st.title('Your Preferences')

            # Step 1
            st.header('Step 1: Tell us what you what to see')

            with st.container(border=True):

                column101, column102, column103 = st.columns([2, 2, 2])

                with column101:
                    favorite_status_1 = st.checkbox("See your favorite recommendations")
                with column102:
                    removed_status_1 = st.checkbox("See what recommendations you rejected")
                with column103:
                    person_status_1 = st.checkbox("See what recommendations have been given to you")

            # Step 2
            st.header('Step 2: Pick a sorting method - optional')

            column105, column106 = st.columns([3, 3])

            with column105:
                with st.container(border=True):
                    order_question_1 = st.radio(
                        "Show from",
                        ("A to Z", "Z to A"),
                        index=None
                    )
                    order_1 = -1
                    if order_question_1 == "A to Z":
                        order_1 = 1

            with column106:
                with st.container(border=True):
                    completed_question = st.radio(
                        "Include only",
                        ("Completed Recommendations", "Incomplete Recommendations"),
                        index=None
                    )
                    completed = None
                    if completed_question == "Completed Recommendations":
                        completed = False
                    elif completed_question == "Incomplete Recommendations":
                        completed = True

            # See the result
            st.header('See your record')

            if favorite_status_1 or removed_status_1 or person_status_1:

                condition, user_recommendation_history, message = create_recommendation_history(
                    st.session_state.current_passcode, order_1, favorite_status_1, removed_status_1,
                    person_status_1, completed)

                pointer_1 = 1

                if condition:
                    st.write(message)
                    if len(user_recommendation_history) == 1:
                        st.write('You have ', len(user_recommendation_history), ' result')
                    else:
                        st.write('You have ', len(user_recommendation_history), ' results')
                    for entry in user_recommendation_history:
                        with st.container(border=True):
                            column121, column122, column123, column124, column125 = st.columns([1, 1, 1, 4, 1])
                            with st.container(border=True):
                                with column121:
                                    st.write(pointer_1)
                                with column122:
                                    if entry['Type'] == "Favorite_Recommendation":
                                        st.header(':material/favorite:')
                                    elif entry['Type'] == "Removed_Recommendation":
                                        st.header(':material/heart_broken:')
                                    elif entry['Outcome']:
                                        st.header(':material/badge:')
                                    else:
                                        st.header(':material/badge: :material/done_outline:')
                                with column123:
                                    st.write(entry['Created_At'])
                                with column124:
                                    st.markdown(
                                        f"<div style='text-align: center; font-weight: bold;'>{entry['Title']}</div>",
                                        unsafe_allow_html=True)
                                    if len(entry['Description']) > 150:
                                        st.markdown(
                                            "<div style='text-align: center;'>Open Recommendation to see description</div>",
                                            unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"<div style='text-align: center;'>{entry['Description']}</div>",
                                                    unsafe_allow_html=True)
                                with column125:
                                    if entry['Extend']:
                                        st.button("", icon=":material/open_in_full:", use_container_width=True,
                                                  on_click=open_recommendation, args=[entry['ID']],
                                                  key=f"open_recommendation_XY_{pointer_1}")
                                    if entry['Remove']:
                                        st.button("", icon=":material/delete:", use_container_width=True,
                                                  on_click=change_recommendation_preference_for_user,
                                                  args=[1, st.session_state.current_passcode, entry['ID'], True],
                                                  key=f"remove_recommendation_X_{pointer_1}")
                        pointer_1 += 1
                else:
                    st.write(message)
            else:
                st.write("You haven't selected a category")
        else:
            st.write('Something went wrong, user not found.')

    elif st.session_state.page == 5:

        if user is not None and index != -1:

            # The Title
            st.title('Your Record')

            # Step 1
            st.header('Step 1: Tell us what you what to see')

            with st.container(border=True):

                column16, column26, column36 = st.columns([2, 2, 2])

                with column16:
                    user_status = st.checkbox("See when your profile was generated")
                with column26:
                    question_status = st.checkbox("See what questions you have answered")
                with column36:
                    record_status = st.checkbox("See what actions the application has done on your behalf")

                column46, column56, column66 = st.columns([2, 2, 2])

                with column46:
                    status_status = st.checkbox("See when you answered the Stress Daily Stress Questionnaire")
                with column56:
                    recommendation_status = st.checkbox("See what recommendations you have entered")
                with column66:
                    tag_status = st.checkbox("See what Tags you have added to recommendations")

                column76, column86, column96 = st.columns([2, 2, 2])

                with column76:
                    favorite_status = st.checkbox("See your favorite recommendations")
                with column86:
                    removed_status = st.checkbox("See what recommendations you rejected")
                with column96:
                    person_status = st.checkbox("See what recommendations have been given to you")

            # Step 2
            st.header('Step 2: Pick a sorting method - optional')

            column17, column27 = st.columns([3, 3])

            with column17:
                with st.container(border=True):
                    priority = st.radio(
                        "Sort By",
                        ("Time", "Substance"),
                        index=None
                    )

            with column27:
                with st.container(border=True):
                    order_question = st.radio(
                        "Show from",
                        ("A to Z", "Z to A"),
                        index=None
                    )
                    order = -1
                    if order_question == "A to Z":
                        order = 1

            user_passcode_search = st.text_input("Search for user", key="user_username_for_search",
                                                 value=st.session_state.current_passcode,
                                                 disabled=(user['Role'] == 'User'))

            # See the result
            st.header('See your record')

            if user_status or question_status or record_status or status_status or recommendation_status or tag_status or favorite_status or removed_status or person_status:

                condition, user_history, message = create_history(user_passcode_search, priority, order,
                                                                  user_status, question_status, record_status,
                                                                  status_status, recommendation_status, tag_status,
                                                                  favorite_status, removed_status, person_status)
                pointer = 1
                if condition:
                    st.write(message)
                    if len(user_history) == 1:
                        st.write('You have ', len(user_history), ' result')
                    else:
                        st.write('You have ', len(user_history), ' results')
                    for entry in user_history:
                        with st.container(border=True):
                            condition1 = entry['Type'] == "Recommendation" or entry['Type'] == "Tag" or entry[
                                'Type'] == "Favorite_Recommendation" or entry['Type'] == "Removed_Recommendation"
                            condition2 = entry['Type'] == "Recommendation_Per_Person"
                            if user['Role'] == 'User':
                                column19, column29, column49, column59 = st.columns([2, 2, 4, 1])
                                with column19:
                                    st.write(pointer)
                                with column29:
                                    st.write(entry['Created_At'])
                                with column49:
                                    st.write(entry['Message'])
                                with column48:
                                    if condition1:
                                        st.button("", icon=":material/open_in_full:", use_container_width=True,
                                                  on_click=open_recommendation, args=[entry['Key']],
                                                  key=f"open_recommendation_Z_{pointer}")
                                    elif condition2:
                                        st.button("", icon=":material/open_in_full:", use_container_width=True,
                                                  on_click=open_recommendation, args=[entry['Key2']],
                                                  key=f"open_recommendation_C_{pointer}")
                            else:
                                column18, column28, column38, column48, column58 = st.columns([2, 2, 2, 4, 1])
                                with column18:
                                    st.write(pointer)
                                with column28:
                                    st.write(entry['Created_At'])
                                with column38:
                                    st.write(entry['Type'])
                                with column48:
                                    st.write(entry['Message'])
                                with column58:
                                    if condition1:
                                        st.button("", icon=":material/open_in_full:", use_container_width=True,
                                                  on_click=open_recommendation, args=[entry['Key']],
                                                  key=f"open_recommendation_X_{pointer}")
                                    elif condition2:
                                        st.button("", icon=":material/open_in_full:", use_container_width=True,
                                                  on_click=open_recommendation, args=[entry['Key2']],
                                                  key=f"open_recommendation_Y_{pointer}")
                                    st.button("", icon=":material/delete:", use_container_width=True,
                                              on_click=delete_entry,
                                              args=[entry['Passcode'], entry['Key'], entry['Key2'], entry['Created_At'],
                                                    entry['Type'], st.session_state.current_passcode],
                                              key=f"delete_{pointer}")
                        pointer += 1
                else:
                    st.write(message)
            else:
                st.write("You haven't selected a category")
        else:
            st.write('Something went wrong, user not found.')

    elif st.session_state.page == 6:

        if recommendation is not None and user is not None and index != -1:

            # The Title
            with st.container(border=True):
                st.markdown(
                    f"<div style='text-align: center;font-size: 40px;font-weight: bold;'>{recommendation['Title']}</div>",
                    unsafe_allow_html=True)

            st.write("")
            st.write("")
            st.write("")
            st.write("")

            # The Side Information
            column14, column24, column34, column44 = st.columns([1, 2, 2, 3])
            with st.container(border=True):
                with column14:
                    st.markdown(
                        f"<div style='text-align: center;font-size: 15px;'>{recommendation['ID']}</div>",
                        unsafe_allow_html=True)
                with column24:
                    st.markdown(
                        f"<div style='text-align: center;font-size: 15px;'>Created By</div>",
                        unsafe_allow_html=True)
                    data = User.find_one({"Passcode": recommendation['Passcode']})['Username']
                    st.markdown(
                        f"<div style='text-align: center;font-size: 15px;'>{data}</div>",
                        unsafe_allow_html=True)
                with column34:
                    st.markdown(
                        f"<div style='text-align: center;font-size: 15px;'>Created At</div>",
                        unsafe_allow_html=True)
                    st.markdown(
                        f"<div style='text-align: center;font-size: 15px;'>{recommendation['Created_At']}</div>",
                        unsafe_allow_html=True)
                with column44:
                    st.markdown(
                        f"<div style='text-align: center;font-size: 15px;'>Minimum Points awarded: {recommendation['Points']}</div>",
                        unsafe_allow_html=True)

            st.write("")
            st.write("")
            st.write("")
            st.write("")

            # The Recommendation
            Tag.count_documents({"ID": recommendation['ID']})
            if Tag.count_documents({"ID": recommendation['ID']}) == 0:
                with st.container(border=True):
                    st.write(recommendation['Description'])
                    if recommendation['Link'] is not None:
                        st.write('See more information on ', recommendation['Link'])
            else:
                column15, column25 = st.columns([5, 2])
                with column15:
                    with st.container(border=True):
                        st.write(recommendation['Description'])
                        if recommendation['Link'] is not None:
                            st.write('See more information on ', recommendation['Link'])
                    with column25:
                        st.write("Tags related to this recommendation:")
                        tags = list(Tag.find({"ID": recommendation['ID']}))
                        for entry in tags:
                            st.write(entry['Title_Of_Criteria'], ': ', entry['Category'], 'as assigned by, ',
                                     User.find_one({"Passcode": entry['Passcode']})['Username'])

        elif recommendation:
            st.write('Something went wrong, user not found.')
        elif user:
            st.write('Something went wrong, recommendation not found.')
        else:
            st.write('Something went wrong, user and recommendation not found.')

    elif st.session_state.page == 7:

        if user is not None and index != -1:

            # The Title
            st.title('Welcome to our application')
            st.write('Here’s a quick guide on how to navigate the application.')

            # Header Number 1
            with st.container(border=True):
                st.header('Signing In')
                st.write('To sign in, enter your unique 10-digit code ', user['Passcode'],
                         ' into the Passcode field on the login section on the initial page.')

            # Header Number 2
            with st.container(border=True):
                st.header('Daily Stress Questionnaire')
                st.write('Every day, you’ll need to fill out a questionnaire to rate your daily stress.')
                st.write('You only need to complete this once per day, not every time you log in.')

            # Header Number 3
            with st.container(border=True):
                st.header('Recommendations')
                st.write(
                    'Based on your Stress Questionnaire answers and the number of suggestions you choose, you will receive recommendations on the Home page.')
                st.write(
                    'To complete a recommendation and earn points click the button with the :material/done_outline: icon next to it.')
                st.write(
                    'To mark your favorites click the button with the :material/favorite: icon next to the recommendation you like.')
                st.write(
                    'To avoid future suggestions click the button with the :material/heart_broken: icon next to the recommendation you don’t want to see again.')
                st.write(
                    'To remove any of the :material/favorite: or :material/heart_broken: registration click the button with the :material/delete: icon.')
                st.write(
                    'That option is available at the Home page or the ‘Profile and Preferences’ page at the navigation menu.')
                st.write('To see a recommendation in detail click the :material/open_in_full: button next to it.')
                st.write(
                    'If you want new recommendations create a New Status by clicking ‘Make New Status’ in the navigation menu and answer the Stress Questionnaire again.')

            # Header Number 4
            with st.container(border=True):
                st.header('Scores and Levels')
                st.write('You earn points by completing recommendations. Every Monday, your score will determine:')
                st.write('Whether you move up to a new level.')
                st.write('Whether you stay at your current level.')
                st.write('Whether you are demoted to a lower level.')
                st.write(
                    'You can track your progress and check when the next level assessment is on the home page. After each assessment your score will reset to 0.')
                st.write(
                    'Your level affects how many points you earn per recommendation and the scores needed to advance or get demoted.')

            # Header Number 5
            with st.container(border=True):
                st.header('Your Preferences')
                st.write(
                    'Go to the ‘Profile and Preferences’ page in the navigation menu to view your profile and preferences.')
                st.write('See the recommendations you have marked as favorites or not favorites.')
                st.write(
                    'Adjust your preferences and follow the instructions on the page to filter the types of recommendations you want to see.')
                st.write('To navigate the results by keeping track of the samples next to the results:')
                st.write('Look for the :material/badge: icon to find a recommendation given to you.')
                st.write('Look for the :material/done_outline: icon to find a completed recommendation.')
                st.write('Look for the :material/heart_broken: icon to find a removed recommendation.')
                st.write('Look for the :material/favorite: icon to find a favorite recommendation.')
                st.write(
                    'Look for the :material/delete: icon to remove a recommendation from the :material/heart_broken: or :material/favorite: category.')
                st.write('Click on the :material/open_in_full: icon to open the recommendation in full.')

            # Header Number 6
            with st.container(border=True):
                st.header('Your Record')
                st.write('Click the ‘See Record’ button in the navigation menu to view your application history.')
                st.write(
                    'Filter by categories and follow the instructions on the page to track specific actions you’ve taken in the app.')

            # Header Number 7
            with st.container(border=True):
                st.header('Confessions')
                st.write(
                    "Feel like journaling? Click in the 'Make a confession' page in the navigation menu and make a confession.")
                st.write(
                    'You will also be able to manage your confessions on that page. To delete a confession click on the button with the :material/delete: icon.')

            st.write('We hope this helps you navigate the app with ease! Let us know if you need further assistance.')

        else:
            st.write('Something went wrong, user not found.')

    elif st.session_state.page == 8:

        if user is not None and index != -1:

            # The Title
            con_question = 'Want to take something off your chest? Make a confession!'
            st.title(con_question)

            # The New Confession Section
            with st.container(border=True):
                st.header(f"Tell us what's on your mind {user['Username']}!")
                answer = st.text_area("", height=300)
                disclaimer = st.checkbox(
                    "I have not entered any identifying or sensitive information such as full names or banking information.")
                st.button("Enter confession", icon=":material/draw:", use_container_width=True,
                          on_click=record_question,
                          args=[con_question, answer, st.session_state.current_passcode, disclaimer],
                          key="add_confession_button_1")

            # The Table
            st.header("Your previous confessions:")
            data = list(Question.find({"Passcode": st.session_state.current_passcode, "Question": con_question}))

            if len(data) == 0:
                st.write("You haven't entered any confessions yet")
            elif len(data) == 1:
                st.write("You have made 1 confession")
            else:
                st.write(f"You have made {len(data)} confessions")

            pointer = 1
            for entry in data:
                with st.container(border=True):
                    column151, column152, column153, column154 = st.columns([1, 2, 4, 0.5])
                    with column151:
                        st.write(pointer)
                    with column152:
                        st.write(entry['Created_At'])
                    with column153:
                        st.write(entry['Answer'])
                    with column154:
                        st.button('', icon=":material/delete:", use_container_width=True,
                                  on_click=delete_entry,
                                  args=[st.session_state.current_passcode, entry['Question'], None, entry['Created_At'],
                                        "Question", st.session_state.current_passcode],
                                  key=f"delete_confession_button_{pointer}")
                pointer += 1
        else:
            st.write('Something went wrong, user not registered.')

    elif st.session_state.page == 9:

        if user is not None and index != -1 and user['Role'] != 'User':

            # The Title
            st.title('Add Recommendations and Tags')

            # The recommendation section
            st.header('Add a recommendation')

            question_about_passcode = "User Passcode"
            question_about_recommendation_id = "Recommendation ID"
            question_about_points = "Points"
            question_about_title = "Title"
            question_about_description = "Description"
            question_about_link = "Link - optional"

            # The recommendation input
            with st.container(border=True):

                column161, column162, column163 = st.columns([2, 2, 2])
                with column161:
                    your_passcode = st.text_input(question_about_passcode, key="your_passcode",
                                                  value=st.session_state.current_passcode, disabled=True)
                with column162:
                    this_generated_id = st.text_input(question_about_recommendation_id, key="recommendation_id",
                                                      value=generate_recommendation_id(), disabled=True)
                with column163:
                    points = st.number_input(question_about_points, min_value=10, max_value=150)

                title = st.text_input(question_about_title, key="title")
                description = st.text_area(question_about_description, height=300, key="description")

                column164, column165 = st.columns([4, 3])
                with column164:
                    link_input = st.text_input(question_about_link, key="link")
                with column165:
                    link_condition = st.checkbox(
                        "Include link - User takes full responsibility that the link has been verified and is secure")
                link = None
                if link_condition:
                    link = link_input

                st.button('Add Recommendation', icon=":material/fact_check:", use_container_width=True,
                          on_click=add_recommendation_here,
                          args=[your_passcode, this_generated_id, points, title, description, link,
                                question_about_recommendation_id, question_about_points, question_about_title,
                                question_about_description, question_about_link],
                          key="add_recommendation_entry_button")

            # The tag section

            if Recommendation.count_documents({}) >= 1:

                st.header('Add a tag')

                your_passcode_1 = st.text_input(question_about_passcode, key="your_passcode_X",
                                                value=st.session_state.current_passcode, disabled=True)

                # Stress level
                with st.container(border=True):

                    column171, column172, column173, column174 = st.columns([2, 2, 2, 0.5])

                    with column171:
                        st.write("Add a stress level tag")
                    with column172:
                        recommendation_id = st.number_input(question_about_recommendation_id, min_value=1, key="cat_1")
                    with column173:
                        stress_level = st.number_input("Stress Level", min_value=min_limit,
                                                       max_value=Recommendation.count_documents({}))
                    with column174:
                        st.button('', icon=":material/check:", use_container_width=True,
                                  on_click=add_tag_here,
                                  args=[recommendation_id, your_passcode_1, "Stress Level", stress_level,
                                        question_about_recommendation_id],
                                  key="add_stress_level_tag_button")

                # Time Available
                with st.container(border=True):
                    column181, column182, column183, column184 = st.columns([2, 2, 2, 0.5])

                    with column181:
                        st.write("Add a time available tag")
                    with column182:
                        recommendation_id_1 = st.number_input(question_about_recommendation_id, min_value=1, key="cat_2")
                    with column183:
                        time_available = st.number_input("Time Available", min_value=min_limit,
                                                         max_value=max_limit)
                    with column184:
                        st.button('', icon=":material/check:", use_container_width=True,
                                  on_click=add_tag_here,
                                  args=[recommendation_id_1, your_passcode_1, "Time Available", time_available,
                                        question_about_recommendation_id],
                                  key="add_time_available_tag_button")

                # Focus Area
                with st.container(border=True):
                    column1121, column1122, column1123, column1124 = st.columns([2, 2, 2, 0.5])

                    with column1121:
                        st.write("Add a focus area tag")
                    with column1122:
                        recommendation_id_3 = st.number_input(question_about_recommendation_id, min_value=1, key="cat_3")
                    with column1123:
                        focus_area = st.radio("Focus Area", (
                            "Work/Career", "Finances", "Health & Well-being", "Relationships", "Time Management",
                            "Personal Identity",
                            "Major Life Changes", "Social Media & Technology", "Uncertainty & Future Planning"))
                    with column1124:
                        st.button('', icon=":material/check:", use_container_width=True,
                                  on_click=add_tag_here,
                                  args=[recommendation_id_3, your_passcode_1, "Focus Area", focus_area,
                                        question_about_recommendation_id],
                                  key="add_focus_area_tag_button")

                # Age Variant
                with st.container(border=True):
                    column191, column192, column193, column194 = st.columns([2, 2, 2, 0.5])

                    with column191:
                        st.write("Add a age variant tag")
                    with column192:
                        recommendation_id_2 = st.number_input(question_about_recommendation_id, min_value=1, key="cat_4")
                    with column193:
                        age_variant = st.radio("Age Variant", ("18-25", "26-35", "36-55", "56-70", "70+"))
                    with column194:
                        st.button('', icon=":material/check:", use_container_width=True,
                                  on_click=add_tag_here,
                                  args=[recommendation_id_2, your_passcode_1, "Age Variant", age_variant,
                                        question_about_recommendation_id],
                                  key="add_age_variant_tag_button")

            else:
                st.write('There are no recommendation in the data base')

        elif user is not None and index != -1:
            st.write('You do not have access to this page')
        else:
            st.write('Something went wrong, user not found.')

    else:
        st.write('You are on page ', st.session_state.page)





