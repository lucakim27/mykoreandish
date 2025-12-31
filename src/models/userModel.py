import logging
from google.cloud import firestore
from src.config.db import get_db
from src.utils.time import format_time_ago

class UserManager:
    def __init__(self):
        self.db = get_db()
        self.users_ref = self.db.collection('Users')

    def store_google_user(self, google_user_data: dict) -> None:
        google_id = google_user_data.get('id')
        name = google_user_data.get('name')

        try:
            user_ref = self.users_ref.document(google_id)
            user_doc = user_ref.get()

            if user_doc.exists:
                user_ref.update({
                    'name': name,
                    'last_login': firestore.SERVER_TIMESTAMP
                })
            else:
                user_ref.set({
                    'admin': False,
                    'email': "",
                    'google_id': google_id,
                    'name': name,
                    'dietary_preference': "",
                    'friends': [],
                    'last_login': firestore.SERVER_TIMESTAMP,
                    'created_at': firestore.SERVER_TIMESTAMP
                })
            
            logging.info(f"User {name} stored successfully!")
        except Exception as e:
            logging.error(f"Error storing user: {e}")
    
    def get_total_users(self):
        return self.users_ref.count().get()[0][0].value
    
    def get_all_users(self) -> list[dict]:
        try:
            user_docs = self.users_ref.order_by('created_at', direction=firestore.Query.DESCENDING).stream()
            users = [{
                'google_id': doc.get('google_id'),
                'created_at': format_time_ago(doc.get('created_at')),
                'name': doc.get('name')} for doc in user_docs]
            return users
        except Exception as e:
            logging.error(f"Error retrieving all users: {e}")
            return []
    
    def get_user_by_id(self, user_id: str) -> dict | None:
        try:
            user_ref = self.users_ref.where('google_id', '==', user_id)
            user_docs = user_ref.get()

            if user_docs:
                user_data = user_docs[0].to_dict()
                user_data['created_at'] = format_time_ago(user_data.get('created_at'))
                user_data['last_login'] = format_time_ago(user_data.get('last_login'))
                return user_data
            else:
                logging.info(f"No user found with google_id {user_id}")
                return None
        except Exception as e:
            logging.error(f"Error retrieving user by id: {e}")
            return None
    
    def update_dietary_preference(self, user_id, dietary_preference: str) -> bool:
        try:
            user_ref = self.users_ref.document(user_id)
            user_doc = user_ref.get()

            if user_doc.exists:
                user_ref.update({
                    'dietary_preference': dietary_preference
                })
                logging.info(f"Updated dietary preferences for user {user_id}")
                return True
            else:
                logging.info(f"No user found with google_id {user_id}")
                return False
        except Exception as e:
            logging.error(f"Error updating dietary preferences: {e}")
            return False