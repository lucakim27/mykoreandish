from flask import flash, logging
from src.config.db import get_db

class TasteManager:
    def __init__(self, firestore):
        self.db = get_db()
        self.firestore = firestore
        self.dishes_ref = self.db.collection('Dishes')
        self.users_ref = self.db.collection('Users')
        self.user_selections_ref = self.db.collection('UserSelections')
        self.ingredients_ref = self.db.collection('Ingredients')
        self.dietaries_ref = self.db.collection('Dietaries')

    def delete_history(self, history_id):
        if history_id:
            try:
                history_ref = self.user_selections_ref.document(history_id)
                history_ref.delete()
                flash('History item deleted successfully.', 'success')
            except Exception:
                flash('An error occurred while deleting the history item.', 'error')
        else:
            flash('Invalid history ID.', 'error')
    
    def get_dish_review_by_id(self, history_id):
        try:
            reviews_ref = self.db.collection("UserSelections")
            review_doc = reviews_ref.document(history_id).get()

            if review_doc.exists:
                review_data = review_doc.to_dict()
                dish_name = review_data.get("dish_name")
                spiciness = review_data.get("spiciness")
                sweetness = review_data.get("sweetness")
                sourness = review_data.get("sourness")
                temperature = review_data.get("temperature")
                texture = review_data.get("texture")
                rating = review_data.get("rating")
                healthiness = review_data.get("healthiness")

                return {
                    "dish_name": dish_name,
                    "spiciness": spiciness,
                    "sweetness": sweetness,
                    "sourness": sourness,
                    "temperature": temperature,
                    "texture": texture,
                    "rating": rating,
                    "healthiness": healthiness
                }
            else:
                return None
        except Exception as e:
            logging.error(f"Error retrieving dish review by id: {e}")
            return None

    def update_review(self, history_id, spiciness, sweetness, sourness, texture, temperature, healthiness, rating):
        if not history_id or not rating:
            flash('Invalid input for rating.', 'error')
            return False

        try:
            history_ref = self.user_selections_ref.document(history_id)
            history_ref.update({
                'rating': int(rating),
                'spiciness': int(spiciness),
                'sweetness': int(sweetness),
                'sourness': int(sourness),
                'texture': int(texture),
                'temperature': int(temperature),
                'healthiness': int(healthiness)
            })
            flash('Rating saved successfully!', 'success')
            return True
        except Exception as e:
            flash(f'Error saving rating: {e}', 'error')
            return False

    def add_taste_review(self, google_id, dish_name, spiciness, sweetness, sourness, texture, temperature, healthiness, rating):
        try:
            user_ref = self.users_ref.where('google_id', '==', google_id)
            user = user_ref.get()

            if not user:
                raise ValueError("User does not exist.")
            
            dish_ref = self.dishes_ref.document(dish_name)
            dish = dish_ref.get()
            
            if not dish:
                raise ValueError("Dish does not exist.")
            
            self.user_selections_ref.add({
                'google_id': google_id,
                'dish_name': dish_name,
                'spiciness': int(spiciness),
                'sweetness': int(sweetness),
                'sourness': int(sourness),
                'texture': int(texture),
                'temperature': int(temperature),
                'healthiness': int(healthiness),
                'rating': int(rating),
                'timestamp': self.firestore.SERVER_TIMESTAMP
            })
            flash('Taste review added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding taste review: {e}', 'error')

    def get_user_history(self, google_id):
        try:
            user_ref = self.users_ref.where('google_id', '==', google_id)
            user_docs = user_ref.get()

            if not user_docs:
                return []

            user = user_docs[0]

            user_selections_ref = self.user_selections_ref.where('google_id', '==', user.to_dict().get('google_id'))
            selections = user_selections_ref.stream()

            return [{
                'id': selection.id,
                'dish_name': selection.to_dict().get('dish_name'),
                'timestamp': selection.to_dict().get('timestamp'),
                'spiciness': selection.to_dict().get('spiciness'),
                'sourness': selection.to_dict().get('sourness'),
                'sweetness': selection.to_dict().get('sweetness'),
                'texture': selection.to_dict().get('texture'),
                'temperature': selection.to_dict().get('temperature'),
                'healthiness': selection.to_dict().get('healthiness'),
                'rating': selection.to_dict().get('rating')
            } for selection in selections]

        except Exception:
            return []