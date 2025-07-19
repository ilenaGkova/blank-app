from datetime import datetime, timedelta
from mongo_connection import Record, User, Status
from check_and_balance import get_status, new_entry_in_record_collection, new_entry_in_score_history_collection
from generate_items import get_limits


# This function checks and will increase the continuous days connected for a user, as given by a Passcode
def update_user_streak(passcode):
    # This function returns a message for the outcome of the function to show the user

    if not User.find_one({"Passcode": passcode}):
        return "Something went wrong, user not registered."  # Make sure the user is registered first - another thing that probably won't happen since this function won't be called then

    latest_change = Record.find_one({"Passcode": passcode, "Type": "C"}, sort=[("Created_At",-1)])

    if latest_change is not None:

        latest_change_time = datetime.strptime(latest_change['Created_At'],'%Y-%m-%d %H:%M:%S')

        now = datetime.now()

        if now.date() == latest_change_time.date():  # If there was a type C action made for the user we need to make sure it didn't happen today

            return "You have already signed in today, your streak will not change."

        if (now.date() - latest_change_time.date()).days == 1:

            User.update_one({"Passcode": passcode},
                            {"$inc": {"Days_Summed": 1}})  # We need to increase the days connected for the user anyway

            User.update_one({"Passcode": passcode}, {
                "$inc": {"Streak": 1}})  # yesterday means the user was here yesterday, so we increase their streak

            message = "Your streak was increased."  # Custom a message for the user

            streak_action = f"Streak increased for user {passcode}"  # Custom the action done for the streak

        else:

            User.update_one({"Passcode": passcode},
                            {"$inc": {"Days_Summed": 1}})  # We need to increase the days connected for the user anyway

            User.update_one({"Passcode": passcode}, {
                "$set": {"Streak": 1}})  # Since we are here the user wasn't here yesterday so the streak was reset

            message = "You did not check in less than 48 hours ago. Your streak was reset."  # Custom a message for the user

            streak_action = 'Streak reset'  # Custom the action done for the streak

    else:

        User.update_one({"Passcode": passcode},
                        {"$inc": {"Days_Summed": 1}})  # We need to increase the days connected for the user anyway

        User.update_one({"Passcode": passcode}, {
            "$inc": {"Streak": 1}})  # yesterday means the user was here yesterday, so we increase their streak

        message = "Your streak was increased."

        streak_action = f"Streak increased for user {passcode}"

    new_entry_in_record_collection(passcode, streak_action, "C")

    new_entry_in_record_collection(passcode, f"Days connected increased for user {passcode}", "C")

    return message


# This function returns True if the action type D, score being reset to 0 after a level change, needs to happen
def get_record(passcode):
    if not User.find_one({"Passcode": passcode}):  # Obviously we can't do anything without the user being valid
        return False

    today = datetime.today().date()  # Get today's date

    week_start = today  # Set the week start being today
    if not today.weekday() == 0:  # If today isn't monday we go back to the monday
        week_start = today - timedelta(days=today.weekday())  # today.weekday() is assigning a number to a day

    return Record.find_one({"Passcode": passcode, "Type": "S",
                            # True means the action hasn't happened and that there was a status made for a user. True will mean we need to assess the user levels
                            "Created_At": {"$gte": week_start.isoformat()}}) is None and Status.count_documents(
        {"Passcode": passcode}) > 1


# This function makes changes in a user's score and level. This should happen weekly. It will return a message to the user
def determine_level_change(passcode):
    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode

    if not user:  # If the user isn't registered we can't get their level or their profile
        return "Something went wrong, user not registered"

    move_up_threshold, move_down_threshold = get_limits(
        user['Level'])  # Get the promotion / demotion point for the user's level

    # We set up 2 messages related to the change that happened to the level, one will be for the user, one will be for the record
    message_for_user = f"You have remained at level {user['Level']}."
    message_for_system = f"User remained at level {user['Level']}."

    if user["Score"] > move_up_threshold and user['Level'] < 25:

        User.update_one({"Passcode": passcode}, {"$inc": {"Level": 1}})  # The user moves up a level
        user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode

        # We set up 2 messages related to the change that happened to the level, one will be for the user, one will be for the record
        message_for_user = f"You have moved up to level {user['Level']}."
        message_for_system = f"User {passcode} moved up to level {user['Level']}"

    elif user["Score"] < move_down_threshold:

        if user["Level"] != 1:  # The user moved down a level, we keep 1 as the minimum

            User.update_one({"Passcode": passcode}, {"$inc": {"Level": -1}})
            user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode

            # We set up 2 messages related to the change that happened to the level, one will be for the user, one will be for the record
            message_for_user = f"You have been demoted to level {user['Level']}."
            message_for_system = f"User {passcode} has been demoted to level {user['Level']}"

        else:

            # We set up 2 messages related to the change that happened to the level, one will be for the user, one will be for the record
            message_for_user = "You have been demoted but remained at level 1."
            message_for_system = f"User {passcode} was demoted but remained at level 1"

    new_entry_in_record_collection(passcode, message_for_system, "S")

    number = get_reset_score(user["Score"], user["Level"])

    User.update_one({"Passcode": passcode},
                    {"$set": {"Score": number}})  # We reset the user's score to 0 to start over on this level

    new_entry_in_score_history_collection(passcode)

    new_entry_in_record_collection(passcode, message_for_system, "S")

    return message_for_user


def get_reset_score(current_score, new_level, task_base=25, max_weekly_tasks=50):
    move_up_threshold, move_down_threshold = get_limits(new_level)
    points_per_task = task_base * new_level
    max_weekly_points = points_per_task * max_weekly_tasks

    target_score = max(move_up_threshold - max_weekly_points, 0)

    # Calculate carryover percentage
    carryover_percentage = min(5 + new_level, 35) / 100
    carryover_points = (current_score - move_up_threshold) * carryover_percentage if current_score > move_up_threshold else 0

    target_score += max(carryover_points, 0)

    # Ensure under demotion threshold
    if target_score >= move_down_threshold:
        target_score = move_down_threshold - 1

    return max(int(target_score), 0)
