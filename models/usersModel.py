import logging

class User:
    def __init__(self, google_id: str, name: str, email: str):
        self.google_id = google_id
        self.name = name
        self.email = email

class UserManager:
    def __init__(self, db):
        self.db = db
        self.users_ref = db.collection('Users')

    def store_google_user(self, google_user_data: dict) -> None:
        """
        Store user data in Firebase Firestore.
        
        :param google_user_data: Dictionary containing Google user data
        """
        google_id = google_user_data.get('id')
        name = google_user_data.get('name')
        email = google_user_data.get('email')

        try:
            # Check if the user already exists in Firestore
            user_ref = self.users_ref.document(google_id)
            user_doc = user_ref.get()

            user = User(google_id, name, email)

            if user_doc.exists:
                # If the user exists, update their data
                user_ref.update({
                    'email': user.email,
                    'google_id': user.google_id,
                    'name': user.name
                })
            else:
                # If the user doesn't exist, add new user
                user_ref.set({
                    'admin': False,
                    'email': user.email,
                    'google_id': user.google_id,
                    'name': user.name
                })
            
            logging.info(f"User {user.name} stored successfully!")
        except Exception as e:
            logging.error(f"Error storing user: {e}")

    def get_user_by_session(self, session: dict) -> dict:
        """
        Get user details by session's google_id.

        :param session: Flask session containing the google_id
        :return: Dictionary containing user data or None if not found
        """
        if session is None:
            logging.warning("Session is None")
            return None

        google_id = session.get('google_id')
        if google_id:
            try:
                # Query to get the user by google_id from the session
                user_ref = self.users_ref.where('google_id', '==', google_id)
                user_docs = user_ref.get()

                if user_docs:
                    # Assuming only one user document matches, get the first document
                    user_data = user_docs[0].to_dict()
                    return user_data
                else:
                    logging.info(f"No user found with google_id {google_id}")
                    return None
            except Exception as e:
                logging.error(f"Error retrieving user: {e}")
                return None
        else:
            logging.warning("No google_id found in session")
            return None