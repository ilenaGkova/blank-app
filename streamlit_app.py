import streamlit as st

# Configuration Command

st.set_page_config(
    page_title="StressTest",
    page_icon="👋",
)

# Additional Imports
import plotly.graph_objects as go  # Needs to be downloaded
import pandas as pd  # Needs to be downloaded
import altair as alt  # Needs to be downloaded
from datetime import datetime, timedelta
from streamlit_cookies_controller import CookieController  # Needs to be downloaded
from Tables import Recommendations, Tags, Users  # Import from files
from mongo_connection import add_points, change_recommendation_preference_for_user, determine_level_change, \
    generate_animal_username, generate_unique_passcode, get_limits, get_recommendations, get_record, get_status, \
    init_connection, make_recommendation_table, record_status, update_user_streak, validate_user, new_user, \
    record_question, create_history, delete_entry, create_recommendation_history, update_user, add_recommendation, \
    add_tag, generate_recommendation, add_question_to_Questionnaire, insert_data, \
    return_collections, generate_recommendation_id, get_maximum_entries  # Import from files

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
    st.session_state.error_status = None  # Will indicate whether there is an error to show

if "username" not in st.session_state:
    st.session_state.username = generate_animal_username()  # Will store temporary username so user can sign up without generating a new one each time they select an option

if 'answers' not in st.session_state:
    st.session_state.answers = {}  # Will store answers to the Daily Stress Questioner

# Part B: The Global But Not Session Variables

# Step 1: Get collections. This happens via function, so we don't have to establish any connection here, on this file

User, Recommendation, Tag, Question_Questionnaire, Score_History, Question, Status = return_collections()

# The majority of the function alterations are done in the mongo file.
# The above database collections are initialized here and used exclusively for find and count_document actions in the mongo database

# Step 2: Initialise collections with data if needed

# Moved to other file

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

# The below variables are used in various pages

min_time_limit = 3  # The minimum time limit a user will enter as time available
min_limit = 1  # The general minimum limit a user can enter
max_limit = 20  # The general maximum limit a user can enter
stress_max_limit = 10  # The general maximum limit a user can enter when rating stress
max_recommendation_limit, max_additional_recommendations = get_maximum_entries()  # The amount te recommendations the user can ask

# Inputs for questions

question_username = "What's your username?"
question_age = "Age"
question_focus_area = "Where would you like to focus?"
question_time_available = f"How many minutes are you willing to spend in reducing stress ({min_time_limit} - {max_limit})?"
question_suggestions = f"How many tasks do you want to try daily ({min_limit} - {max_recommendation_limit})?"
question_passcode = "What's your passcode?"


# Part C: The Functions

def change_page(new_page):  # This function will change the page

    st.session_state.page = new_page  # By changing the page number we change the layout
    st.session_state.error_status = True  # Will reset the status of the error message, so it doesn't follow the user


# Layouts and numbers assigned
# 1 is the page where the user makes a new account or signs in with their passcode
# 2 is the page where the user can answer questions about stress levels
# 3 is the home page where the user can see and complete recommendations
# 4 is the profile and preferences page where the user can update their profile and manage their preferences
# 5 is the Record page where the user can see their application history
# 6 is the page where the user can see a recommendation in full
# 7 is the tutorial page where the user can see how the application works
# 8 is the page where the user can make a confession and manage their confessions
# 9 is the page where an admin can add entries to the collections of the database


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


def catalog_question(question, answer, passcode1):  # Called for each question in the Daily Stress Questionnaire

    record_question(question, answer, passcode1)  # We need record the answer the user gave to a question everytime the user enters something in a field or selects an answer out of a radio button

    # Depending on the answer the stress level will rise by 0, 1 or 2
    if answer == "Good":
        return 0
    elif answer == "Neutral":
        return 1
    return 2


def make_status(
        user_stress_level):  # Called when the user makes a status by answering questions about their stress level

    st.session_state.error_status, st.session_state.error = record_status(st.session_state.current_passcode,
                                                                          user_stress_level)  # Will update the session error variables and maybe create new status for user if appropriate

    if st.session_state.error_status:  # Warning: The status variable is in reverse

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

    return f"{days_until_sunday} Days {hours:02} Hours {minutes:02} Minutes and {seconds:02} Seconds"  # Will return time remaining repeated


def add_recommendation_to_user():  # Called when the user wants to see another recommendation

    st.session_state.error_status, st.session_state.error = generate_recommendation(
        st.session_state.current_passcode)  # Will update the session error variables and maybe increase the user's score if appropriate

    if st.session_state.error_status:  # Warning: The status variable is in reverse

        change_page(st.session_state.page)  # Will change the page to itself to reload and see the result


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


def add_question(ID, passcode_for_question, question_input, question_for_question_input, question_for_id):
    st.session_state.error_status, st.session_state.error = add_question_to_Questionnaire(ID, passcode_for_question,
                                                                                          question_input)  # Will update the session error variables and maybe add a recommendation if appropriate

    if st.session_state.error_status:  # Warning: The status variable is in reverse

        # We need record the answer the user gave to a question everytime the user enters something in a field or selects an answer out of a radio button
        record_question(question_for_id, ID, passcode_for_question)
        record_question(question_for_question_input, question_input, passcode_for_question)

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


def create_store_history_graph():  # Called to make a graph of the score history of a user

    # Below we will get data from a collection and create a table to make a graph out of
    # The new table df will start with
    # Passcode - We will show only the passcodes matching out user
    # Score - The user's score
    # Level - The user's level at the time
    # Outcome - Either True if score will promote user to next level False if ot will demote them or None for anything else
    # Created_At - When it was recorded
    # These were from the collection. Through calculations, we will add 3 more attributes
    # Color - Will dictate the color of the dot created for the entry depending on the outcome
    # Promotion_Score - Will tell us the promotion point depending on the level
    # Demotion_Score - Will tell us the demotion point depending on the level

    df = pd.DataFrame(list(Score_History.find({
        "Passcode": st.session_state.current_passcode})))  # Convert dictionary list that comes from the user's score history to DataFrame

    # Create a color mapping for Outcome
    # The colors are Red for score that gets demoted, green for promoted score and blue for sustaining score
    # Here we are not creating the dots just setting the colors

    df['Color'] = df['Outcome'].map({True: 'green', False: 'red', None: 'blue'})

    result = list(zip(*df['Level'].apply(get_limits)))
    df['Promotion_Score'] = result[0]
    df['Demotion_Score'] = result[1]

    hover = alt.selection_single(
        fields=["Created_At"],
        nearest=True,
        on="mouseover",
        empty="none",
    )  # Sets the baseline that is the date the score number was recorded based on the Created_At field if the Collection

    # Create the baseline chart with custom field names
    # The tooltip is what the user see when they hover on a dot
    # The letters used mean Q for numeric value and T for date and time
    # Other letter not used are N for categories / names and O for ordered data
    # The values before the letters are the attributes created in the df table we are showing
    # The Titles are what the user sees

    base = alt.Chart(df).encode(
        x=alt.X('Created_At:T', title='Date'),
        y=alt.X('Score:Q', title='Performance Score'),
        tooltip=[
            alt.Tooltip('Score:Q', title='Performance Score'),
            alt.Tooltip('Level:Q', title='Difficulty Level'),
            alt.Tooltip('Promotion_Score:Q', title='Promotion Score'),
            alt.Tooltip('Demotion_Score:Q', title='Demotion Score'),
            alt.Tooltip('Created_At:T', title='Date and Time')
        ]
    )

    line = base.mark_line()  # Create a line to connect all scores

    dots = base.mark_circle(size=100).encode(
        color=alt.Color('Color:N', scale=None)  # Here we created the dots of the scores
    ).add_selection(hover)  # Create points with colors based on Outcome

    chart_for_score_history = line + dots  # Combine the line and points

    return chart_for_score_history


# Part D: The layouts

# Step 1: Show the error if needed

if st.session_state.error_status is not None and not st.session_state.error_status:
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
# 9 is the page where an admin can add entries to the collections of the database

# Layout logistics

# There is a conditional statement. Depending on the number of the st.session_state.page value different assets will be generated.
# Each asset however needs their own quick name to be identified.

# Except page 1 every page needs a valid user to be signed in. Pages 1 and 2 are the only pages that don't require a status to be made by the user and page 6 needs a valid recommendation number.
# The above conditions are initialised in Part B Step 4 every time the page loads.

# From now on any button needs a distinct key, it will be found as the key="XXX" in the button parameters, input fields are the same
# Buttons have other parameters like on_click= XXXXX is the function called when the button is clicked or args = [XXXXX, YYYYY] are the parameters of the function

# Text can be show either by a streamlit option, st.write/header/title... or use html in st.markdown. Both are utilised here.

# Users enter information is text fields, number fields, checkboxes and radio buttons.
# Text fields need to get information when the user presses enter, number fields need limits, checkboxes will return True or False and radio buttons will have a preselected choice unless specified.
# Each type of text input prompt will tell the user what to do to save their answer, thought it might be small in letters.

# Any command st. is a streamlit layout asset. Any command that starts with 'with XXXXX' will put the assets under it in the asset.
# Here that is used to put things in columns and putting things in a square.

# Database collection function
# When a user wants to delete and entry in any collection the Record Collection makes a new entry
# Record Collection keeps other things recorded as well and assigns a letter in an action
# Question Collection records every prompt the user enters as a question
# A tag with the same Recommendation ID, Title and Category will not be entered twice
# Look at the mongo file for more information

# Warning
# The database and the variable names refer to recommendations.
# The texts shown to the user use the word task.
#
insert_data()  # Insert default data if needed

if st.session_state.page == 1:  # 1 is the page where the user makes a new account or signs in with their passcode

    # The SideBar - User Signs In With Passcode

    st.sidebar.header('Already have an account? Sign in!')

    passcode = st.sidebar.text_input(question_passcode, key="passcode", value=st.session_state.previous_passcode)

    st.sidebar.button('Log in', use_container_width=True, on_click=log_in_user, args=[passcode, question_passcode],
                      key="sign_in_user")

    # The Title

    st.title('Wellcome to Stressless Living!')

    st.header(
        'If you have an account sign in on the left - find the :material/arrow_forward_ios: icon to find the sign in form.')

    st.write("New here? Please answer the following questions and we'll create your account.")

    # The Initial Questions Section

    if Recommendation.count_documents(
            {}) >= 1:  # The application won't sign on new users if there are no recommendations to be given

        with st.container(border=True):  # Add a square around the section to seperate

            # Step 1: User enters a username - randomly generated at first

            user_username = st.text_input(question_username, key="user_username", value=st.session_state.username)

            if user_username != st.session_state.username:
                st.session_state.username = user_username  # Save the username the user gave to avoid generating another later

            # Step 2: Generate a password randomly with 10 digits

            user_passcode = generate_unique_passcode()

            # Step 3: User enters an Age category and focus area to personalise the experience

            age = st.radio(question_age, ("18-25", "26-35", "36-55", "56-70", "70+"))

            focus_area = st.radio(question_focus_area, (
                "Work/Career", "Finances", "Health & Well-being", "Relationships", "Time Management",
                "Personal Identity",
                "Major Life Changes", "Social Media & Technology", "Uncertainty & Future Planning"))

            # Step 4: User enters their free time amount and the amount of suggestion they wish to see

            time_available = st.number_input(question_time_available, min_value=min_time_limit, max_value=max_limit)

            suggestions = st.number_input(question_suggestions, min_value=min_limit,
                                          max_value=max_recommendation_limit)  # Set maximum at the amount of suggestions available

            # Step 5: User clicks button to create an account

            st.button('Let us get started', use_container_width=True, on_click=create_user,
                      args=[user_username, user_passcode, age, focus_area, time_available, suggestions,
                            question_username,
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

            st.sidebar.button('Skip', on_click=change_page, args=[3], use_container_width=True, key="skip")

        # The Title

        st.title(f"Hello {user['Username']}")
        """Please answer the Daily Stress Questioner"""

        # The Daily Question Section

        questionnaire_list = Question_Questionnaire.find()  # Get the questioner questions

        for entry in questionnaire_list:

            key = f"Question_{entry['ID']}"  # Make a unique key for each input field.

            # For each question we will have a slider for the user to answer
            st.select_slider(
                entry['Question'],
                options=["Bad", "Neutral", "Good"],
                key=key
            )

            st.session_state.answers[entry['Question']] = st.session_state[key]  # Store the answer to the question via the key

        if st.button("Submit", key="make_status"):  # Step 2: Click button to submit answers

            # Create a list of question-answer pairs
            question_answer_pairs = [(question, answer) for question, answer in st.session_state.answers.items()]

            stress_level = 0  # Set Stress Level as 0, so we can add to it

            for question, answer in question_answer_pairs:

                stress_level += catalog_question(question, answer, st.session_state.current_passcode)  # Record the question-answer pairs and increase the stress level

            make_status(stress_level)  # Submit to final stress level to move on

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
    # 9 is the page where an admin can add entries to the collections of the database

    st.sidebar.markdown(f"<div style='text-align: center;font-size: 20px; font-weight: bold;'>Navigation Menu</div>",
                        unsafe_allow_html=True)

    st.sidebar.write("")  # Add blank line

    if user is not None and index != -1 and user['Role'] == 'User':  # Users have a more limited menu than an admin

        st.sidebar.button("Home", icon=":material/home:", use_container_width=True, on_click=change_page, args=[3],
                          key="main_page")
        st.sidebar.button("Profile and Preferences", icon=":material/person_3:", use_container_width=True,
                          on_click=change_page, args=[4], key="profile_page")
        st.sidebar.button("Daily Stress Questionnaire", icon=":material/add:", use_container_width=True,
                          on_click=change_page,
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
        st.sidebar.button("Daily Stress Questionnaire", icon=":material/add:", use_container_width=True,
                          on_click=change_page,
                          args=[2], key="status_page_admin")
        st.sidebar.button("See Record", icon=":material/clinical_notes:", use_container_width=True,
                          on_click=change_page, args=[5], key="record_page_admin")
        st.sidebar.button('Add Data to Stress Test Database', icon=":material/add_circle:", use_container_width=True,
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

            show_streak, show_days_connected = st.columns([2, 2])  # Show the information side by side

            with show_streak:

                with st.container(border=True):  # Add a square around the section to seperate them

                    st.markdown(
                        f"<div style='text-align: center;font-size: 40px;font-weight: bold; margin-top: 0'>{user['Streak']}</div>",
                        unsafe_allow_html=True)

                    st.markdown(
                        f"<div style='text-align: center;font-size: 20px; margin-bottom: 30px'>Consecutive Days connected</div>",
                        unsafe_allow_html=True)

            with show_days_connected:

                with st.container(border=True):  # Add a square around the section to seperate them

                    st.markdown(
                        f"<div style='text-align: center;font-size: 40px;font-weight: bold; margin-top: 0'>{user['Days_Summed']}</div>",
                        unsafe_allow_html=True)

                    st.markdown(
                        f"<div style='text-align: center;font-size: 20px; margin-bottom: 30px'>Days connected</div>",
                        unsafe_allow_html=True)

            # Section 2: User Score and Level

            st.subheader('Your Level / Score')

            with st.container(border=True):

                # Step 1: Check if the level or score need to be altered

                if get_record(st.session_state.current_passcode):  # Levels and scores are altered 1 a week
                    st.header(determine_level_change(st.session_state.current_passcode))  # Will do the alteration
                    user = User.find_one(
                        {"Passcode": st.session_state.current_passcode})  # Will update the user after the alteration

                # Step 2: Show level and score

                show_level, show_score = st.columns([1, 5])  # Show the information side by side

                with show_level:
                    st.markdown(
                        f"<div style='text-align: center;font-size: 20px;'>Level</div>",
                        unsafe_allow_html=True)

                    st.markdown(
                        f"<div style='text-align: center;font-size: 60px;font-weight: bold;'>{user['Level']}</div>",
                        unsafe_allow_html=True)

                with show_score:
                    # Depending on the lever the promotion/demotion points are different
                    # See the mongo file for more

                    up, down = get_limits(user['Level'])

                    # Create the slider to show the user score, promotion and demotion points

                    fig = create_custom_slider(0, up + 50, down, up, user['Score'])
                    st.plotly_chart(fig, use_container_width=True)

                # Step 3: Show message

                st.markdown(
                    f"<div style='text-align: left;'>Next level assessments in {get_time()}. Stay above the demotion score to remain to this level or reach the advancement score to move up!</div>",
                    unsafe_allow_html=True)

            if Score_History.count_documents(
                    {"Passcode": st.session_state.current_passcode}) >= 1:  # Only make graph when you have data

                see_score_history = st.checkbox(
                    "See your Score history")  # See score history graph, only show she when there are data to show

                if see_score_history:  # and the user want to see it

                    st.altair_chart(create_store_history_graph(),
                                    use_container_width=True)  # Display the score history graph when the user has results and wants it

            # For new user, add a message to direct them to the tutorial and give them the rundown of managing the recommendations they are given

            if Status.count_documents({"Passcode": st.session_state.current_passcode}) == 1:
                with st.container(border=True):
                    st.header('New here? Here is how you can navigate our task table!')

                    st.write('Remember the number ', user['Passcode'],
                             ' to sign in again after you close the application')

                    st.write('Click :material/done_outline: to complete a task')
                    st.write('Click :material/thumb_up: to mark your favorites')
                    st.write('Click :material/thumb_down: to avoid future tasks')
                    st.write(
                        'Click :material/delete: to remove any of the :material/thumb_up: or :material/thumb_down: registration of a task')
                    st.write('Click the :material/open_in_full: to see a recommendation in detail')

                    st.write("Want another task? Click on the 'Get another task' button under the tasks given to you")

                    st.write(
                        "Check out our tutorial to better navigate the rest of the application! You will locate it in our navigation menu on your left.")

            # Section 3: The daily recommendations

            st.subheader('Our task list for you today')

            user_recommendation_generated_list_build, user_recommendation_generated_list, user_recommendation_generated_list_message = get_recommendations(
                st.session_state.current_passcode)  # Step 1: Create the recommendation table based on the user's information

            st.write(
                user_recommendation_generated_list_message)  # Write the result of the function above, see mongo file for more

            if user_recommendation_generated_list_build:  # This will tell us if the list was made or not

                user_recommendation_generated_list_with_recommendations_built, user_recommendation_generated_list_with_recommendations = make_recommendation_table(
                    user_recommendation_generated_list,
                    st.session_state.current_passcode)  # Step 2: Structure the recommendation table in a way that is helpful

                if user_recommendation_generated_list_with_recommendations_built:

                    # Step 3: Assuming nothing went wrong we can show the table

                    pointer_for_user_recommendation_generated_list_with_recommendations = 1  # Serves as unique identifier for the buttons

                    for entry_for_user_recommendation_generated_list_with_recommendations in user_recommendation_generated_list_with_recommendations:

                        with (st.container(border=True)):  # Puts a border around each entry to seperate

                            # Each column is named after the content it shows

                            column_for_pointer, column_for_title_or_description = st.columns([0.2, 5])

                            with column_for_pointer:

                                st.markdown(
                                    f"<div style='text-align: center;'>{pointer_for_user_recommendation_generated_list_with_recommendations}</div>",
                                    unsafe_allow_html=True)

                            with column_for_title_or_description:

                                st.markdown(
                                    f"<div style='text-align: center; font-weight: bold;'>{entry_for_user_recommendation_generated_list_with_recommendations['Title']}</div>",
                                    unsafe_allow_html=True)

                                if len(entry_for_user_recommendation_generated_list_with_recommendations[
                                           'Description']) > 150:  # If description is big enough it won't show. It can be shown by extending the recommendation to full screen

                                    st.markdown(
                                        "<div style='text-align: center;'>Open Task to see description</div>",
                                        unsafe_allow_html=True)
                                else:

                                    st.markdown(
                                        f"<div style='text-align: center;'>{entry_for_user_recommendation_generated_list_with_recommendations['Description']}</div>",
                                        unsafe_allow_html=True)

                                # Depending on the outcome the user either sees the points the recommendation curies or what they completed it

                                if entry_for_user_recommendation_generated_list_with_recommendations[
                                        'Outcome']:  # Mirrors how the recommendation_per_person stores recommendation outcomes as boolean values with True being default

                                    st.markdown(
                                        f"<div style='text-align: center;'>Complete this and gain {user['Level'] * entry_for_user_recommendation_generated_list_with_recommendations['Points']} points!</div>",
                                        unsafe_allow_html=True)

                                else:

                                    st.markdown(
                                        f"<div style='text-align: center;'>Task completed for {user['Level'] * entry_for_user_recommendation_generated_list_with_recommendations['Points']} points!</div>",
                                        unsafe_allow_html=True)

                            # Each column is named after the content it shows

                            column_for_outcome, column_for_extension_button, column_for_reference_1, column_for_reference_2 = st.columns(
                                [5, 2, 0.5, 0.5])

                            # Preference indicates if the recommendation is in the favorite/removed or no section for this user.
                            # Depending on that the user will see a different combination of buttons
                            # A recommendation can't be both in the favorite and removed section. To be in one it will be removed from the other.

                            with column_for_outcome:

                                if entry_for_user_recommendation_generated_list_with_recommendations['Outcome']:  # Mirrors how the recommendation_per_person stores recommendation outcomes

                                    st.button("", icon=":material/done_outline:", use_container_width=True,
                                              on_click=completed_recommendation,
                                              args=[entry_for_user_recommendation_generated_list_with_recommendations[
                                                        'ID'],
                                                    entry_for_user_recommendation_generated_list_with_recommendations[
                                                        'Status_Created_At']],
                                              key=f"complete_open_user_recommendation_generated_list_with_recommendations_{pointer_for_user_recommendation_generated_list_with_recommendations}")

                            with column_for_extension_button:

                                st.button("", icon=":material/open_in_full:", use_container_width=True,
                                          on_click=open_recommendation, args=[
                                        entry_for_user_recommendation_generated_list_with_recommendations['ID']],
                                          key=f"open_user_recommendation_generated_list_with_recommendations_{pointer_for_user_recommendation_generated_list_with_recommendations}")

                            with column_for_reference_1:

                                if entry_for_user_recommendation_generated_list_with_recommendations[
                                        'Preference'] is False:
                                    st.button("", icon=":material/thumb_up:", use_container_width=True,
                                              on_click=change_recommendation_status, args=[1,
                                                                                           entry_for_user_recommendation_generated_list_with_recommendations[
                                                                                               'ID']],
                                              key=f"love_open_user_recommendation_generated_list_with_recommendations_{pointer_for_user_recommendation_generated_list_with_recommendations}")

                                if entry_for_user_recommendation_generated_list_with_recommendations[
                                        'Preference'] is True:
                                    st.button("", icon=":material/delete:", use_container_width=True,
                                              on_click=change_recommendation_preference_for_user,
                                              args=[1, st.session_state.current_passcode,
                                                    entry_for_user_recommendation_generated_list_with_recommendations[
                                                        'ID'], True],
                                              key=f"remove_recommendation_open_user_recommendation_generated_list_with_recommendations_{pointer_for_user_recommendation_generated_list_with_recommendations}_x")

                                if entry_for_user_recommendation_generated_list_with_recommendations[
                                        'Preference'] is None:
                                    st.button("", icon=":material/thumb_up:", use_container_width=True,
                                              on_click=change_recommendation_status, args=[1,
                                                                                           entry_for_user_recommendation_generated_list_with_recommendations[
                                                                                               'ID']],
                                              key=f"love_open_user_recommendation_generated_list_with_recommendations_{pointer_for_user_recommendation_generated_list_with_recommendations}_y")

                            with column_for_reference_2:

                                if entry_for_user_recommendation_generated_list_with_recommendations[
                                        'Preference'] is False:
                                    st.button("", icon=":material/delete:", use_container_width=True,
                                              on_click=change_recommendation_preference_for_user,
                                              args=[1, st.session_state.current_passcode,
                                                    entry_for_user_recommendation_generated_list_with_recommendations[
                                                        'ID'], True],
                                              key=f"remove_recommendation_open_user_recommendation_generated_list_with_recommendations_{pointer_for_user_recommendation_generated_list_with_recommendations}")

                                if entry_for_user_recommendation_generated_list_with_recommendations[
                                        'Preference'] is True:
                                    st.button("", icon=":material/thumb_down:", use_container_width=True,
                                              on_click=change_recommendation_status, args=[-1,
                                                                                           entry_for_user_recommendation_generated_list_with_recommendations[
                                                                                               'ID']],
                                              key=f"hate_open_user_recommendation_generated_list_with_recommendations_{pointer_for_user_recommendation_generated_list_with_recommendations}_x")

                                if entry_for_user_recommendation_generated_list_with_recommendations[
                                        'Preference'] is None:
                                    st.button("", icon=":material/thumb_down:", use_container_width=True,
                                              on_click=change_recommendation_status, args=[-1,
                                                                                           entry_for_user_recommendation_generated_list_with_recommendations[
                                                                                               'ID']],
                                              key=f"hate_open_user_recommendation_generated_list_with_recommendations_{pointer_for_user_recommendation_generated_list_with_recommendations}_y")

                        pointer_for_user_recommendation_generated_list_with_recommendations += 1

                    # Users are ask initially for up to 1/4 of the number of recommendations in the Recommendation collection
                    # After the get their initial recommendations they can request 1/10 more of the number of recommendations in the Recommendation collection

                    if len(user_recommendation_generated_list_with_recommendations) < max_recommendation_limit + max_additional_recommendations:
                        st.button("Add A Task", icon=":material/add_task:", use_container_width=True,
                                  on_click=add_recommendation_to_user,
                                  args=[],
                                  key="add_a_recommendation_to_user")  # User clicks here to get a new additional recommendation

    elif st.session_state.page == 4:  # 4 is the profile and preferences page where the user can update their profile and manage their preferences

        if user is not None and index != -1:

            # Section 1: The User Profile and Update Profile Function

            # The Title

            st.title('Your Profile')

            # The Profile Information

            with st.container(border=True):

                # This section will show the user their information and change it by putting in their new information and click a button
                # The text labels are shared from page 1

                column_for_username, column_for_passcode = st.columns(
                    [3, 3])  # Each column is named after the attribute if the user it shows

                column_for_age, column_for_focus_area = st.columns(
                    [3, 3])  # Each column is named after the attribute if the user it shows

                column_for_time_available, column_for_number_of_suggestions, column_for_repeat = st.columns(
                    [2, 2, 2])  # Each column is named after the attribute if the user it shows

                with column_for_username:
                    update_username = st.text_input(question_username, key="update_username", value=user['Username'])

                with column_for_passcode:
                    update_passcode = st.text_input("Your Passcode - Not available for Alteration",
                                                    key="update_passcode", value=user['Passcode'], disabled=True)

                with column_for_age:
                    update_age = st.radio(question_age, ("18-25", "26-35", "36-55", "56-70", "70+"))

                    st.write('Current Age Category: ', user[
                        'Age_Category'])  # For radio button entries I can't preselect the user data, so I am adding them below

                with column_for_focus_area:
                    update_focus_area = st.radio(question_focus_area, (
                        "Work/Career", "Finances", "Health & Well-being", "Relationships", "Time Management",
                        "Personal Identity",
                        "Major Life Changes", "Social Media & Technology", "Uncertainty & Future Planning"))

                    st.write('Current Focus Area: ', user[
                        'Focus_Area'])  # For radio button entries I can't preselect the user data, so I am adding them below

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
                    update_repeat = st.number_input(
                        f"You will not see the same task in (choose below) days",
                        min_value=min_limit, max_value=7,
                        value=user['Repeat_Preference'])  # Limits for each number input are shared from page 1

                st.write("")  # Add a blank line for space

                st.write(
                    "Warning: by clicking the button below will update every field of your profile, make sure you are altering only the fields you wish to alter")  # Add a disclaimer for the user

                st.button("Save Alterations", icon=":material/save_as:", use_container_width=True,
                          on_click=update_user_here,
                          args=[update_username, update_passcode, update_age, update_focus_area,
                                update_time_available, update_suggestions, update_repeat,
                                question_username,
                                question_age, question_focus_area, question_time_available, question_suggestions,
                                f"You will not see the same task in (choose below) days"],
                          key="update_user_button")  # When user clicks here the information they have entered will update every field of theo user profile

            # Section 2: User Preferences for Tasks

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

                                    elif entry_for_list_of_recommendations_based_on_filter_given_by_user[
                                            'Outcome']:  # The below are in the Recommendation_per_person Collection

                                        st.header(
                                            ':material/badge:')  # Category given, mirrors how the recommendation_per_person stores recommendation outcomes, default for incomplete recommendations is True

                                    else:

                                        st.header(
                                            ':material/badge: :material/done_outline:')  # Category given, complete recommendations

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

    elif st.session_state.page == 5:  # 5 is the Record page where the user can see their application history

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

                    if user['Role'] != 'User':
                        recommendation_status = st.checkbox(
                            "See what tasks you have entered")  # Include Recommendation Collection

                with column_for_tag_category:

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

    elif st.session_state.page == 6:  # 6 is the page where the user can see a recommendation in full

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

                        st.write(recommendation['Description'])  # Show the description

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

        elif recommendation is None:

            st.session_state.error_status = False
            st.session_state.error = f"Something went wrong, Recommendation with ID number {st.session_state.open_recommendation} not found."

    elif st.session_state.page == 7:  # 7 is the tutorial page where the user can see how the application works

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

    elif st.session_state.page == 8:  # 8 is the page where the user can make a confession and manage their confessions

        if user is not None and index != -1:

            # The Title

            # We save title in a variable to record the confession as a question
            # To record a question we need a question, an answer and a passcode
            # We also search when by the question in the question collection to show the user their previous confessions
            # We don't show any other kind of questions in this page

            con_question = 'Want to take something off your chest? Make a confession!'

            st.title(con_question)

            # Section 1: The New Confession

            with st.container(border=True):  # Put a square around this to seperate from anything else

                st.header(f"Tell us what's on your mind {user['Username']}!")  # Tell the user what to do

                answer = st.text_area("",
                                      height=300)  # Warning: Alike other input text filed this type need control+enter to save the new information

                # This application is not very private.
                # We add a disclaimer to warn the user to keep their information private
                # Putting it in text makes it easy to ignore, so it's a checkbox instead

                disclaimer = st.checkbox(
                    "I have not entered any identifying or sensitive information such as full names or banking information.")

                # Usually record question takes 3 variables: passcode, question and answer
                # Only this time we also sent the disclaimer as a forth
                # See the mongo file for more information

                st.button("Enter confession", icon=":material/draw:", use_container_width=True,
                          on_click=record_question,
                          args=[con_question, answer, st.session_state.current_passcode, disclaimer],
                          key="add_confession_button_in_page")

            # Section 2: The Older Confessions

            # The Title

            st.header("Your previous confessions:")

            data = list(Question.find({"Passcode": st.session_state.current_passcode,
                                       "Question": con_question}))  # Search for only this question in the question collection

            # Depending on the number of confessions, we show different messages before listing them

            if len(data) == 0:

                st.write("You haven't entered any confessions yet")

            elif len(data) == 1:

                st.write("You have made 1 confession")

            else:

                st.write(f"You have made {len(data)} confessions")

            pointer_for_confessions = 1  # Pointer works as unique identifier of the button and separates the confessions for the user

            for entry in data:
                with st.container(border=True):  # Box each entry to seperate them

                    column_for_pointer_for_confession, column_for_timestamp_for_confession, column_for_confession, column_for_delete_confession_button = st.columns(
                        [1, 2, 4, 0.5])  # Columns are named after the content they show

                    with column_for_pointer_for_confession:
                        st.write(pointer_for_confessions)  # Show pointer so seperate confessions

                    with column_for_timestamp_for_confession:
                        st.write(entry['Created_At'])  # When the confession was made

                    with column_for_confession:
                        st.write(entry['Answer'])  # Show the confession

                    with column_for_delete_confession_button:
                        # We use a generalised function that takes a collection name, some key information and deletes an entry from the collection
                        # For the Question Collection we need the question, the user, and the time created to delete the entry

                        st.button('', icon=":material/delete:", use_container_width=True,
                                  on_click=delete_entry,
                                  args=[st.session_state.current_passcode, entry['Question'], None, entry['Created_At'],
                                        "Question", st.session_state.current_passcode],
                                  key=f"delete_confession_button_{pointer_for_confessions}")

                pointer_for_confessions += 1

    elif st.session_state.page == 9:  # 9 is the page where an admin can add entries to the collections of the database

        if user is not None and index != -1 and user['Role'] != 'User':

            # The Title

            st.title('Add Entries to DataBase')

            # Section 1: Add a Recommendation

            # The Title

            st.header('Add a recommendation')

            # Step 1: Initialising the prompts, so we can record the questions later

            question_about_passcode = "User Passcode"
            question_about_recommendation_id = "Recommendation ID"
            question_about_points = "Points (10-150)"
            question_about_title = "Title"
            question_about_description = "Description"
            question_about_link = "Link - optional"

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

                with column_for_point_for_new_recommendation:

                    # The minimum points a recommendation can get is 10 points
                    # The maximum points is 150 which is the cap points for a user in level 1

                    points = st.number_input(question_about_points, min_value=10, max_value=150)

                # Part 2: The recommendation

                title = st.text_input(question_about_title, key="title")  # Recommendation title

                description = st.text_area(question_about_description, height=300,
                                           key="description")  # Warning: Alike other input text filed this type need control+enter to save the new information

                # Part 3: The Recommendation Link

                column_for_url_link, column_for_url_link_disclaimer = st.columns(
                    [4, 3])  # Columns are named after the Recommendation information they show

                with column_for_url_link:
                    link_input = st.text_input(question_about_link,
                                               key="link")  # This is a link the user will be able to go and see more information

                with column_for_url_link_disclaimer:
                    link_condition = st.checkbox(
                        "Include link - User takes full responsibility that the link has been verified and is secure")  # This disclaimer makes the user think to check the link before entering it

                link = None

                if link_condition:  # You only get the link included if you have checked the checkbox

                    link = link_input

                # Step 3: Add the recommendation
                # To add the recommendation the user needs to click this button
                # The function it calls is a local one that will add the recommendation and record the questions

                st.button('Add Recommendation', icon=":material/fact_check:", use_container_width=True,
                          on_click=add_recommendation_here,
                          args=[your_passcode_for_recommendation, this_generated_id, points, title, description, link,
                                question_about_recommendation_id, question_about_points, question_about_title,
                                question_about_description, question_about_link],
                          key="add_recommendation_entry_button")

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

                        focus_area = st.radio("Focus Area", (
                            "Work/Career", "Finances", "Health & Well-being", "Relationships", "Time Management",
                            "Personal Identity",
                            "Major Life Changes", "Social Media & Technology",
                            "Uncertainty & Future Planning"))  # Options match the ones given to user

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

                        age_variant = st.radio("Age Variant", (
                            "18-25", "26-35", "36-55", "56-70", "70+"))  # Options match the ones given to user

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
                        [2, 4, 0.5])  # Columns named after the content they show

                    with column_for_level_tag_title:  # Write the kind of tag the user is entering

                        level_variant = st.radio("Tag Name", (
                            "Show for levels above", "Show for levels below", "Show for levels equal"))  # Options match the ones given to user

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

            else:

                # You can't add tags to a recommendation-less database

                st.session_state.error_status = False
                st.session_state.error = 'There are no recommendations in the data base'

            # Section 3: Questions in Daily Stress Questionnaire

            # The Title

            st.header('Add a Question')

            with st.container(border=True):  # Seperate this section from the others

                column_for_question_ID, column_for_user_passcode = st.columns(
                    [4, 4])  # Columns named after the content they show

                with column_for_question_ID:
                    # This is auto field by finding and ID that is not in the Questionnaire collection and can't change
                    # Warning: While this is a text input the text in converted into a number before being entered with the recommendation

                    Question_ID = "Question ID"  # Saved separately to be used in function

                    this_generated_id = st.text_input(Question_ID, key="question_id",
                                                      value=generate_question_id(),
                                                      disabled=True)  # This ID is generated on the spot

                with column_for_user_passcode:  # This is set as the current user's passcode, and it can't be changed

                    your_passcode_for_question = st.text_input(question_about_passcode,
                                                               key="your_passcode_for_question",
                                                               value=st.session_state.current_passcode,
                                                               disabled=True)

                question_input = "Question"  # Saved separately to be used in function

                question = st.text_area(question_input, height=100,
                                        key="question")  # Warning: Alike other input text filed this type need control+enter to save the new information

                st.button('Add Question To Daily Stress Questionnaire', icon=":material/question_mark:",
                          use_container_width=True,
                          on_click=add_question,
                          args=[this_generated_id, your_passcode_for_question, question, question_input, Question_ID],
                          key="add_question_entry_button")

        elif user is not None and index != -1:

            st.session_state.error_status = False
            st.session_state.error = 'You do not have access to this page'

    else:

        # If for any reason a number more than 9 is called we show message with the number
        # This should never realistically happen

        st.write('You are on page ', st.session_state.page)





