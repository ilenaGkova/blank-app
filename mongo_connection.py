from datetime import datetime, timedelta
import random
import pymongo
import names
import streamlit as st
from random_word import RandomWords
from Tables import Users

@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets["mongo"]["uri"])

client = init_connection()
db = client.StressTest
Status = db["Status"]
User = db["User"]
Question = db["Question"]
Record = db["Record"]

if not User.find_one({"Username": "Admin"}): User.insert_many(Users)

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
            'Level': 0,
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
    latest_status = Status.find_one({"passcode": passcode}, sort=[("Created_At", -1)])
    if not latest_status: return False, -1
    last_status_time = datetime.strptime(latest_status['Created_At'], '%Y-%m-%d %H:%M:%S')
    return (datetime.now() - last_status_time) <= timedelta(hours=48), latest_status["_id"]

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
    if Record.find_one({"Passcode": passcode, "Action": "Days connected increased", "Created_At": {"$gte": datetime.combine(datetime.today(), datetime.min.time())}}):
        return "You have already signed it today, your streak will not change"
    else:
        if not User.find_one({"Passcode": passcode}): return "Something went wrong, user not registered."  
        User.update_one({"Passcode": passcode}, {"$inc": {"Days_Summed": 1}})
        streak_increased, index_status = get_status(passcode) 
        message = None
        streak_action = None
        if streak_increased:
            User.update_one({"Passcode": passcode}, {"$inc": {"Streak": 1}})
            message =  "Your streak was increased."
            streak_action = 'Streak increased'
        else:
            User.update_one({"Passcode": passcode},{"$set": {"Streak": 1}})
            message =  "You did not check in less than 48 hours ago. Your streak was reset."
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
