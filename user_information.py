from datetime import datetime
from mongo_connection import User, Recommendation, Recommendation_Per_Person, Favorite_Recommendation, \
    Removed_Recommendation
from generate_items import get_limits
from check_and_balance import new_entry_in_score_history_collection, new_entry_in_record_collection


# This function adds points when a user completes a recommendation.
def add_points(index, passcode, status, pointer):
    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode

    if not user:  # If we can't find the user we can't do anything about this points
        return False, "Something went wrong, user not found"

    recommendation = Recommendation.find_one({"ID": index})  # Find the recommendation the user completed

    if not recommendation:  # If we can't find the recommendation we can't find the points to add to a user
        return False, "Something went wrong, Recommendation not found"

    recommendation_per_person_entry = Recommendation_Per_Person.find_one(
        {"ID": index, "Passcode": passcode,
         "Status_Created_At": status})  # Find the assignment of the recommendation to the user

    if not recommendation_per_person_entry:  # If the recommendation wasn't given to the user something went wrong
        return False, "Something went wrong, Recommendation not found in given recommendations"

    move_up_threshold, move_down_threshold = get_limits(user[
                                                            'Level'])  # Step 1: Get the promotion / demotion point for the user's level. We do that to get the maximum score for a user

    points = user['Level'] * recommendation[
        'Points']  # Step 2: Get the points we will add the user based on the recommendation's points and the user's level

    maximum_points = move_up_threshold + 50 * user['Level']  # Step 3: Get the maximum limit of the user's points

    combined_points = user['Score'] + user['Level'] * recommendation[
        'Points']  # We add up the current score and the new points

    if combined_points <= maximum_points:  # Step 4: If the additional points will get the user over the limit we top their score and leave it there

        User.update_one({"Passcode": passcode}, {"$set": {"Score": combined_points}})  # Update the user score

    else:

        User.update_one({"Passcode": passcode}, {"$set": {"Score": maximum_points}})  # Update the user score

        points = maximum_points - combined_points  # We are using the variable to keep track of how many points were added to the user

    Recommendation_Per_Person.update_one({"ID": index, "Passcode": passcode, "Status_Created_At": status, "Pointer": pointer}, {
        "$set": {"Outcome": False, "Completed_At": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")}})  # Update the recommendation outcome to add the completion timestamp and change the outcome

    new_entry_in_score_history_collection(passcode)

    new_entry_in_record_collection(passcode, f"User {passcode} increased their score by {points} points", "S")

    new_entry_in_record_collection(passcode, f"User {passcode} completed recommendation {index}", "C")

    return True, f"User {passcode} increased their score by {points} points"


# This function removes a recommendation from a favorite / removed status and maybe add them to another
def change_recommendation_preference_for_user(preference, passcode, index, just_remove=None):
    # This function returns a condition as to if it completed the function needed of it and a message

    if User.count_documents({
            "Passcode": passcode}) == 0:  # If we can't find the user we can't do anything about adding a connotation to a recommendation for them
        return False, "Something went wrong, user not found"

    if Recommendation.count_documents(
            {"ID": index}) == 0:  # If we can't find the recommendation we can't do anything about it either
        return False, "Something went wrong, Recommendation not found"

    # A recommendation can be in one of the below collections, so we don't need to look, we can delete from both and only one will be not None
    Favorite_Recommendation.delete_one({"ID": index, "Passcode": passcode})
    Removed_Recommendation.delete_one({"ID": index, "Passcode": passcode})

    if just_remove is True:  # Maybe we don't want to add the recommendation everywhere, so we stop early
        return True, "Task Completed"

    # Each collection has the same structure. We have a user's passcode, a recommendation ID and a time stamp
    # Key attributes can be Passcode and ID or Passcode and Created_At, both can work
    new_entry = {
        'Passcode': passcode,
        'ID': index,
        'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if preference == -1:  # Depending on the preference (1 for recommendation was in favorites and -1 for removed) we enter the recommendation in the OTHER collection
        Removed_Recommendation.insert_one(new_entry)
    else:
        Favorite_Recommendation.insert_one(new_entry)

    return True, "Task Completed"


# This function gets data for a user profile and updates the user profile in the collection for users
def update_user(passcode, username, repeat, age, focus_area, time_available, suggestions):
    # This function returns in boolean indicator that the function completed a task and a message for the user
    # The message will be shown if the function failed

    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode

    if not user:
        return False, "Something went wrong, user not registered"  # End function early if the user isn't registered

    if User.find_one({"Username": username}) and username != user['Username']:
        return False, "You need to enter a unique username"  # End early is also the user has submitted a new username that already exists

    if not focus_area.strip() or time_available == 0 or suggestions == 0 or repeat == 0 or not age.strip():
        return False, "You need to enter appropriate information"  # End early if any other data is inappropriate, there are safeguards in place to avoid that placed in the application but still

    User.update_one({"Passcode": passcode}, {
        "$set":
            {
                "Username": username,
                "Repeat_Preference": repeat,
                "Age_Category": age,
                "Focus_Area": focus_area,
                "Suggestions": suggestions,
                "Time_Available": time_available
            }
    }
                    )  # Find the user and update their profile with a new data

    new_entry_in_record_collection(passcode,
                                   f"User {passcode} updated their profile: Username {username}, Repeat Preference {repeat}, Age {age}, focus {focus_area}, suggestions {suggestions}, time available {time_available}",
                                   "P")

    return True, "User Profile Updated"
