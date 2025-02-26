import streamlit as st

# Configuration Command

st.set_page_config(
    page_title="StressTest",
    page_icon="👋",
)

# Part A: The Initial Session Variables

if "page" not in st.session_state:
    st.session_state.page = 1

if "current_passcode" not in st.session_state:
    st.session_state.current_passcode = 1

if "open_recommendation" not in st.session_state:
    st.session_state.open_recommendation = -1

if 'previous_passcode' not in st.session_state:
    st.session_state.previous_passcode = ''

# Part B: The Imports

import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_cookies_controller import CookieController
from Tables import Recommendations, Tags, Users
from mongo_connection import add_points, change_recommendation_preference_for_user, determine_level_change, \
    generate_animal_username, generate_unique_passcode, get_limits, get_recommendations, get_record, get_status, \
    init_connection, make_recommendation_table, record_status, update_user_streak, validate_user, new_user, \
    record_question, create_history, delete_entry, create_recommendation_history, update_user

if "username" not in st.session_state:
    st.session_state.username = generate_animal_username()

# Part C: The Functions

client = init_connection()
db = client.StressTest
User = db["User"]
Tag = db["Tag"]
Recommendation = db["Recommendation"]
Question = db["Question"]
Status = db["Status"]
if not User.find_one({"Username": "Admin"}):
    User.insert_many(Users)
if not Tag.find_one({"ID": 1}):
    Tag.insert_many(Tags)
if not Recommendation.find_one({"ID": 1}):
    Recommendation.insert_many(Recommendations)

controller = CookieController()
cookies = controller.getAll()
st.session_state.previous_passcode = cookies.get("previous_user_passcode", "")

user = User.find_one({"Passcode": st.session_state.current_passcode})
today, yesterday, index = get_status(st.session_state.current_passcode)
recommendation = Recommendation.find_one({"ID": st.session_state.open_recommendation})
question_username = "What's your username?"
question_age = "Age"
question_focus_area = "Where would you like to focus?"
question_time_available = "How much time are you willing to spend in reducing stress?"
question_suggestions = "How many suggestions do you want?"
question_passcode = "What's your passcode?"
min_limit = 1


def change_page(new_page): st.session_state.page = new_page


def set_username(passcode_for_setting_username):
    st.session_state.current_passcode = passcode_for_setting_username
    today_for_setting_username, yesterday_for_setting_username, index_for_setting_username = get_status(
        st.session_state.current_passcode)
    if index_for_setting_username == -1:
        change_page(2)
    elif today_for_setting_username:
        change_page(3)
    else:
        change_page(2)


def log_in_user(passcode_for_signing_in_user, question_passcode_for_log_in_user):
    move_on, message_for_signing_in_user = validate_user(passcode_for_signing_in_user)
    if not move_on:
        st.sidebar.write(message_for_signing_in_user)
    else:
        controller.set("previous_user_passcode", str(passcode_for_signing_in_user))
        record_question(question_passcode_for_log_in_user, passcode_for_signing_in_user, passcode_for_signing_in_user)
        set_username(passcode_for_signing_in_user)


def create_user(user_user_username, user_user_passcode, user_age, user_focus_area, user_time_available,
                user_suggestions, question_username_for_create_user, question_age_for_create_user,
                question_focus_area_for_create_user, question_time_available_for_create_user,
                question_suggestions_for_create_user, question_passcode_for_create_user):
    move_on, message_for_signing_up_user = new_user(user_user_username, user_user_passcode, user_age, user_focus_area,
                                                    user_time_available, user_suggestions)
    if not move_on:
        st.sidebar.write(message_for_signing_up_user)
    else:
        controller.set("previous_user_passcode", str(user_user_passcode))
        record_question(question_username_for_create_user, user_user_username, passcode)
        record_question(question_passcode_for_create_user, user_user_passcode, passcode)
        record_question(question_age_for_create_user, user_age, passcode)
        record_question(question_focus_area_for_create_user, user_focus_area, passcode)
        record_question(question_time_available_for_create_user, user_time_available, passcode)
        record_question(question_suggestions_for_create_user, user_suggestions, passcode)
        set_username(user_user_passcode)


def make_status(user_stress_level):
    if user is not None:
        move_on, message_for_make_status = record_status(st.session_state.current_passcode, user_stress_level)
        if not move_on:
            st.sidebar.write(message_for_make_status)
        else:
            record_question(question_stress_level, user_stress_level, st.session_state.current_passcode)
            change_page(3)


def create_custom_slider(min_value, max_value, down_barrier, up_barrier, score):
    scale = go.Figure()
    scale.add_shape(type="line", x0=min_value, y0=0, x1=max_value, y1=0, line=dict(color="RoyalBlue", width=4))
    scale.add_trace(go.Scatter(
        x=[down_barrier],
        y=[0],
        mode="markers",
        marker=dict(size=15, color="red"),
        name="Demotion Point",
        hovertemplate="Demotion Point: %{x}<extra></extra>"
    ))
    scale.add_trace(go.Scatter(
        x=[up_barrier],
        y=[0],
        mode="markers",
        marker=dict(size=15, color="green"),
        name="Promotion Point",
        hovertemplate="Promotion Point: %{x}<extra></extra>"
    ))
    scale.add_trace(go.Scatter(
        x=[score],
        y=[0],
        mode="markers",
        marker=dict(size=15, color="RoyalBlue"),
        name="Your Score",
        hovertemplate="Your Score: %{x}<extra></extra>"
    ))
    scale.update_layout(
        height=150,
        xaxis=dict(range=[min_value, max_value], title=None),
        yaxis=dict(visible=False, range=[-1, 1]),
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="white",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x"
    )
    return scale


def get_time():
    now = datetime.now()
    days_until_sunday = (6 - now.weekday()) % 7
    next_sunday_midnight = (now + timedelta(days=days_until_sunday)).replace(hour=23, minute=59, second=59,
                                                                             microsecond=999999)
    time_remaining = next_sunday_midnight - now
    hours, remainder = divmod(time_remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days_until_sunday}:{hours:02}:{minutes:02}:{seconds:02}"


def completed_recommendation(index_for_completed_recommendation, status):
    condition_for_completed_recommendation = add_points(index_for_completed_recommendation,
                                                        st.session_state.current_passcode, status)
    if condition_for_completed_recommendation:
        change_page(3)


def change_recommendation_status(preference, index_for_change_recommendation_status):
    condition_for_change_recommendation_status = change_recommendation_preference_for_user(preference,
                                                                                           st.session_state.current_passcode,
                                                                                           index_for_change_recommendation_status)
    if condition_for_change_recommendation_status:
        change_page(st.session_state.page)


def update_user_here(new_username, passcode_for_update_employee, new_age, new_focus_area, new_time_available,
                     new_suggestions, new_repeat, question_username_for_update_user, question_age_for_update_user,
                     question_focus_area_for_update_user, question_time_available_for_update_user,
                     question_suggestions_for_update_user, repeat_question):
    move_on, message_for_update_user = update_user(passcode_for_update_employee, new_username, new_repeat, new_age,
                                                   new_focus_area,
                                                   new_time_available, new_suggestions)
    if move_on:
        record_question(question_username_for_update_user, new_username, passcode_for_update_employee)
        record_question(question_age_for_update_user, new_age, passcode_for_update_employee)
        record_question(question_focus_area_for_update_user, new_focus_area, passcode_for_update_employee)
        record_question(question_time_available_for_update_user, new_time_available, passcode_for_update_employee)
        record_question(question_suggestions_for_update_user, new_suggestions, passcode_for_update_employee)
        record_question(repeat_question, new_repeat, passcode_for_update_employee)
        change_page(st.session_state.page)
    else:
        st.write(message_for_update_user)


def open_recommendation(index_for_open_recommendation):
    st.session_state.open_recommendation = index_for_open_recommendation
    change_page(6)


# Part D: The layouts

if st.session_state.page == 1:

    # The SideBar - User Signs In With Passcode
    st.sidebar.write('Already have an account? Sign it!')
    question_passcode = "What's your passcode?"
    passcode = st.sidebar.text_input(question_passcode, key="passcode", value=st.session_state.previous_passcode)
    st.sidebar.button('Log in', on_click=log_in_user, args=[passcode, question_passcode], key="sign_in_user")

    # The Title
    """
    # Wellcome to Stress Test!
    Please answer the following questions and we'll create your account
    """

    # The Initial Questions Section
    if Recommendation.count_documents({}) >= 1:

        user_username = st.text_input(question_username, key="user_username", value=st.session_state.username)
        if user_username != st.session_state.username:
            st.session_state.username = user_username
        user_passcode = generate_unique_passcode()
        age = st.radio(question_age, ("18-25", "26-35", "36-55", "56-70", "70+"))
        focus_area = st.radio(question_focus_area, (
            "Work/Career", "Finances", "Health & Well-being", "Relationships", "Time Management", "Personal Identity",
            "Major Life Changes", "Social Media & Technology", "Uncertainty & Future Planning"))
        time_available = st.number_input(question_time_available, min_value=min_limit, max_value=20)
        suggestions = st.number_input(question_suggestions, min_value=min_limit,
                                      max_value=Recommendation.count_documents({}))
        st.button('Let us get started', on_click=create_user,
                  args=[user_username, user_passcode, age, focus_area, time_available, suggestions, question_username,
                        question_age, question_focus_area, question_time_available, question_suggestions,
                        question_passcode], key="create_user")

elif st.session_state.page == 2:

    # The SideBar - User Information
    if user is not None:
        st.sidebar.write(update_user_streak(user['Passcode']))
        st.sidebar.write('Username:', user['Username'])
        st.sidebar.write('Focus Area:', user['Focus_Area'])
        st.sidebar.write('Number of Suggestions:', user['Suggestions'])
        st.sidebar.write('Time Available:', user['Time_Available'])
        st.sidebar.write('Days Connected:', user['Days_Summed'])
        st.sidebar.write('Streak:', user['Streak'])
        st.sidebar.write("Don't show me the same suggestion for ", user['Repeat_Preference'], ' day(s) after')
        if today:
            st.sidebar.button('Skip', on_click=change_page, args=[3], key="skip")
    else:
        st.sidebar.write('Something went wrong, user not registered.')

    # The Title
    if user is not None:
        st.title(f"Hello {user['Username']}")
        """Please answer the questions below"""
    else:
        st.write('Something went wrong, user not registered.')

    # The Daily Question Section
    min_limit = 1
    max_limit = 10
    question_stress_level = "How would you rate your stress level?"
    stress_level = st.number_input(question_stress_level, min_value=min_limit, max_value=max_limit)
    st.button('Let us get started', on_click=make_status, args=[stress_level], key="make_status")

elif 3 <= st.session_state.page <= 9:

    # The Menu
    st.sidebar.markdown(f"<div style='text-align: center;font-size: 20px; font-weight: bold;'>Navigation Menu</div>",
                        unsafe_allow_html=True)
    st.sidebar.write("")
    if user is not None and not index == -1 and user['Role'] == 'User':
        st.sidebar.button("Home", icon=":material/home:", use_container_width=True, on_click=change_page, args=[3],
                          key="main_page")
        st.sidebar.button("Profile and Preferences", icon=":material/person_3:", use_container_width=True,
                          on_click=change_page, args=[4], key="profile_page")
        st.sidebar.button("Make New Status", icon=":material/add:", use_container_width=True, on_click=change_page,
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
    elif user is not None and not index == -1:
        st.sidebar.button("Home", icon=":material/home:", use_container_width=True, on_click=change_page, args=[3],
                          key="main_page_admin")
        st.sidebar.button("Profile and Preferences", icon=":material/person_3:", use_container_width=True,
                          on_click=change_page, args=[4], key="profile_page_admin")
        st.sidebar.button("Make New Status", icon=":material/add:", use_container_width=True, on_click=change_page,
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
        st.write('Something went wrong, user not registered.')
    else:
        st.sidebar.write('Something went wrong, status not found.')

    if st.session_state.page == 3:

        # The Title
        if user is not None:
            st.markdown(
                f"<div style='text-align: center;font-size: 60px;font-weight: bold;'>Hello {user['Username']}, we are happy to see you!</div>",
                unsafe_allow_html=True)
        else:
            st.write('Something went wrong, user not registered.')

        # The Score
        if user is not None:

            with st.container(border=True):
                column141, column142 = st.columns([2, 2])
                with column141:
                    st.markdown(
                        f"<div style='text-align: center;font-size: 30px;'>Streak</div>",
                        unsafe_allow_html=True)
                    st.markdown(
                        f"<div style='text-align: center;font-size: 60px;font-weight: bold;'>{user['Streak']}</div>",
                        unsafe_allow_html=True)
                with column142:
                    st.markdown(
                        f"<div style='text-align: center;font-size: 30px;'>Days connected</div>",
                        unsafe_allow_html=True)
                    st.markdown(
                        f"<div style='text-align: center;font-size: 60px;font-weight: bold;'>{user['Days_Summed']}</div>",
                        unsafe_allow_html=True)

            st.subheader('Your Level / Score')

            with st.container(border=True):
                if get_record(st.session_state.current_passcode):
                    st.header(determine_level_change(st.session_state.current_passcode))
                    user = User.find_one({"Passcode": st.session_state.current_passcode})
                column1, column2 = st.columns([0.2, 2])
                with column1:
                    st.markdown(
                        f"<div style='text-align: center;font-size: 60px;font-weight: bold;'>{user['Level']}</div>",
                        unsafe_allow_html=True)
                with column2:
                    up, down = get_limits(user)
                    fig = create_custom_slider(0, up + 50, down, up, user['Score'])
                    st.plotly_chart(fig, use_container_width=True)
            st.markdown(
                f"<div style='text-align: left;'>Next level assessments in {get_time()}. Stay above the demotion score to remain to this level or reach the advancement score to move up!</div>",
                unsafe_allow_html=True)
        else:
            st.write('Something went wrong, user not registered.')

        if Status.count_documents({"Passcode": st.session_state.current_passcode}) == 1:
            st.header("New here? Check out our tutorial to better navigate this application! You will locate it in our navigation menu on your left.")

        # The Recommendations
        st.subheader('Our recommendations for you today')
        condition, user_recommendations, message = get_recommendations(st.session_state.current_passcode)
        st.write(message)

        if condition:

            condition, user_recommendations = make_recommendation_table(user_recommendations,
                                                                        st.session_state.current_passcode)
            if condition:
                for entry in user_recommendations:
                    with (st.container(border=True)):
                        column13, column23, column33, column53, column63 = st.columns([0.2, 2, 1, 0.5, 0.5])
                        with column13:
                            st.markdown(f"<div style='text-align: center;'>{entry['Pointer']}</div>",
                                        unsafe_allow_html=True)
                        with column23:
                            st.markdown(f"<div style='text-align: center; font-weight: bold;'>{entry['Title']}</div>",
                                        unsafe_allow_html=True)
                            if len(entry['Description']) > 150:
                                st.markdown(
                                    "<div style='text-align: center;'>Open Recommendation to see description</div>",
                                    unsafe_allow_html=True)
                            else:
                                st.markdown(f"<div style='text-align: center;'>{entry['Description']}</div>",
                                            unsafe_allow_html=True)
                        with column33:
                            if entry['Outcome']:
                                st.markdown(
                                    f"<div style='text-align: center;'>Complete this and gain {user['Level'] * entry['Points']}!</div>",
                                    unsafe_allow_html=True)
                            else:
                                st.markdown(
                                    f"<div style='text-align: center;'>Recommendation completed {entry['Completed_At']}!</div>",
                                    unsafe_allow_html=True)
                        with column53:
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
                        with column63:
                            if entry['Outcome']:
                                st.button("", icon=":material/done_outline:", use_container_width=True,
                                          on_click=completed_recommendation,
                                          args=[entry['ID'], entry['Status_Created_At']],
                                          key=f"complete_{entry['Pointer']}")
                            st.button("", icon=":material/open_in_full:", use_container_width=True,
                                      on_click=open_recommendation, args=[entry['ID']], key=f"open_{entry['Pointer']}")
            else:
                st.write('Something went wrong, recommendations not found.')

    elif st.session_state.page == 4:

        if user is not None:

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
                    update_time_available = st.number_input(question_time_available, min_value=min_limit, max_value=20,
                                                            value=user['Suggestions'])
                with column138:
                    update_suggestions = st.number_input(question_suggestions, min_value=min_limit,
                                                         max_value=Recommendation.count_documents({}),
                                                         value=user['Time_Available'])
                with column139:
                    update_repeat = st.number_input(
                        f"You will not see tha same suggestion in {user['Repeat_Preference']} days",
                        min_value=min_limit, max_value=20,
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

        if user is not None:

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
                                with column58:
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

        if recommendation is not None and user is not None:

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
                            st.write({entry['Title_Of_Criteria']}, ': ', {entry['Category']}, 'as assigned by, ', User.find_one({"Passcode": entry['Passcode']})['Username'])

        elif recommendation:
            st.write('Something went wrong, user not found.')
        elif user:
            st.write('Something went wrong, recommendation not found.')
        else:
            st.write('Something went wrong, user and recommendation not found.')

    elif st.session_state.page == 7:

        if user is not None:

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
                st.write("Feel like journaling? Click in the 'Make a confession' page in the navigation menu and make a confession.")
                st.write('You will also be able to manage your confessions on that page. To delete a confession click on the button with the :material/delete: icon.')

            st.write('We hope this helps you navigate the app with ease! Let us know if you need further assistance.')

        else:
            st.write('Something went wrong, user not found.')

    elif st.session_state.page == 8:

        if user is not None:

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
                                  args=[st.session_state.current_passcode, entry['Question'], None, entry['Created_At'], "Question", st.session_state.current_passcode],
                                  key="add_confession_button")
        else:
            st.write('Something went wrong, user not registered.')

    else:
        st.write('You are on page ', st.session_state.page)
else:
    st.write('You are on page ', st.session_state.page)




