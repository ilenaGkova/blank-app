from mongo_connection import Recommendation
from generate_items import generate_recommendation_id, calculate_fail_count, get_now
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
import streamlit as st
import re
import os
import json


def update_sample():

    list_of_samples = list(Recommendation.find(
        {'Passcode': "Gemini", 'Prompt': {'$exists': True}, 'Answer': {'$exists': True}}))  # Get all relevant entries

    pointer = 1  # Used to assign a unique number to each recommendation

    # Update each document with a new "Pointer"
    for entry in list_of_samples:
        Recommendation.update_one(
            {'ID': entry['ID']},
            {'$set': {'Pointer': pointer}}
        )
        pointer += 1


def delete_samples():
    Recommendation.delete_many(
        {'Passcode': "Groq", 'Prompt': {'$exists': True}, 'Answer': {'$exists': True}, 'Pointer': {'$exists': True}})


def add_samples():

    gemini_samples = list(Recommendation.find(
        {'Passcode': "Gemini", 'Prompt': {'$exists': True}, 'Answer': {'$exists': True}, 'Pointer': {'$exists': True}}))

    for entry in gemini_samples:

        print(f"Currently on pointer {entry['Pointer']}")

        if Recommendation.find_one({'Passcode': "Groq", 'Prompt': {'$exists': True}, 'Answer': {'$exists': True}, 'Pointer': entry['Pointer']}) is None:

            outcome, new_recommendation, prompt = use_groq(entry)

            fail_count = 0  # We have a minor fail count to keep track if the recommendation was added, we probably won't have to use it unless we have various users doing this at the same time

            recommendation_added = False

            if outcome:  # Add recommendation only of one was generated

                condition, title, description, duration = extract_json(new_recommendation, entry['Prompt'])

                print(f"|{condition}|, |{title}|, |{description}|, |{duration}|, |{new_recommendation}|")

                while fail_count <= calculate_fail_count() and not recommendation_added and condition:  # We have a maximum of 100 attempts to enter the recommendations

                    try:
                        Recommendation.insert_one(
                            {
                                'ID': generate_recommendation_id(),
                                'Passcode': "Groq",
                                'Created_At': get_now(),
                                'Title': title,
                                'Description': description,
                                'Link': None,
                                'Points': duration * 2,
                                'Prompt': prompt,
                                'Answer': str(new_recommendation),
                                'Pointer': entry['Pointer']
                            }
                        )

                        recommendation_added = True

                    except Exception as e:
                        print(str(e))  # Print problem with recommendation generation
                        recommendation_added = False

                    if not recommendation_added:

                        fail_count += 1  # Increase the minor fail count

            if not recommendation_added:

                print(f"[ABORT] Groq failed on pointer {entry['Pointer']}.")
                break  # ❌ ABORT immediately


def use_groq(entry):
    try:
        if not os.environ.get("GROQ_API_KEY"):
            os.environ["GROQ_API_KEY"] = st.secrets["API"]["groqkey"]  # Find groq key in secret file

        model = init_chat_model(
            "llama-3.3-70b-versatile",  # Specify model
            model_provider="groq"
        )

        messages = [  # Structure model messages
            SystemMessage(content=(
                "You are an assistant that helps users reduce stress with actionable, personalized recommendations. "
                "Respond only with a valid JSON object matching the schema. No markdown, no explanations, no code blocks."
            )),  # Work on tone and model role
            HumanMessage(content=entry['Prompt'])  # Add generated prompt
        ]

        result = model.invoke(messages)  # Call model to generate recommendation

        return True, result, entry['Prompt']   # Return new recommendation

    except Exception as e:
        print(str(e))  # Print problem with recommendation generation
        return False, str(e), None  # Return problem with recommendation generation


def extract_json(new_recommendation, prompt):
    try:
        text = getattr(new_recommendation, "content", str(new_recommendation)).strip()

        if text.startswith(prompt):
            text = text[len(prompt):].strip()

        match = re.search(r'\{[\s\S]*?\}', text)

        if not match:
            return False, "No JSON Found", text.strip(), 5

        json_str = match.group(0)

        # Attempt regular JSON parse first
        try:
            response_json = json.loads(json_str)
        except json.JSONDecodeError:
            try:
                # Targeted replacement: only keys, not all single quotes
                json_str_fixed = json_str

                # Replace 'Title': with "Title":
                json_str_fixed = re.sub(r"'Title'\s*:", r'"Title":', json_str_fixed)
                json_str_fixed = re.sub(r"'Description'\s*:", r'"Description":', json_str_fixed)
                json_str_fixed = re.sub(r"'Duration'\s*:", r'"Duration":', json_str_fixed)

                # Also replace ': int(' with ': '
                json_str_fixed = re.sub(r": int\(", r": ", json_str_fixed)
                json_str_fixed = json_str_fixed.replace(")", "")

                response_json = json.loads(json_str_fixed)
            except Exception:
                return False, "Invalid Format", json_str.strip(), 5

        title = response_json.get("Title", "Untitled")
        description = response_json.get("Description", text.strip())
        duration = response_json.get("Duration", 5)

        try:
            duration = int(duration)
        except (ValueError, TypeError):
            duration = 5

        return True, title, description, duration

    except Exception as e:
        return False, "Error", f"{str(e)}\n\nRaw Output:\n{str(new_recommendation)}", 5

