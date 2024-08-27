import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv  # pip install python-dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch the Firebase configuration from environment variable
firebase_config = os.getenv('FIREBASE_CONFIG')

if firebase_config:
    # Convert the JSON string back to a dictionary
    firebase_config_dict = json.loads(firebase_config)
    
    # Initialize Firebase app using the dictionary
    cred = credentials.Certificate(firebase_config_dict)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
else:
    raise ValueError("FIREBASE_CONFIG environment variable is not set.")

def fetch_all_periods():
    periods_ref = db.collection("periods")
    periods = periods_ref.stream()
    return [period.id for period in periods]

def insert_period(period, incomes, expenses, comment):
    doc_ref = db.collection("periods").document(period)
    doc_ref.set({
        "incomes": incomes,
        "expenses": expenses,
        "comment": comment
    })

def get_period(period):
    doc_ref = db.collection("periods").document(period)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None
