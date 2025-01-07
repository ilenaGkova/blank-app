import streamlit as st
from pymongo import MongoClient

host = "localhost"  # The host part of the MongoDB URI
port = 27017  # The port number, extracted from the URI
username = "E20030"  # Replace with your MongoDB username
password = "E20030"  # Replace with your MongoDB password

# Define Starter Data
Users = [
    {'name': 'Ilena',
     'surname': 'Gkova',
     'username': 'Admin',
     'passowrd': 'Admin123',
     'repeat_preference': 5,
     'age_category': '18-25',
     'level': 1,
     'score': 500,
     'streak': 0,
     'days_summed': 0,   
     'status': 2, 
     'role': 'Admin'},
]

def get_database():
    client = client = MongoClient(host=host, port=port, username=username, password=password)
    return client.StressTest

def insert_starter_data():
    data = get_database
    collection = data['StressUser']
    for entries in Users:
        if collection.count_documents({'username': entries['username']}) == 0:
            print(f"Inserting data for user: {entries['username']}...")
            try:
                data['StressUser'].insert_one(data)
            except Exception as e:
                print(f"Error inserting data: {e}")
        else:
            print(f"Data for user: {data['username']} already exists. Skipping insert.")
    return True
