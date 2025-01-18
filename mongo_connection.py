from datetime import datetime, timedelta
import random
from Tables import Users, Questions, Status, Favorite, Recommendations_Per_Person, Recommendations, Tags

def validate_user(username, password):
    if not username.strip() or not password.strip():
        return False, "You need to fill in all fields provided to proceed"
    for user in Users:
        if user["Username"] == username and user["Password"] == password:
            user["Status"] = 1
            return True, "You have an account"
    return False, "You do not have an account"

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

def record_status(username,focus_area,stress_level,time_available,suggestions):
    if not focus_area.strip() or not stress_level==0 or not time_available==0 or not suggestions==0:
        return False, "You need to fill in all fields provided to proceed"
    else:
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
        return True, "Status recorded"
    
def get_favorites(username):
    user_favorites = [Favorite["user_username"] == username]
    return user_favorites

def get_past_recomendations(username,days_behind):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    end_of_today = current_datetime.replace(hour=23, minute=59, second=59, microsecond=999999)
    start_date = current_datetime - timedelta(days=days_behind)
    start_of_range = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    user_past_recomendations = [
        (Recommendations_Per_Person["created_at"] >= start_of_range) & 
        (Recommendations_Per_Person["created_at"] <= end_of_today) & 
        (Recommendations_Per_Person["user_username"] == username)
    ]
    return user_past_recomendations

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
        return time_diff <= timedelta(hours=24), index
    index = len(Status) - 1
    found = False
    while index >= 0 and not found:
        found = Users[index]['Username'] == username
        index -= 1
    if found:
        return True, index 
    return False, -1 

def get_recomendations(username):
    index = 0
    found = False
    age = None
    while index <= len(Users) - 1 and not found:
        found = Users[index]['Username'] == username
        index += 1
    user_recomendations = []
    if found:
        user_past_recomendations = get_past_recomendations(username,Users[index-1]['Repeat_Prefence'])
        age = Users[index-1]['Age_Category']
        condition, index = get_status(username)
        focus_area = Status[index]['Focus_Area']
        stress_level = Status[index]['Stress_Level']
        time_available = Status[index]['Time_Available']
        suggestions = Status[index]['Suggestions']
        index = 1
        while index <= suggestions:
            pottential_recomendation_index = random.randint(1, len(Recommendations))
            valid = True
            table_filtered = [(user_past_recomendations[pottential_recomendation_index]['ID'] == pottential_recomendation_index)]  
            for entry in table_filtered:
                valid = False
            if valid or fails == 3:
                table_filtered = [(user_recomendations[pottential_recomendation_index]['ID'] == pottential_recomendation_index)]
                for entry in table_filtered:
                    valid = False
                if valid or fails == 3:
                    table_filtered = [(Tags[pottential_recomendation_index]['ID'] == pottential_recomendation_index)]
                    for entry in table_filtered:
                        if entry['Title_Of_Criteria'] == 'Age Variant':
                            valid = entry['Category'] == age
                        elif entry['Title_Of_Criteria'] == 'Focus Area':
                            valid = entry['Category'] == focus_area
                        elif entry['Title_Of_Criteria'] == 'Stress Level':
                            valid = entry['Category'] == stress_level
                        else:
                            valid = entry['Category'] == time_available
                    if valid or fails == 3:
                        new_entry = [
                            {
                                'Username': username,
                                'ID': pottential_recomendation_index,
                                'Outcome': None,
                                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                        ]
                        user_recomendations.append(new_entry)
                        index += 1
                        fails = 0
                    else:
                        fails += 1
                else:
                    fails += 1
            else:
                fails += 1
        Recommendations_Per_Person.append(user_recomendations)
        return True, user_recomendations
    return False, user_recomendations
