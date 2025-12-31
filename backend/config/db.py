import os
import firebase_admin
from firebase_admin import credentials, firestore

_db = None

def get_db():
    global _db

    if _db is not None:
        return _db

    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    if cred_path is None:
        cred_path = os.path.join(
            os.path.dirname(__file__), 
            "../..", 
            "credentials.json"
        )

    if not os.path.exists(cred_path):
        raise RuntimeError(f"Firebase credential file not found: {cred_path}")

    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

    _db = firestore.client()
    return _db
