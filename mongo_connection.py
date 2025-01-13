from datetime import datetime
from Tables import Users, Questions, Status

def validate_user(username, password):
    if not username.strip() or not password.strip():
        return False, "You need to fill in all fields provided to proceed"
    for user in Users:
        if user["username"] == username and user["password"] == password:
            user["status"] = 1
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
        while index < len(Users) and valid_username and valid_password:
            valid_username = not Users[index]["username"] == username
            valid_password = not Users[index]["password"] == password
            index += 1  
        if valid_username and valid_password:
            new_entry = [
                {
                    'name': first_name,
                    'surname': last_name,
                    'username': username,
                    'password': password,
                    'repeat_preference': 1,
                    'age_category': age,
                    'level': 0,
                    'score': 0,
                    'streak': 0,
                    'days_summed': 0,   
                    'status': 1, 
                    'role': 'User',
                    'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]
    Questions.append(new_entry)

def record_status(username,focus_area,stress_level,time_available,suggestions):
    if not focus_area.strip() or not stress_level==0 or not time_available.strip() or not suggestions==0:
        return False, "You need to fill in all fields provided to proceed"
    else:
        new_entry = [
            {
                'username': username,
                'focus_area': focus_area,
                'stress_level': stress_level,
                'suggestions': suggestions,
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        Status.append(new_entry)
        return True, "Status recorded"
