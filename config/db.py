# db.py
from firebase_admin import credentials, firestore, initialize_app

# Load credentials and initialize Firestore
# cred = credentials.Certificate("/etc/secrets/credentials.json") # production
cred = credentials.Certificate('credentials.json') # local environment

initialize_app(cred)
db = firestore.client()