from check_and_balance import get_status
from generate_items import get_maximum_entries
from mongo_connection import User, Recommendation


def initialize_variables(current_passcode, open_recommendation):
    user = User.find_one(
        {"Passcode": current_passcode})  # Will be the user using the application currently
    today, yesterday, index = get_status(
        current_passcode)  # Will tell us if the user needs to make a status today
    recommendation = Recommendation.find_one(
        {"ID": open_recommendation})  # Will tell us if the user picked a recommendation to open

    return user, today, yesterday, index, recommendation


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
focus_areas = "Work/Career", "Finances", "Health & Well-being", "Relationships", "Time Management", "Personal Identity", "Major Life Changes", "Social Media & Technology", "Uncertainty & Future Planning"
ages = "18-25", "26-35", "36-55", "56-70", "70+"
genders = "Male", "Female", "Other"
options = {
    "Not happened": 0,
    "Happened rarely": 1,
    "Happened sometimes": 2,
    "Happened often": 3,
    "Happened very often": 4
}
con_question = 'Want to take something off your chest? Make a confession!'

question_about_passcode = "User Passcode"
question_about_recommendation_id = "Recommendation ID"
question_about_points = "Points (10-150)"
question_about_title = "Title"
question_about_description = "Description"
question_about_link = "Link - optional"

Question_ID = "Question ID"  # Saved separately to be used in function
question_input = "Question"  # Saved separately to be used in function

