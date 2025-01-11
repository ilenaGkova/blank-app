from Tables import get_users

def validate_user(username, password):
    users = users.extend(get_users())
    if not username.strip() or not password.strip():
        return False
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True
    return False
