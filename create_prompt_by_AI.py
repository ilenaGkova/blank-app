import re
import json
from mongo_connection import User, Status, Question_Questionnaire, Question, Favorite_Recommendation, \
    Removed_Recommendation, Recommendation, Recommendation_Per_Person
from check_and_balance import get_status
from generate_items import generate_recommendation_id, calculate_fail_count
from add_data_in_collection import add_recommendation
from generate_recommendations_functions import enter_recommendation_for_user, generate_valid_index
from initialise_variables import con_question
from langchain.schema import HumanMessage
from langchain.schema import SystemMessage
import os
from langchain.chat_models import init_chat_model


# This function generates a required amount of recommendations by setting a prompt in an openAI machine
def generate_recommendations_by_AI(passcode, entries_generated_by_AI, key):

    index = 0  # Set to the index to indicate we added a recommendation to the user to keep track of how many

    while index < entries_generated_by_AI:

        outcome, new_recommendation = return_prompt(passcode, key)

        fail_count = 0  # We have a minor fail count to keep track if the recommendation was added, we probably won't have to use it unless we have various users doing this at the same time

        recommendation_added = False

        if outcome:

            description, title = extract_json(new_recommendation, create_prompt(passcode))

            while fail_count <= calculate_fail_count() and not recommendation_added:  # We have a maximum of 100 attempts to enter the recommendations

                recommendation_generated_id = generate_recommendation_id()  # Generate an ID for a new recommendation in the Recommendation collection, this means that future users will be able to see this generated recommendation

                recommendation_added, recommendation_added_message = add_recommendation(recommendation_generated_id,
                                                                                        "OpenAI",
                                                                                        title, description, None,
                                                                                        10)  # We enter OpenAI as the passcode of the creator

                if recommendation_added:

                    enter_recommendation_for_user(passcode, recommendation_generated_id, fail_count,
                                                  'A')  # Add the recommendation with Category A, aka generated by OpenAI

                else:

                    fail_count += 1  # Increase the minor fail count

        if not recommendation_added:
            enter_recommendation_for_user(passcode, generate_valid_index(), fail_count,
                                          'A-')  # Add the recommendation with Category A-, aka chosen by algorithm when is should have been generated by OpenAI

        index += 1  # Increase to the index to indicate we added a recommendation to the user to keep track of how many

    return index


def create_prompt(passcode):
    return (
        f"We have a user in an application. We require one (1) recommendation for the user to release stress today. "
        f"We have information on the user following:"
        f"\n----------------\n"
        f"{generate_user_profile(passcode)}"
        f"\n----------------\n"
        f"Please return your  answer exclusively in one (1) JSON request containing a title and a description. "
        f"A sample answer would look like this:\n"
        f"{{\n"
        f"    'Title': 'This is a title',\n"
        f"    'Description': 'This is a description'\n"
        f"}}"
    )


def return_prompt(passcode, key):

    if not os.environ.get("GROQ_API_KEY"):
        os.environ["GROQ_API_KEY"] = key

    model = init_chat_model("llama3-8b-8192", model_provider="groq")

    try:

        messages = [
            SystemMessage(content=(
                "You are an assistant that helps users reduce stress with actionable, personalized recommendations. "
                "Always return exactly one (1) JSON object with a 'Title' and a 'Description' field. "
                "Do not include anything outside of the JSON structure. Please escape all special characters, and wrap the JSON in a code block so it is valid."
            )),
            HumanMessage(content=create_prompt(passcode))
        ]

        new_recommendation = model.invoke(messages)

        return True, new_recommendation

    except Exception as e:

        return True, str(e)


def extract_json(new_recommendation, prompt):
    try:

        new_recommendation = new_recommendation.content

        if new_recommendation.startswith(prompt):  # Remove prompt from the response
            new_recommendation = new_recommendation[len(prompt):]

        match = re.search(r'\{.*?\}', new_recommendation, re.DOTALL)  # Try to extract JSON from the response

        if match:

            json_str = match.group(0)

            json_str_cleaned = json_str.replace("'", '"')  # Convert single quotes to double quotes

            try:
                response_json = json.loads(json_str_cleaned)

                title = response_json.get("Title", "Untitled")
                description = response_json.get("Description", new_recommendation)

            except json.JSONDecodeError:

                title = "Invalid Format"
                description = json_str_cleaned

        else:

            title = "No JSON Found"
            description = new_recommendation

    except Exception as e:

        return "Error", str(e)

    return description, title


# This function generates a user profile to be added to a prompt to an AI, and a condition to indicate if it did it correctly
def generate_user_profile(passcode):
    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode

    # Find the last status the user made (look in the function for more) and make sure we enter the right amount if return variables

    today, yesterday, index = get_status(passcode)

    if not today:  # If the user hasn't made a status, we can't generate a profile for them

        return 'Something went wrong, status was not found'

    status = Status.find_one({"_id": index})

    stress_level = status['Stress_Level']  # Find the status to find the stress level

    data = Recommendation_Per_Person.find({"Passcode": passcode, "Status_Created_At": status['Created_At']})

    previous_recommendations = []

    for entry in data:

        if Recommendation.find_one({"ID": entry['ID']}):
            previous_recommendations.append(
                {
                    'Recommendation': Recommendation.find_one({"ID": entry['ID']})['Description']
                }
            )

    answers = []  # Initialise table
    history = []  # Initialise table

    Question_Questionnaire_list = list(Question_Questionnaire.find())

    for entry in Question_Questionnaire_list:

        if Question.find_one({"Passcode": passcode, "Question": entry['Question']}, sort=[("Created_At", -1)]):
            answers.append(
                # The table will hold the latest answer to a questionnaire question
                {
                    'Question': entry['Question'],
                    'Answer': Question.find_one({"Passcode": passcode, "Question": entry['Question']},
                                                sort=[("Created_At", -1)])['Answer']
                }
            )
            data = list(Question.find({"Passcode": passcode, "Question": entry['Question']}))
            for sub_entry in data:
                history.append(
                    # The table will hold all the answers the user has given, ever
                    {
                        'Question': entry['Question'],
                        'Answers': sub_entry['Answer'],
                        'Created_at': sub_entry['Created_At']
                    }

                )

    data = list(
        Recommendation.find({"Passcode": passcode}))  # Gathering user preferences by checking recommendations we have
    preferences = []  # Initialise table

    for entry in data:

        if Favorite_Recommendation.find({"Passcode": passcode, "ID": entry['ID']}) or Removed_Recommendation.find(
                {"Passcode": passcode,
                 "ID": entry['ID']}):  # We see if it is either category, can be on only one by design

            preferences.append(
                # This table holds the user's preferences
                {
                    'Preference': (
                        'User liked this recommendation' if Favorite_Recommendation.find(
                            {"Passcode": passcode, "ID": entry['ID']}) is not None
                        else "User didn't like this recommendation"
                    ),
                    'Recommendation': entry['Description']
                }

            )

    data = list(Question.find({"Passcode": passcode, "Question": con_question}))
    confessions = []  # Initialise table

    for entry in data:
        confessions.append(
            {
                'entry': entry['Answer']
            }
        )

    my_prompt = (
        f"User between the ages of {user['Age_Category']} has answered various questions about his experience with stress today. The questions and answers are in the table given here: {answers}."
        f"Based on his answers today we rated their stress level as {stress_level}."
        f"The user has identified {user['Focus_Area']} as the area mostly stressing them out, and has {user['Time_Available']} minutes free to do an activity today."
        f"Additionally we also have the user's answers to the stress related questions in the past in this table: {history}"
        f"We are also provided with the user's general thoughts, be aware this might be empty as the user might be new: {confessions}"
        f"Lastly we have a collection of the user has seen and has given feedback back, we have that information here: {preferences}"
        f"The user has already been given today the recommendations {previous_recommendations}. Please don't return any similar.")

    return my_prompt
