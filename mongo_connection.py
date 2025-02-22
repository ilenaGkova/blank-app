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
Recommendation_Per_Person = db["Recommendations_Per_Person"]
Tag = db["Tag"]
Recommendation = db["Recommendation"]
Removed_Recommendation = db["Removed_Recommendation"]
Favorite_Recommendation = db["Favorite"]

if not User.find_one({"Username": "Admin"}): User.insert_many(Users)
if not Tag.find_one({"ID": 1}): Tag.insert_many(Tags)
if not Recommendation.find_one({"ID": 1}): Recommendation.insert_many(Recommendations)

# Start Page Function
def validate_user(passcode):
    if not passcode.strip():
        return False, "You need to enter your passcode"
    potential_user = User.find_one({"Passcode": passcode})
    return (True, "You have an account") if potential_user else (False, "You do not have an account")

# Start Page Function
def new_user(username, passcode, age,focus_area,time_available,suggestions):
    if not username.strip() or passcode == "Please reload the page" or not age.strip() or not focus_area.strip() or time_available==0 or suggestions==0:
        return False, "You need to fill in all fields provided to proceed. If Passcode not available reload the page."
    if User.find_one({"Username": username}): return False, "You need to enter a unique username"
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
    return True, "You have been added to our service"

# Start Page Function
def generate_unique_passcode(max_attempts=100):
    attempt_count = 0
    while attempt_count < max_attempts:
        passcode = str(random.randint(1000000000, 9999999999))
        if not User.find_one({"Passcode": passcode}): return passcode
        attempt_count += 1
    return "Please reload the page"

# Start Page Function
def generate_animal_username(max_attempts=100):
    attempt_count = 0
    animals = ['Lion', 'Tiger', 'Elephant', 'Giraffe', 'Zebra', 'Panda', 'Koala', 'Kangaroo', 'Cheetah', 'Penguin']
    adjectives = ['Fluffy', 'Mighty', 'Sneaky', 'Grumpy', 'Mysterious', 'Sleepy', 'Bold', 'Spiky', 'Shiny', 'Wild']
    while attempt_count < max_attempts:
        username = f"{random.choice(adjectives)}{random.choice(animals)}#{random.randint(1000, 9999)}"
        if not User.find_one({"Username": username}): return username
        attempt_count += 1
    return "Please reload the page"
        
# Start/Status Page Function       
def record_question(question,answer,passcode):
    Question.insert_one(
        {
            'Passcode': passcode,
            'Question': question,
            'Answer': answer,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )

# Status/Main Page Function
def get_status(passcode):
    latest_status = Status.find_one({"Passcode": passcode}, sort=[("Created_At", -1)])
    if not latest_status: return False, False, -1
    last_status_time = datetime.strptime(latest_status['Created_At'], '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    return (now.date() == last_status_time.date()),((now.date() - last_status_time.date()).days == 1), latest_status["_id"]

# Status Page Function
def record_status(passcode,stress_level):
    if stress_level==0:
        return False, "You need to fill in all fields provided to proceed"
    else:
        if not User.find_one({"Passcode": passcode}): return False,"Something went wrong, user not registered."
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
    last_record = Record.find_one({"Passcode": passcode, "Action": "Days connected increased"}, sort=[("Created_At", -1)])
    if last_record:
        last_time = datetime.strptime(last_record["Created_At"], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        if last_time.date() == now.date():
            return "You have already signed in today, your streak will not change."
    if not User.find_one({"Passcode": passcode}): return "Something went wrong, user not registered."  
    User.update_one({"Passcode": passcode}, {"$inc": {"Days_Summed": 1}})
    today, yesterday, index = get_status(passcode) 
    message = None
    streak_action = None
    if yesterday:
        User.update_one({"Passcode": passcode}, {"$inc": {"Streak": 1}})
        message =  "Your streak was increased."
        streak_action = 'Streak increased'
    else:
        User.update_one({"Passcode": passcode},{"$set": {"Streak": 1}})
        if index == -1: message =  "Wellcome to your first Status."
        else: message =  "You did not check in less than 48 hours ago. Your streak was reset."
        streak_action = 'Streak reset'
        
    Record.insert_many(
        [
            {
                'Passcode': passcode,
                'Action': streak_action,
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                'Passcode': passcode,
                'Action': 'Days connected increased',
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
    )
    return message
    
# Main page side side function
def calculate_fail_count():
    number_of_recomedations_in_total = Recommendation.count_documents({})  
    last_entry_added = Recommendation.find_one({}, sort=[('ID', -1)])
    max_ID = last_entry_added['ID'] 
    total_possible_IDs = max_ID 
    number_of_recommendation_after_removing_deleted_entries = total_possible_IDs - number_of_recomedations_in_total
    return int(total_possible_IDs / (number_of_recomedations_in_total - number_of_recommendation_after_removing_deleted_entries))

# Main page side function
def generate_valid_index():
    recommendation_fail = 0
    potential_recommendation_index = random.randint(1, Recommendation.count_documents({}))
    while Recommendation.find_one({"ID": potential_recommendation_index}) is None and recommendation_fail <= calculate_fail_count():
        recommendation_fail += 1
        potential_recommendation_index = random.randint(1, Recommendation.count_documents({}))
    if recommendation_fail > calculate_fail_count():
        potential_recommendation_index = Recommendation.find_one({}, sort=[('ID', -1)])['ID']
    return potential_recommendation_index

# Main Page Side Side Function
def get_past_recomendations(passcode,days_behind):
    current_datetime = datetime.now()
    end_of_today = current_datetime.replace(hour=23, minute=59, second=59, microsecond=999999)
    start_date = current_datetime - timedelta(days=days_behind)
    start_of_range = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    user_past_recommendations = Recommendation_Per_Person.find({'Passcode': passcode, 'Created_At': {'$gte': start_of_range, '$lte': end_of_today}})
    return list(user_past_recommendations)

# Main Page Side function
def has_the_user_seen_this_recomendation_before(passcode,potential_recommendation_index):
    user = User.find_one({"Passcode": passcode})
    user_past_recommendations = get_past_recomendations(passcode, user['Repeat_Preference'])
    return not any(rec['ID'] == potential_recommendation_index for rec in user_past_recommendations)

# Main page side function
def do_the_tags_match(passcode, potential_recommendation_index):
    tags = list(Tag.find({"ID": potential_recommendation_index}))
    user = User.find_one({"Passcode": passcode})
    today,yesterday, index = get_status(passcode)
    status = Status.find_one({"_id": index})
    for tag in tags:
        if tag['Title_Of_Criteria'] == 'Age Variant' and tag['Category'] != user['Age_Category']: return False
        if tag['Title_Of_Criteria'] == 'Focus Area' and tag['Category'] != user['Focus_Area']: return False
        if tag['Title_Of_Criteria'] == 'Stress Level' and tag['Category'] != status['Stress_Level']: return False
        if tag['Title_Of_Criteria'] == 'Time Available' and tag['Category'] != user['Time_Available']: return False
    return True

# Main Page Function
def get_recomendations(passcode):
    if Recommendation.count_documents({}) == 0: return False, None, 'There are no recommendations available for you.'
    user = User.find_one({"Passcode": passcode})
    if not user: return False, None, 'Something went wrong, user not registered'
    today,yesterday, index = get_status(passcode)
    if not today: return False, None, 'Something went wrong, status was not found'
    status = Status.find_one({"_id": index})
    latest_recommendation = Recommendation_Per_Person.find_one({"Passcode": passcode}, sort=[("Created_At", -1)])
    if latest_recommendation and status['Created_At'] == latest_recommendation['Status_Created_At']:
        return True, list(Recommendation_Per_Person.find({"Passcode": passcode, "Status_Created_At": status['Created_At']}, sort=[("Pointer", 1)])), 'Feel free to try any of the below.' 
    user_recommendations = []
    suggestions = user['Suggestions']
    index = 1
    fails = 0
    while index <= suggestions:
        potential_recommendation_index = generate_valid_index()
        if (
            has_the_user_seen_this_recomendation_before(passcode, potential_recommendation_index) and
            sum(1 for rec in user_recommendations if rec['ID'] == potential_recommendation_index) == 0 and
            do_the_tags_match(passcode, potential_recommendation_index) and
            Removed_Recommendation.find_one({"ID": potential_recommendation_index, "Passcode": passcode}) is None
        ) or fails == 3:
            new_entry = [
                {
                    'Passcode': passcode,
                    'ID': potential_recommendation_index,
                    'Pointer': index,
                    'Outcome': True,
                    'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'Status_Created_At': status['Created_At'],
                    'Completed_At': None
                }
            ]
            user_recommendations.extend(new_entry)
            index += 1
            fails = 0
        else:
            fails += 1
    Recommendation_Per_Person.insert_many(user_recommendations)
    return True, user_recommendations, 'Feel free to try any of the below.' 

# Main page function
def make_recommendation_table(recommendations,passcode):
    Recommendation_table = []
    for entry in recommendations:
        this_recommendation = Recommendation.find_one({"ID": entry['ID']})
        if not this_recommendation: return False, None
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
    return move_up_threshold,move_down_threshold

# Main page function
def get_record(passcode):
    today = datetime.today().date()
    week_start = today
    if not today.weekday() == 0: week_start = today - timedelta(days=today.weekday())   
    return Record.find_one({"Passcode": passcode, "Action": "Score Reset", "Created_At": {"$gte": week_start.isoformat()}}) is None

# Main Page Function
def determine_level_change(passcode):
    user = User.find_one({"Passcode": passcode})
    move_up_threshold, move_down_threshold = get_limits(user)
    message_for_user = f"You have remained at level {user['Level']}."
    message_for_system = f"User remained at level {user['Level']}."
    if user["Score"] > move_up_threshold:
        User.update_one({"Passcode": passcode}, {"$inc": {"Level": 1}})
        user = User.find_one({"Passcode": passcode})
        message_for_user = f"You have moved up to level {user['Level']}."
        message_for_system = f"User moved up to level {user['Level']}"
    elif user["Score"] < move_down_threshold:
        if user["Level"] != 1:
            User.update_one({"Passcode": passcode}, {"$inc": {"Level": -1}})
            user = User.find_one({"Passcode": passcode})
            message_for_user = f"You have been demoted to level {user['Level']}."
            message_for_system = f"User has been demoted to level {user['Level']}"
        else:
            message_for_user = "You have been demoted but remained at level 1."
            message_for_system = "User was demoted but remained at level 1" 
    User.update_one({"Passcode": passcode},{"$set": {"Score": 0}})
    Record.insert_many(
        [
            {
                'Passcode': passcode,
                'Action': message_for_system,
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                'Passcode': passcode,
                'Action': 'Score Reset',
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
    )
    return message_for_user

# Main page function
def add_points(index,passcode,status):
    user = User.find_one({"Passcode": passcode})
    if not user: return False
    recommendation = Recommendation.find_one({"ID": index})
    if not recommendation: return False
    recommendation_per_person_entry = Recommendation_Per_Person.find_one({"ID": index, "Passcode": passcode, "Status_Created_At": status})
    if not recommendation_per_person_entry: return False
    up, down = get_limits(user)
    if user['Score']+user['Level']*recommendation['Points'] <= up+50: User.update_one({"Passcode": passcode}, {"$inc": {"Score": user['Level']*recommendation['Points']}})
    else: User.update_one({"Passcode": passcode}, {"$set": {"Score": up+50}})
    Recommendation_Per_Person.update_one({"ID": index, "Passcode": passcode, "Status_Created_At": status}, {"$set": {"Outcome": False, "Completed_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})
    return True

# Main page function
def change_recommendation_preference_for_user(preference,passcode,index):
    if User.count_documents({"Passcode": passcode}) == 0: return False
    if Recommendation.count_documents({"ID": index}) == 0: return False
    Favorite_Recommendation.delete_one({"ID": index, "Passcode": passcode})
    Removed_Recommendation.delete_one({"ID": index, "Passcode": passcode})
    new_entry = {
        'Passcode': passcode,
        'ID': index,
        'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    if preference == -1: Removed_Recommendation.insert_one(new_entry)
    else: Favorite_Recommendation.insert_one(new_entry)
    return True
