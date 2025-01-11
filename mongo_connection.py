from Tables import Users

def validate_user(username, password):
    if not username.strip() or not password.strip():
        return False, "You need to fill in all fields provided to proceed"
    for user in Users:
        if user["username"] == username and user["password"] == password:
            user["status"] = 1
            return True, "You have an account"
    return False, "You do not have an account"

def new_user(first_name,last_name,username,password,chosen):
    if not first_name.strip() or not last_name.strip() or not username.strip() or not password.strip() or not chosen.strip():
        return False, "You need to fill in all fields provided to proceed"
    else:
        valid_username = True
        valid_password = True
        index = 0
        while index < len(Users) and valid_username and valid_password:
            valid_username = not Users[index]["username"] == username
            valid_password = not Users[index]["password"] == password
            index += 1  
        if valid_username and valid_password:
            new_user = [
                {
                    'name': first_name,
                    'surname': last_name,
                    'username': username,
                    'password': password,
                    'repeat_preference': 1,
                    'age_category': chosen,
                    'level': 0,
                    'score': 0,
                    'streak': 0,
                    'days_summed': 0,   
                    'status': 1, 
                    'role': 'User'
                }
            ]
            Users.append(new_user)
            return True, "You have been added to our service"
        elif valid_username and not valid_password:
            return False, "You need to enter a unique username"
        elif not valid_username and valid_password:
            return False, "You need to enter a unique password"
        else:
            return False, "You need to enter a unique username and password"
