from datetime import datetime
from mongo_connection import User, Recommendation, Tag, Question_Questionnaire, Recommendation_Per_Person
from generate_items import get_now


def add_recommendation(ID, passcode, title, description, link, points, duration):
    ID = int(ID)  # Convert any possible IDs in text into numbers

    if not User.find_one(
            {"Passcode": passcode}):  # If we can't find the user we can add a recommendation on their behalf

        return False, "Something went wrong, user not registered"

    if Recommendation.find_one({"ID": ID}) or Tag.find_one(
            {"ID": ID}) or Recommendation_Per_Person.find_one({"ID": ID}):  # If the ID matches any of the Tags or other Recommendations we can't add it

        return False, "Please try again, it look like the ID generated has already been added."

    if not title.strip() or not description.strip() or points <= 0 or points > 150 or (
            link is not None and not link.strip()) or duration <= 0:
        return False, "You need to fill in all mandatory fields"  # Make sure the data entered are appropriate to be added

    # This collection's entries contain an ID that can be used as a key to find the entry across the collections
    # It also includes the passcode of the user that added it and a timestamp for when it was created
    # The content is a title, a description, a link that is optional and minimum points assigned to them

    Recommendation.insert_one(
        {
            'ID': ID,
            'Passcode': passcode,
            'Created_At': get_now(),
            'Title': title,
            'Description': description,
            'Link': link,
            'Points': points
        }
    )

# This function adds a tag to a recommendation, it returns an indicator that shows whether the function completed and a message
def add_tag(ID, passcode, title, category):
    ID = int(ID)  # Convert any possible IDs in text into numbers

    if not User.find_one(
            {"Passcode": passcode}):  # If we can't find the user we can add a recommendation on their behalf

        return False, "Something went wrong, user not registered"

    if not Recommendation.find_one({"ID": ID}):  # We can't add a tag to a recommendation that doesn't exist

        return False, "Something went wrong, recommendation not found"

    if Tag.find_one({"ID": ID, "Title_Of_Criteria": title, "Category": category}):  # We can't add a tag twice

        return False, "Tag already exists"

    # This collection identifies an entry by 3 to maybe 4 attributes
    # The ID of the recommendation given this Tag, the criteria title and value (Category)
    # Other attributes that seperate an entry is a timestamp of creation and the passcode of the person that added it

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


# This function enters a question in the daily stress questionnaire
def add_question_to_Questionnaire(ID, passcode, question_input):
    ID = int(ID)  # Just in case make sure the ID is a number

    if not User.find_one({"Passcode": passcode}):  # Make sure the user is registered
        return False, "Something went wrong, user not registered"

    if Question_Questionnaire.find_one({"ID": ID}):  # Can't have two same IDs in the same collection
        return False, "ID already exists"

    if Question_Questionnaire.find_one({"Question": question_input}):
        return False, "Question already exists"  # Can't have the same exact question

    if not question_input.strip():  # Can't enter an empty question
        return False, "You need to enter a question"

    Question_Questionnaire.insert_one(
        {
            'ID': ID,  # The collection has multable attributes, use ID it identify the entries
            'Passcode': passcode,  # Save the creator of the question
            'Question': question_input,  # Use the question as another key of the entry
            'Created_At': get_now(),  # Timestamp of creation
        }
    )
    return True, "Question added"
