from datetime import datetime, timedelta
import random
from Tables import Users, Questions, Status, Favorite, Recommendations_Per_Person, Recommendations, Tags, Records, Removed_Recomendations

# Start Page Function
def validate_user(username, password):
    if not username.strip() or not password.strip():
        return False, "You need to fill in all fields provided to proceed"
    for user in Users:
        if user['Username'] == username and user["Password"] == password:
            user['Status'] = 1
            return True, "You have an account"
    return False, "You do not have an account"

# Start Page Function
def new_user(first_name,last_name,username,password,age):
    if not first_name.strip() or not last_name.strip() or not username.strip() or not password.strip() or not age.strip():
        return False, "You need to fill in all fields provided to proceed"
    else:
        if username == "username":
            return False, "You can't use the word 'username' for a username"
        valid_username = True
        valid_password = True
        index = 0
        while index <= len(Users) - 1 and valid_username and valid_password:
            valid_username = not Users[index]['Username'] == username
            valid_password = not Users[index]['Password'] == password
            index += 1  
        if valid_username and valid_password:
            new_entry = [
                {
                    'Name': first_name,
                    'Surname': last_name,
                    'Username': username,
                    'Password': password,
                    'Repeat_Prefence': 1,
                    'Age_Category': age,
                    'Level': 0,
                    'Score': 0,
                    'Streak': 0,
                    'Days_Summed': 0,   
                    'Status': 1, 
                    'Role': 'User',
                    'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
            Users.append(new_entry)
            return True, "You have been added to our service"
        elif valid_username and not valid_password:
            return False, "You need to enter a unique username"
        elif not valid_username and valid_password:
            return False, "You need to enter a unique password"
        else:
            return False, "You need to enter a unique username and password"

# Start/Status Page Function       
def record_question(question,answer,username):
    new_entry = [
        {
            'username': username,
            'question': question,
            'answer': answer,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]
    Questions.append(new_entry)

# Status Page Function
def record_status(username,focus_area,stress_level,time_available,suggestions):
    if not focus_area.strip() or not stress_level==0 or not time_available==0 or not suggestions==0:
        return False, "You need to fill in all fields provided to proceed"
    else:
        index = get_user(username)
        if index == -1:
            return False,"Something went wrong, user not registered."
        new_entry = [
            {
                'Username': username,
                'Focus_Area': focus_area,
                'Stress_Level': stress_level,
                'Suggestions': suggestions,
                'Time_Available': time_available,
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        Status.append(new_entry)
        Users[index]['Status'] = 2
        return True, "Status recorded"

# Status Page
def update_user_streak(username):
    if find_action_in_record(username,'Streak increased/reset'):
        return "You have already signed it today, your streak will not be increased"
    else:
        index = get_user(username)
        if index == -1:
            return "Something went wrong, user not registered."
        Users[index]['Days_Summed'] = Users[index]['Days_Summed'] + 1
        streak_increased, index_status = get_status(username) 
        message = None
        if streak_increased:
            Users[index]['Streak'] = Users[index]['Streak'] + 1
            message =  "Your streak was increased."
        else:
            Users[index]['Streak'] = 1
            message =  "You did not check in less than 48 hours ago. Your streak was reseted."
        new_entry = [
            {
                'Username': username,
                'Action': 'Streak increased/reset',
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                'Username': username,
                'Action': 'Days connected increased',
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        Records.append(new_entry)
        return message

# General function used everywhere
def find_action_in_record(username, action):
    today = datetime.now().strftime("%Y-%m-%d")
    user_record_today = []
    if len(Records):
        user_record_today =  [
            (Records['Username'] == username) &
            (Records['Action'] == action) &
            (Records['Created_At'].startswith(today))
        ]
    return len(user_record_today) == 1

# Status/Main Page Function
def get_status(username):
    index = len(Status) - 1
    found = False
    while index >= 0 and not found:
        found = Status[index]['Username'] == username
        index -= 1
    last_status = None
    time_diff = None
    if found:
        last_status = datetime.strptime(Status[index+1]['Created_At'].to_datetime,'%Y-%m-%d %H:%M:%S')
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_diff = current_datetime - last_status
        return time_diff <= timedelta(hours=48), index+1
    return False, -1

# Main Page Function
def get_past_recomendations(username,days_behind):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    end_of_today = current_datetime.replace(hour=23, minute=59, second=59, microsecond=999999)
    start_date = current_datetime - timedelta(days=days_behind)
    start_of_range = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    user_past_recomendations = [
        (Recommendations_Per_Person['Created_At'] >= start_of_range) & 
        (Recommendations_Per_Person['Created_At'] <= end_of_today) & 
        (Recommendations_Per_Person['Username'] == username)
    ]
    return user_past_recomendations 

# Main Page Function
def get_recomendations(username):
    index = get_user(username)
    user_recomendations = []
    if index >= 0:
        condition, index = get_status(username)
        suggestions = Status[index]['Suggestions']
        index = 1
        fails = 0
        while index <= suggestions:
            pottential_recomendation_index = random.randint(1, len(Recommendations))
            if (has_the_user_seen_this_recomendation_before(pottential_recomendation_index) and will_the_user_see_this_recomendation_twice(username, pottential_recomendation_index) and do_the_tags_match(username, pottential_recomendation_index) and has_the_user_rejected_this_suggestion(username, pottential_recomendation_index)) or fails == 3:
                new_entry = [
                    {
                        'Username': username,
                        'ID': pottential_recomendation_index,
                        'Outcome': 'Incomplete',
                        'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                ]
                user_recomendations.append(new_entry)
                index += 1
                fails = 0
            else:
                fails += 1
        Recommendations_Per_Person.append(user_recomendations)
        return True, user_recomendations, 'Feel free to try any of the below'
    return False, None, 'Something went wrong, user not registered.' 

# Main page side function
def has_the_user_rejected_this_suggestion(username, pottential_recomendation_index):
    table_filtered = [
        (Removed_Recomendations['ID'] == pottential_recomendation_index) & 
        (Removed_Recomendations['Username'] == username)
    ]
    return len(table_filtered) == 0

# Main page side function
def do_the_tags_match(username, pottential_recomendation_index):
    table_filtered = [(Tags['ID'] == pottential_recomendation_index)]
    index = get_user(username)
    age = Users[index]['Age_Category']
    condition, index = get_status(username)
    focus_area = Status[index]['Focus_Area']
    stress_level = Status[index]['Stress_Level']
    time_available = Status[index]['Time_Available']
    index = 0
    valid = True
    while index <= len(table_filtered) - 1 and valid:
        if table_filtered[index]['Title_Of_Criteria'] == 'Age Variant':
            valid = table_filtered[index]['Category'] == age
        elif table_filtered[index]['Title_Of_Criteria'] == 'Focus Area':
            valid = table_filtered[index]['Category'] == focus_area
        elif table_filtered[index]['Title_Of_Criteria'] == 'Stress Level':
            valid = table_filtered[index]['Category'] == stress_level
        else:
            valid = table_filtered[index]['Category'] == time_available
        index += 1
    return valid

# Main page side function
def will_the_user_see_this_recomendation_twice(user_recomendations, pottential_recomendation_index):
    table_filtered = [(user_recomendations['ID'] == pottential_recomendation_index)]
    return len(table_filtered) == 0

# Main page side function
def has_the_user_seen_this_recomendation_before(username,pottential_recomendation_index):
    index = get_user(username)
    user_past_recomendations = get_past_recomendations(username,Users[index]['Repeat_Prefence'])
    table_filtered = [(user_past_recomendations['ID'] == pottential_recomendation_index)]  
    return len(table_filtered) == 0

# Status/Main Page Function
def get_user(username):
    index = 0
    for entry in Users:
        if entry['Username'] == username:
            return index
        index += 1
    return -1    
