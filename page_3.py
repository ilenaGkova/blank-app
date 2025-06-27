import streamlit as st  # Streamlit Software
from initialise_variables import initialize_variables, max_additional_recommendations  # Application Function
from application_actions import get_record, determine_level_change  # Database Function
from mongo_connection import User, Score_History, Status  # Database Function
from generate_recommendations_main import get_recommendations, generate_recommendation  # Database Function
from initialise_variables import max_recommendation_limit  # Application Function
from structure_recommendation_table import make_recommendation_table  # Database Function
from change_page import change_page, open_recommendation  # Application Function
from generate_items import get_limits  # Database Function
from datetime import datetime, timedelta  # Other
import plotly.graph_objects as go  # Visual Elements
import pandas as pd  # Visual Elements
import altair as alt  # Visual Elements
from page_7 import summary

if 'page' not in st.session_state:
    st.session_state.page = 1  # Will set the layout the application will open

if 'current_passcode' not in st.session_state:
    st.session_state.current_passcode = 1  # Will register the user operating the application

if 'error' not in st.session_state:
    st.session_state.error = ''  # Will store error logs for functions called

if 'error_status' not in st.session_state:
    st.session_state.error_status = None  # Will indicate whether there is an error to show

if 'open_recommendation' not in st.session_state:
    st.session_state.open_recommendation = -1  # Will select a recommendation to open in full


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
    df = pd.DataFrame(list(Score_History.find({"Passcode": st.session_state.current_passcode})))

    # Create a color mapping for Outcome
    # The colors are Red for score that gets demoted, green for promoted score and blue for sustaining score
    # Here we are not creating the dots just setting the colors
    df['Color'] = df['Outcome'].map({True: 'green', False: 'red', None: 'blue'})  # Create color mapping as before

    # Calculate promotion/demotion scores
    result = list(zip(*df['Level'].apply(get_limits)))
    df['Promotion_Score'] = result[0]
    df['Demotion_Score'] = result[1]

    # Extract date and time components
    df['Date'] = pd.to_datetime(df['Created_At']).dt.date
    df['Time'] = pd.to_datetime(df['Created_At']).dt.time

    hover = alt.selection_single(
        fields=["Created_At"],
        nearest=True,
        on="mouseover",  # This is correct for Streamlit
        empty="none",
    )  # Sets the baseline that is the date the score number was recorded based on the Created_At field if the Collection

    # Create column-based chart
    dots = alt.Chart(df).mark_circle(size=100).encode(
        x=alt.X('Date:T', title='Date', axis=alt.Axis(format='%b %d, %Y')),  # Use date as x-axis (categorical)
        y=alt.Y('Score:Q', title='Performance Score'),  # Use score for y-axis
        order=alt.Order('Time:T', sort='descending'),
        color=alt.Color('Color:N', scale=None),  # Color based on outcome
        # The tooltip is what the user see when they hover on a dot
        # The letters used mean Q for numeric value and T for date and time
        # Other letter not used are N for categories / names and O for ordered data
        # The values before the letters are the attributes created in the df table we are showing
        # The Titles are what the user sees
        tooltip=[
            alt.Tooltip('Score:Q', title='Performance Score'),
            alt.Tooltip('Level:Q', title='Difficulty Level'),
            alt.Tooltip('Promotion_Score:Q', title='Promotion Score'),
            alt.Tooltip('Demotion_Score:Q', title='Demotion Score'),
            alt.Tooltip('Date:T', title='Date', format='%b %d, %Y'),  # Date separately
            alt.Tooltip('Time:T', title='Time', format='%H:%M:%S'),  # Time separately
        ]
    ).add_selection(hover)

    lines = alt.Chart(df).mark_line().encode(
        x='Date:T',
        y='Score:Q',
        order=alt.Order('Created_At:T')  # Connect points in chronological order
    )

    chart_for_score_history = dots + lines

    return chart_for_score_history


def add_recommendation_to_user():  # Called when the user wants to see another recommendation

    st.session_state.error_status, st.session_state.error = generate_recommendation(
        st.session_state.current_passcode)  # Will update the session error variables and maybe increase the user's score if appropriate

    if st.session_state.error_status:  # Warning: The status variable is in reverse

        change_page(st.session_state.page)  # Will change the page to itself to reload and see the result


def layout_3():
    user, today, yesterday, index, recommendation = initialize_variables(st.session_state.current_passcode,
                                                                         st.session_state.open_recommendation)

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

        if int(user['Days_Summed']) == 1:
            summary(st.session_state.current_passcode)

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

                            if entry_for_user_recommendation_generated_list_with_recommendations['Outcome']:  # Mirrors how the recommendation_per_person stores recommendation outcomes as boolean values with True being default

                                st.markdown(
                                    f"<div style='text-align: center;'>Complete this and gain {user['Level'] * entry_for_user_recommendation_generated_list_with_recommendations['Points']} points!</div>",
                                    unsafe_allow_html=True)

                            else:

                                st.markdown(
                                    f"<div style='text-align: center;'>Task completed for {user['Level'] * entry_for_user_recommendation_generated_list_with_recommendations['Points']} points!</div>",
                                    unsafe_allow_html=True)

                        st.button("", icon=":material/open_in_full:", use_container_width=True,
                                  on_click=open_recommendation, args=[entry_for_user_recommendation_generated_list_with_recommendations['ID']],
                                  key=f"open_user_recommendation_generated_list_with_recommendations_{pointer_for_user_recommendation_generated_list_with_recommendations}")

                    pointer_for_user_recommendation_generated_list_with_recommendations += 1

                # Users are ask initially for up to 1/4 of the number of recommendations in the Recommendation collection
                # After the get their initial recommendations they can request 1/10 more of the number of recommendations in the Recommendation collection

                if len(user_recommendation_generated_list_with_recommendations) < max_recommendation_limit + max_additional_recommendations:
                    st.button("", icon=":material/add_task:", use_container_width=True,
                              on_click=add_recommendation_to_user,
                              args=[],
                              key="add_a_recommendation_to_user")  # User clicks here to get a new additional recommendation
