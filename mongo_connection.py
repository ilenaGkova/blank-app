from datetime import datetime, timedelta
import random
import pymongo
import streamlit as st
from Tables import Users, Tags, Recommendations


@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets["mongo"]["uri"])


client = init_connection()
db = client.StressTest
Status = db["Status"]
User = db["User"]
Question = db["Question"]
Record = db["Record"]
Recommendation_Per_Person = db["Recommendation_Per_Person"]
Tag = db["Tag"]
Recommendation = db["Recommendation"]
Removed_Recommendation = db["Removed_Recommendation"]
Favorite_Recommendation = db["Favorite"]
Question_Questionnaire = db["Questionnaire"]
Score_History = db["Score_History"]

if not User.find_one({"Username": "Admin"}):
    User.insert_many(Users)
if not Tag.find_one({"ID": 1}):
    Tag.insert_many(Tags)
if not Recommendation.find_one({"ID": 1}):
    Recommendation.insert_many(Recommendations)


# Start Page Function
def validate_user(passcode):
    if not passcode.strip():
        return False, "You need to enter your passcode"
    user = User.find_one({"Passcode": passcode})
    if user is None:
        return False, "You do not have an account"
    Record.insert_one(
        {
            'Passcode': passcode,
            'Action': f"User {passcode} signed in.",
            'Type': "I",
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    return True, "You have an account"


# Start Page Function
def new_user(username, passcode, age, focus_area, time_available, suggestions):
    if not username.strip() or passcode == "Please reload the page" or not age.strip() or not focus_area.strip() or time_available == 0 or suggestions == 0:
        return False, "You need to fill in all fields provided to proceed. If Passcode not available reload the page."
    if User.find_one({"Username": username}):
        return False, "You need to enter a unique username"
    if User.find_one({"Passcode": passcode}):
        return False, "Something went wrong, please reload the page and try again"
    User.insert_one(
        {
            'Username': username,
            'Passcode': passcode,
            'Repeat_Preference': 1,
            'Age_Category': age,
            'Focus_Area': focus_area,
            'Suggestions': suggestions,
            'Time_Available': time_available,
            'Level': 1,
            'Score': 0,
            'Streak': 0,
            'Days_Summed': 0,
            'Role': 'User',
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    Score_History.insert_one(
        {
            'Passcode': passcode,
            'Score': 0,
            'Level': 1,
            'Outcome': False,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    Record.insert_many(
        [
            {
                'Passcode': passcode,
                'Action': f"User {passcode} created their profile: Username {username}, Repeat Preference {1}, Age {age}, focus {focus_area}, suggestions {suggestions}, time available {time_available}",
                'Type': "H",
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                'Passcode': passcode,
                'Action': f"User {passcode} has had their score set to 0",
                'Type': "D",
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
    )
    return True, "You have been added to our service"


# Start Page Function
def generate_unique_passcode(max_attempts=100):
    attempt_count = 0
    all_collections = [
        "Status", "User", "Question", "Record", "Recommendations_Per_Person",
        "Tag", "Recommendation", "Removed_Recommendation", "Favorite_Recommendation"
    ]
    while attempt_count < max_attempts:
        passcode = str(random.randint(1000000000, 9999999999))
        passcode_exists = False
        for collection_name in all_collections:
            collection = db[collection_name]  # Get the collection
            if collection.find_one({"Passcode": passcode}):
                passcode_exists = True
                break
            if not passcode_exists:
                return passcode
        attempt_count += 1
    return "Please reload the page"


# Start Page Function
def generate_animal_username(max_attempts=100):
    attempt_count = 0
    animals = ['Lion', 'Tiger', 'Elephant', 'Giraffe', 'Zebra', 'Panda', 'Koala', 'Kangaroo', 'Cheetah', 'Penguin']
    adjectives = ['Fluffy', 'Mighty', 'Sneaky', 'Grumpy', 'Mysterious', 'Sleepy', 'Bold', 'Spiky', 'Shiny', 'Wild']
    while attempt_count < max_attempts:
        username = f"{random.choice(adjectives)}{random.choice(animals)}#{random.randint(1000, 9999)}"
        if not User.find_one({"Username": username}):
            return username
        attempt_count += 1
    return "Please reload the page"


# Start/Status Page Function       
def record_question(question, answer, passcode, function=None):
    if function is not None:
        if not answer.strip() or not question.strip() or function is False:
            return False, "Question failed to be recorded"
    Question.insert_one(
        {
            'Passcode': passcode,
            'Question': question,
            'Answer': answer,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    return True, "Question recorded"


# Status/Main Page Function
def get_status(passcode):
    latest_status = Status.find_one({"Passcode": passcode}, sort=[("Created_At", -1)])
    if not latest_status:
        return False, False, -1
    last_status_time = datetime.strptime(latest_status['Created_At'], '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    return (now.date() == last_status_time.date()), ((now.date() - last_status_time.date()).days == 1), latest_status[
        "_id"]


# Status Page Function
def record_status(passcode, stress_level):
    if stress_level == 0:
        return False, "You need to fill in all fields provided to proceed"
    else:
        if not User.find_one({"Passcode": passcode}):
            return False, "Something went wrong, user not registered."
        Status.insert_one(
            {
                'Passcode': passcode,
                'Stress_Level': stress_level,
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
        return True, "Status recorded"


# Status Page
def update_user_streak(passcode):
    last_record = Record.find_one({"Passcode": passcode, "Type": "B"},
                                  sort=[("Created_At", -1)])
    if last_record:
        last_time = datetime.strptime(last_record["Created_At"], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        if last_time.date() == now.date():
            return "You have already signed in today, your streak will not change."
    if not User.find_one({"Passcode": passcode}):
        return "Something went wrong, user not registered."
    User.update_one({"Passcode": passcode}, {"$inc": {"Days_Summed": 1}})
    today, yesterday, index = get_status(passcode)
    if yesterday:
        User.update_one({"Passcode": passcode}, {"$inc": {"Streak": 1}})
        message = "Your streak was increased."
        streak_action = f"Streak increased for user {passcode}"
    else:
        User.update_one({"Passcode": passcode}, {"$set": {"Streak": 1}})
        if index == -1:
            message = "Wellcome to your first Status."
        else:
            message = "You did not check in less than 48 hours ago. Your streak was reset."
        streak_action = 'Streak reset'
    Record.insert_many(
        [
            {
                'Passcode': passcode,
                'Action': streak_action,
                'Type': "A",
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                'Passcode': passcode,
                'Action': f"Days connected increased for user {passcode}",
                'Type': "B",
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
    )
    return message


# Main page side side function
def calculate_fail_count():
    number_of_recommendations_in_total = Recommendation.count_documents({})
    last_entry_added = Recommendation.find_one({}, sort=[('ID', -1)])
    max_ID = last_entry_added['ID']
    total_possible_IDs = max_ID
    number_of_recommendation_after_removing_deleted_entries = total_possible_IDs - number_of_recommendations_in_total
    return int(total_possible_IDs / (
            number_of_recommendations_in_total - number_of_recommendation_after_removing_deleted_entries))


# Main page side function
def generate_valid_index():
    recommendation_fail = 0
    potential_recommendation_index = random.randint(1, Recommendation.count_documents({}))
    while Recommendation.find_one(
            {"ID": potential_recommendation_index}) is None and recommendation_fail <= calculate_fail_count():
        recommendation_fail += 1
        potential_recommendation_index = random.randint(1, Recommendation.count_documents({}))
    if recommendation_fail > calculate_fail_count():
        potential_recommendation_index = Recommendation.find_one({}, sort=[('ID', -1)])['ID']
    return potential_recommendation_index


# Main Page Side function
def has_the_user_seen_this_recommendation_before(passcode, potential_recommendation_index):
    user = User.find_one({"Passcode": passcode})
    return not Recommendation_Per_Person.find_one(
        {'Passcode': passcode, 'ID': potential_recommendation_index,
         'Created_At': {'$gte': datetime.now() - timedelta(days=user['Repeat_Preference'])}}
    )


# Main page side function
def do_the_tags_match(passcode, potential_recommendation_index):
    tags = list(Tag.find({"ID": potential_recommendation_index}))
    user = User.find_one({"Passcode": passcode})
    today, yesterday, index = get_status(passcode)
    status = Status.find_one({"_id": index})
    for tag in tags:
        if tag['Title_Of_Criteria'] == 'Age Variant' and tag['Category'] != user['Age_Category']:
            return False
        if tag['Title_Of_Criteria'] == 'Focus Area' and tag['Category'] != user['Focus_Area']:
            return False
        if tag['Title_Of_Criteria'] == 'Stress Level' and int(tag['Category']) < status['Stress_Level']:
            return False
        if tag['Title_Of_Criteria'] == 'Time Available' and int(tag['Category']) < user['Time_Available']:
            return False
    return True


# Main Page Function
def get_recommendations(passcode):
    if not User.find_one({"Passcode": passcode}):
        return False, None, "Something went wrong, user not registered"
    if Recommendation.count_documents({}) == 0:
        return False, None, 'There are no recommendations available for you.'
    user = User.find_one({"Passcode": passcode})
    today, yesterday, index = get_status(passcode)
    if not today:
        return False, None, 'Something went wrong, status was not found'
    status = Status.find_one({"_id": index})
    latest_recommendation = Recommendation_Per_Person.find_one({"Passcode": passcode}, sort=[("Created_At", -1)])
    if latest_recommendation and status['Created_At'] == latest_recommendation['Status_Created_At']:
        return True, list(
            Recommendation_Per_Person.find({"Passcode": passcode, "Status_Created_At": status['Created_At']},
                                           sort=[("Pointer", 1)])), 'Feel free to try any of the below.'
    user_recommendations = []
    suggestions = user['Suggestions']
    index = 1
    fails = 0
    max_tries = calculate_fail_count()
    while index <= suggestions:
        potential_recommendation_index = generate_valid_index()
        if (
                has_the_user_seen_this_recommendation_before(passcode, potential_recommendation_index) and
                sum(1 for rec in user_recommendations if rec['ID'] == potential_recommendation_index) == 0 and
                do_the_tags_match(passcode, potential_recommendation_index) and
                Removed_Recommendation.find_one({"ID": potential_recommendation_index, "Passcode": passcode}) is None
        ) or fails > max_tries:
            new_entry = [
                {
                    'Passcode': passcode,
                    'ID': potential_recommendation_index,
                    'Pointer': index,
                    'Outcome': True,
                    'Fail_Count': f"{fails} / {max_tries}",
                    'Completed_At': None,
                    'Status_Created_At': status['Created_At'],
                    'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
            user_recommendations.extend(new_entry)
            index += 1
            fails = 0
        else:
            fails += 1
    Recommendation_Per_Person.insert_many(user_recommendations)
    return True, user_recommendations, 'Feel free to try any of the below.'


def generate_recommendation(passcode):
    if not User.find_one({"Passcode": passcode}):
        return False, "Something went wrong, user not registered"
    if Recommendation.count_documents({}) == 0:
        return False, "There are no recommendations available for you."
    today, yesterday, index = get_status(passcode)
    if not today:
        return False, "Something went wrong, status was not found"
    status = Status.find_one({"_id": index})
    if Recommendation_Per_Person.count_documents(
            {"Passcode": passcode, "Status_Created_At": status['Created_At']}) >= int(
            Recommendation.count_documents({}) / 4) + int(Recommendation.count_documents({}) * 0.1):
        return False, "You have received most available recommendations. No more for now!"
    user_recommendations = list(
        Recommendation_Per_Person.find({"Passcode": passcode, "Status_Created_At": status['Created_At']},
                                       sort=[("Pointer", 1)]))
    max_tries = calculate_fail_count()
    fails = 0
    potential_recommendation_index = generate_valid_index()
    while fails <= max_tries:
        if (
                has_the_user_seen_this_recommendation_before(passcode, potential_recommendation_index) and
                sum(1 for rec in user_recommendations if rec['ID'] == potential_recommendation_index) == 0 and
                do_the_tags_match(passcode, potential_recommendation_index) and
                Removed_Recommendation.find_one({"ID": potential_recommendation_index, "Passcode": passcode}) is None):
            new_entry = {
                'Passcode': passcode,
                'ID': potential_recommendation_index,
                'Pointer': len(user_recommendations) + 1,
                'Outcome': True,
                'Fail_Count': f"{fails} / {max_tries}",
                'Completed_At': None,
                'Status_Created_At': status['Created_At'],
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            Recommendation_Per_Person.insert_one(new_entry)
            return True, "Recommendation added"
        else:
            fails += 1
            potential_recommendation_index = generate_valid_index()
    new_entry = {
        'Passcode': passcode,
        'ID': generate_valid_index(),
        'Pointer': len(user_recommendations) + 1,
        'Outcome': True,
        'Fail_Count': f"{fails} / {max_tries}",
        'Completed_At': None,
        'Status_Created_At': status['Created_At'],
        'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    Recommendation_Per_Person.insert_one(new_entry)
    return True, 'Recommendation added'


# Main page function
def make_recommendation_table(recommendations, passcode):
    if not User.find_one({"Passcode": passcode}):
        return False, None
    Recommendation_table = []
    for entry in recommendations:
        this_recommendation = Recommendation.find_one({"ID": entry['ID']})
        if not this_recommendation:
            return False, None
        completed_duration = None
        if entry['Completed_At'] is not None:
            completed_at_dt = datetime.strptime(entry['Completed_At'], "%Y-%m-%d %H:%M:%S")
            time_diff = datetime.now() - completed_at_dt
            days = time_diff.days
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            completed_duration = f"{days} days, {hours} hours ago" if days > 0 else f"{hours} hours, {minutes} minutes and {seconds} seconds ago"
        new_entry = [
            {
                'ID': entry['ID'],
                'Pointer': entry['Pointer'],
                'Outcome': entry['Outcome'],
                'Status_Created_At': entry['Status_Created_At'],
                'Completed_At': completed_duration,
                'Title': this_recommendation['Title'],
                'Description': this_recommendation['Description'],
                'Points': this_recommendation['Points'],
                'Preference': (
                    False if Removed_Recommendation.find_one({"ID": entry['ID'], "Passcode": passcode})
                    else True if Favorite_Recommendation.find_one({"ID": entry['ID'], "Passcode": passcode})
                    else None
                )
            }
        ]
        Recommendation_table.extend(new_entry)
    return True, Recommendation_table


# Main Page Function
def get_limits(user):
    x = 100 * user["Level"]
    y = 50 - 5 * user["Level"]
    move_up_threshold = x * user["Level"]
    move_down_threshold = move_up_threshold * (1 - y / 100)
    return move_up_threshold, move_down_threshold


# Main page function
def get_record(passcode):
    if not User.find_one({"Passcode": passcode}):
        return False
    today = datetime.today().date()
    week_start = today
    if not today.weekday() == 0:
        week_start = today - timedelta(days=today.weekday())
    return Record.find_one({"Passcode": passcode, "Type": "D",
                            "Created_At": {"$gte": week_start.isoformat()}}) is None and Status.count_documents(
        {"Passcode": passcode}) > 1


# Main Page Function
def determine_level_change(passcode):
    if not User.find_one({"Passcode": passcode}):
        return "Something went wrong, user not registered"
    user = User.find_one({"Passcode": passcode})
    move_up_threshold, move_down_threshold = get_limits(user)
    message_for_user = f"You have remained at level {user['Level']}."
    message_for_system = f"User remained at level {user['Level']}."
    if user["Score"] > move_up_threshold:
        User.update_one({"Passcode": passcode}, {"$inc": {"Level": 1}})
        user = User.find_one({"Passcode": passcode})
        message_for_user = f"You have moved up to level {user['Level']}."
        message_for_system = f"User {passcode} moved up to level {user['Level']}"
    elif user["Score"] < move_down_threshold:
        if user["Level"] != 1:
            User.update_one({"Passcode": passcode}, {"$inc": {"Level": -1}})
            user = User.find_one({"Passcode": passcode})
            message_for_user = f"You have been demoted to level {user['Level']}."
            message_for_system = f"User {passcode} has been demoted to level {user['Level']}"
        else:
            message_for_user = "You have been demoted but remained at level 1."
            message_for_system = f"User {passcode} was demoted but remained at level 1"
    User.update_one({"Passcode": passcode}, {"$set": {"Score": 0}})
    Score_History.insert_one(
        {
            'Passcode': passcode,
            'Score': user["Score"],
            'Level': user["Level"],
            'Outcome': False,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    Record.insert_many(
        [
            {
                'Passcode': passcode,
                'Action': message_for_system,
                'Type': "C",
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                'Passcode': passcode,
                'Action': f"User {passcode} has had their score set to 0",
                'Type': "D",
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
    )
    return message_for_user


# Main page function
def add_points(index, passcode, status):
    user = User.find_one({"Passcode": passcode})
    if not user:
        return False, "Something went wrong, user not found"
    recommendation = Recommendation.find_one({"ID": index})
    if not recommendation:
        return False, "Something went wrong, Recommendation not found"
    recommendation_per_person_entry = Recommendation_Per_Person.find_one(
        {"ID": index, "Passcode": passcode, "Status_Created_At": status})
    if not recommendation_per_person_entry:
        return False, "Something went wrong, Recommendation not found in given recommendations"
    up, down = get_limits(user)
    points = user['Level'] * recommendation['Points']
    if user['Score'] + user['Level'] * recommendation['Points'] <= up + 50:
        User.update_one({"Passcode": passcode}, {"$inc": {"Score": user['Level'] * recommendation['Points']}})
    else:
        User.update_one({"Passcode": passcode}, {"$set": {"Score": up + 50}})
        points = up + 50 - user['Score']
    Recommendation_Per_Person.update_one({"ID": index, "Passcode": passcode, "Status_Created_At": status}, {
        "$set": {"Outcome": False, "Completed_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})
    user = User.find_one({"Passcode": passcode})
    outcome = None
    if user["Score"] > up:
        outcome = True
    if user["Score"] < down:
        outcome = False
    Score_History.insert_one(
        {
            'Passcode': passcode,
            'Score': user["Score"],
            'Level': user["Level"],
            'Outcome': outcome,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )

    Record.insert_many(
        [
            {
                'Passcode': passcode,
                'Action': f"User {passcode} increased their score by {points} points",
                'Type': "E",
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                'Passcode': passcode,
                'Action': f"User {passcode} completed recommendation {index}",
                'Type': "F",
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
    )
    return True, f"User {passcode} increased their score by {points} points"


# Main page function
def change_recommendation_preference_for_user(preference, passcode, index, function=None):
    if User.count_documents({"Passcode": passcode}) == 0:
        return False, "Something went wrong, user not found"
    if Recommendation.count_documents({"ID": index}) == 0:
        return False, "Something went wrong, Recommendation not found"
    Favorite_Recommendation.delete_one({"ID": index, "Passcode": passcode})
    Removed_Recommendation.delete_one({"ID": index, "Passcode": passcode})
    if function is True:
        return True, "Task Completed"
    new_entry = {
        'Passcode': passcode,
        'ID': index,
        'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    if preference == -1:
        Removed_Recommendation.insert_one(new_entry)
    else:
        Favorite_Recommendation.insert_one(new_entry)
    return True, "Task Completed"


# User profile page (for user) function
def update_user(passcode, username, repeat, age, focus_area, time_available, suggestions):
    user = User.find_one({"Passcode": passcode})
    if not user:
        return False, "Something went wrong, user not registered"
    if User.find_one({"Username": username}) and username != user['Username']:
        return False, "You need to enter a unique username"
    if not focus_area.strip() or time_available == 0 or suggestions == 0 or repeat == 0 or not age.strip():
        return False, "You need to enter appropriate information"
    User.update_one({"Passcode": passcode}, {"$set": {
        "Username": username,
        "Repeat_Preference": repeat,
        "Age_Category": age,
        "Focus_Area": focus_area,
        "Suggestions": suggestions,
        "Time_Available": time_available
    }})
    Record.insert_one(
        {
            'Passcode': passcode,
            'Action': f"User {passcode} updated their profile: Username {username}, Repeat Preference {repeat}, Age {age}, focus {focus_area}, suggestions {suggestions}, time available {time_available}",
            'Type': "G",
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    return True, "User Profile Updated"


# Recommendation page (for user) side function
def add_collection(passcode, status, collection_name, collection, completed):
    if not status:
        return None
    data_table = []
    data = collection.find({"Passcode": passcode})
    for entry in data:
        outcome = None
        if collection == Recommendation_Per_Person:
            outcome = entry['Outcome']
        if (collection == Recommendation_Per_Person and (
                outcome == completed or completed is None)) or collection != Recommendation_Per_Person:
            data_table.extend(create_entry(entry['ID'], passcode, collection_name, outcome, entry['Created_At']))
    return data_table


# Recommendation page (for user) side function    
def create_entry(index, passcode, collection, outcome, created):
    this_recommendation = Recommendation.find_one({"ID": index})
    if this_recommendation:
        new_entry = [
            {
                'Title': this_recommendation['Title'],
                'Description': this_recommendation['Description'],
                'ID': index,
                'Type': collection,
                'Outcome': outcome,
                'Created_At': created,
                'Extend': True,
                'Remove': (
                    True if Removed_Recommendation.find_one(
                        {"ID": this_recommendation['ID'], "Passcode": passcode}) or Favorite_Recommendation.find_one(
                        {"ID": this_recommendation['ID'], "Passcode": passcode})
                    else False
                )
            }
        ]
    else:
        new_entry = [
            {
                'Title': "Recommendation not found",
                'Description': "Recommendation not found",
                'ID': "Recommendation not found",
                'Type': collection,
                'Outcome': outcome,
                'Created_At': created,
                'Extend': False,
                'Remove': False
            }
        ]
    return new_entry


# Recommendation page (for user) side function
def sort_by_created_by(entry):
    return entry["Created_At"]


# Recommendation page (for user) function
def create_recommendation_history(passcode, order, include_favorite, include_removed,
                                  include_Recommendations, completed):
    user = User.find_one({"Passcode": passcode})
    query = f"Order: {order} - Favorite {include_favorite} - Removed {include_removed} - Per Person {include_Recommendations} / {completed}"
    if not user:
        return False, None, "Something went wrong, user not registered"
    user_recommendation = []
    temporary_table = add_collection(passcode, include_favorite, "Favorite_Recommendation", Favorite_Recommendation,
                                     None)
    if temporary_table is not None:
        user_recommendation.extend(temporary_table)
    temporary_table = add_collection(passcode, include_removed, "Removed_Recommendation", Removed_Recommendation, None)
    if temporary_table is not None:
        user_recommendation.extend(temporary_table)
    temporary_table = add_collection(passcode, include_Recommendations, "Recommendation_Per_Person",
                                     Recommendation_Per_Person, completed)
    if temporary_table is not None:
        user_recommendation.extend(temporary_table)
    user_recommendation.sort(key=sort_by_created_by, reverse=(order == -1))
    Record.insert_one(
        {
            'Passcode': passcode,
            'Action': f"User {passcode} requested record for {query}",
            'Type': "L",
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    return True, user_recommendation, f"Record for user {passcode} assembled."


# Recommendation page (for admin) function
def add_recommendation(ID, passcode, title, description, link, points):
    ID = int(ID)
    if not User.find_one({"Passcode": passcode}):
        return False, "Something went wrong, user not registered"
    if Recommendation.find_one({"ID": ID}):
        return False, "Please try again, it look like the ID generated has already been added."
    if not title.strip() or not description.strip() or points < 10 or points > 150 or (
            link is not None and not link.strip()):
        return False, "You need to fill in all mandatory fields"
    Recommendation.insert_one(
        {
            'ID': ID,
            'Passcode': passcode,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Title': title,
            'Description': description,
            'Link': link,
            'Points': points
        }
    )
    return True, "Recommendation added"


# Recommendation page (for admin) function
def add_tag(ID, passcode, title, category):
    ID = int(ID)
    if not User.find_one({"Passcode": passcode}):
        return False, "Something went wrong, user not registered"
    if not Recommendation.find_one({"ID": ID}):
        return False, "Something went wrong, recommendation not found"
    if Tag.find_one({"ID": ID, "Title_Of_Criteria": title, "Category": category}):
        return False, "Tag already exists"
    Tag.insert_one(
        {
            'ID': ID,
            'Passcode': passcode,
            'Title_Of_Criteria': title,
            'Category': category,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )
    return True, "Tag added"


# Questionnaire page (for admin) function
def add_question_to_Questionnaire(ID, passcode, question_input):
    ID = int(ID)
    if not User.find_one({"Passcode": passcode}):
        return False, "Something went wrong, user not registered"
    if Question_Questionnaire.find_one({"ID": ID}):
        return False, "ID already exists"
    if Question_Questionnaire.find_one({"Question": question_input}):
        return False, "Question already exists"
    if not question_input.strip():
        return False, "You need to enter a question"
    Question_Questionnaire.insert_one(
        {
            'ID': ID,
            'Passcode': passcode,
            'Question': question_input,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )
    return True, "Question added"


# Database page (for admin) function
def delete_entry(passcode, key, key2, created, collection_name, this_user_passcode):
    if not User.find_one({"Passcode": passcode}):
        return False, "Something went wrong, requested user not registered"
    if not User.find_one({"Passcode": this_user_passcode}):
        return False, None, "Something went wrong, User not registered"
    if collection_name == "User":
        query = {"Passcode": passcode}
    elif collection_name == "Question":
        query = {"Passcode": passcode, "Question": key, "Created_At": created}
    elif collection_name == "Record":
        query = {"Passcode": passcode, "Type": key, "Created_At": created}
    elif collection_name == "Status":
        query = {"Passcode": passcode, "Created_At": created}
    elif collection_name == "Recommendation":
        query = {"ID": key, "Created_At": created}
    elif collection_name == "Tag":
        query = {"Passcode": passcode, "ID": key, "Category": key2, "Created_At": created}
    elif collection_name == "Favorite_Recommendation":
        query = {"Passcode": passcode, "ID": key, "Created_At": created}
    elif collection_name == "Removed_Recommendation":
        query = {"Passcode": passcode, "ID": key, "Created_At": created}
    elif collection_name == "Recommendation_Per_Person":
        query = {"Passcode": passcode, "Pointer": key, "ID": key2, "Created_At": created}
    elif collection_name == "Question_Questionnaire":
        query = {"Passcode": passcode, "ID": key, "Question": key2, "Created_At": created}
    elif collection_name == "Score_History":
        query = {"Passcode": passcode, "Score": key, "Level": key2, "Created_At": created}
    else:
        return False, "Invalid collection name"
    collection = globals().get(collection_name)  # Get the actual collection object
    if not collection_name:
        return False, "Collection not found"
    delete_result = collection.delete_one(query)
    deleted_count = delete_result.deleted_count
    Record.insert_one(
        {
            'Passcode': this_user_passcode,
            'Action': f"User {this_user_passcode} requested to delete record {query} from {collection_name}",
            'Type': "J",
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    if deleted_count > 0:
        Record.insert_one(
            {
                'Passcode': this_user_passcode,
                'Action': f"Deleted 1 record for {query} from {collection_name} as requested by user {this_user_passcode}",
                'Type': "K",
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
        return True, f"Deleted 1 record for {query} from {collection_name}"
    Record.insert_one(
        {
            'Passcode': this_user_passcode,
            'Action': f"No matching record {query} found in {collection_name} as requested by user {this_user_passcode}",
            'Type': "K",
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    return False, f"No matching record {query} found in {collection_name}"


# Record page side function
def sort_by_time(entry):
    return entry["Created_At"], entry["Message"]


# Record page side function
def sort_by_message(entry):
    return entry["Message"], entry["Created_At"]


# Record page side function
def sort_by_type(entry):
    return entry["Type"], entry["Created_At"], entry["Message"]


# Database page (for user) function
def create_history(passcode, priority, order, include_user, include_question, include_record,
                   include_status, include_recommendation, include_Tag,
                   include_favorite, include_removed, include_recommendation_per_person, include_question_Questionnaire, include_score, this_user_passcode):
    if not User.find_one({"Passcode": passcode}):
        return False, None, "User requested not registered"
    if not User.find_one({"Passcode": this_user_passcode}):
        return False, None, "User not registered"
    query = f"Priority {priority} - Order {order} - User {include_user} - Question {include_question} - Record {include_record} - Status {include_status} - Recommendation {include_recommendation} - Tag {include_Tag} - Favorite {include_favorite} - Removed {include_removed} - Per Person {include_recommendation_per_person} - Daily Stress Questionnaire - {include_question_Questionnaire} - Score {include_score}"
    user_history = []
    message_templates = {
        "User": "User {Passcode} registered.",
        "Question": "User {Passcode} was asked '{Question}' and answered {Answer}.",
        "Record": "{Action}",
        "Status": "User {Passcode} answered Daily Stress Questionnaire.",
        "Recommendation": "User {Passcode} added recommendation '{Title}' with ID {ID}.",
        "Tag": "User {Passcode} added Tag '{Title_Of_Criteria}:{Category}' to recommendation with ID {ID}.",
        "Favorite_Recommendation": "User {Passcode} marked recommendation with ID {ID} as favorite.",
        "Removed_Recommendation": "User {Passcode} rejected recommendation with ID {ID}.",
        "Recommendation_Per_Person": "Recommendation with ID {ID} was assigned to User {Passcode} with pointer {Pointer}.",
        "Question_Questionnaire": "User {Passcode} added question '{Question}' with ID {ID}",
        "Score_History": "Score {Score} recorded for user {Passcode} at level {Level}"
    }

    # Datapage page side function
    def add_history_entries(collection_name, collection, key, key2=None):
        entries = collection.find({"Passcode": passcode})
        for entry in entries:
            new_entry = [
                {
                    'Type': collection_name,
                    'Key': entry.get(key, "N/A"),
                    'Key2': entry.get(key2, None),
                    'Message': message_templates[collection_name].format(**entry),
                    'Created_At': entry['Created_At'],
                    'Passcode': passcode
                }
            ]
            user_history.extend(new_entry)

    if include_user:
        add_history_entries("User", User, "Passcode")
    if include_question:
        add_history_entries("Question", Question, "Question")
    if include_record:
        add_history_entries("Record", Record, "Type")
    if include_status:
        add_history_entries("Status", Status, "Passcode")
    if include_recommendation:
        add_history_entries("Recommendation", Recommendation, "ID")
    if include_Tag:
        add_history_entries("Tag", Tag, "ID", "Category")
    if include_favorite:
        add_history_entries("Favorite_Recommendation", Favorite_Recommendation, "ID")
    if include_removed:
        add_history_entries("Removed_Recommendation", Removed_Recommendation, "ID")
    if include_recommendation_per_person:
        add_history_entries("Recommendation_Per_Person", Recommendation_Per_Person, "Pointer", "ID")
    if include_question_Questionnaire:
        add_history_entries("Question_Questionnaire", Question_Questionnaire, "ID", "Question")
    if include_score:
        add_history_entries("Score_History", Score_History, "Score", "Level")

    if priority == "Time":
        user_history.sort(key=sort_by_time, reverse=(order == -1))
    elif priority == "Substance":
        user_history.sort(key=sort_by_message, reverse=(order == -1))
    else:
        user_history.sort(key=sort_by_type, reverse=(order == -1))
    Record.insert_one(
        {
            'Passcode': passcode,
            'Action': f"User {this_user_passcode} requested record for {query} for user {passcode}",
            'Type': "L",
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    return True, user_history, f"Record for user {passcode} assembled."
