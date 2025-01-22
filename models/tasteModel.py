from flask import flash

class Taste:
    def __init__(self, history_id, dish_name, rating=None):
        self.history_id = history_id
        self.dish_name = dish_name
        self.rating = rating

class TasteManager:
    def __init__(self, db, firestore):
        self.db = db
        self.firestore = firestore
        self.dishes_ref = db.collection('Dishes')
        self.users_ref = db.collection('Users')
        self.user_selections_ref = db.collection('UserSelections')
        self.ingredients_ref = db.collection('Ingredients')
        self.dietaries_ref = db.collection('Dietaries')

    def delete_history(self, history_id):
        """Delete a history item from the 'UserSelections' collection."""
        try:
            history_ref = self.user_selections_ref.document(history_id)
            history_ref.delete()
            flash('History item deleted successfully.', 'success')
            return True
        except Exception as e:
            flash('An error occurred while deleting the history item.', 'error')
            print(f"Error: {e}")
            return False

    def update_review(self, history_id, spiciness, sweetness, sourness, texture, temperature, healthiness, rating):
        """Rate a dish by updating its rating in the 'UserSelections' collection."""
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
        
    def get_dish_rating(self, dish_name):
        try:
            total_rating, count_rating = 0, 0
            total_spiciness, count_spiciness = 0, 0
            total_sweetness, count_sweetness = 0, 0
            total_texture, count_texture = 0, 0
            total_healthiness, count_healthiness = 0, 0
            total_sourness, count_sourness = 0, 0
            total_temperature, count_temperature = 0, 0

            selections = self.user_selections_ref.where('dish_name', '==', dish_name).stream()

            for selection in selections:
                selection_data = selection.to_dict()

                if (rating := selection_data.get('rating')) is not None:
                    total_rating += rating
                    count_rating += 1

                if (spiciness := selection_data.get('spiciness')) is not None:
                    total_spiciness += spiciness
                    count_spiciness += 1

                if (sweetness := selection_data.get('sweetness')) is not None:
                    total_sweetness += sweetness
                    count_sweetness += 1

                if (texture := selection_data.get('texture')) is not None:
                    total_texture += texture
                    count_texture += 1

                if (healthiness := selection_data.get('healthiness')) is not None:
                    total_healthiness += healthiness
                    count_healthiness += 1

                if (sourness := selection_data.get('sourness')) is not None:
                    total_sourness += sourness
                    count_sourness += 1

                if (temperature := selection_data.get('temperature')) is not None:
                    total_temperature += temperature
                    count_temperature += 1

            average_rating = total_rating / count_rating if count_rating else None
            average_spiciness = total_spiciness / count_spiciness if count_spiciness else None
            average_sweetness = total_sweetness / count_sweetness if count_sweetness else None
            average_texture = total_texture / count_texture if count_texture else None
            average_healthiness = total_healthiness / count_healthiness if count_healthiness else None
            average_sourness = total_sourness / count_sourness if count_sourness else None
            average_temperature = total_temperature / count_temperature if count_temperature else None

            return {
                "average_rating": average_rating,
                "average_spiciness": average_spiciness,
                "average_sweetness": average_sweetness,
                "average_texture": average_texture,
                "average_healthiness": average_healthiness,
                "average_sourness": average_sourness,
                "average_temperature": average_temperature,
            }

        except Exception as e:
            print(f"Error fetching dish statistics: {e}")
            return None

    def add_selection(self, google_id, dish_name, spiciness, sweetness, sourness, texture, temperature, healthiness, rating):
        """Add a food selection without a rating initially."""
        user_ref = self.users_ref.where('google_id', '==', google_id)
        user = user_ref.get()

        if not user:
            raise ValueError("User does not exist.")
        
        dish_ref = self.dishes_ref.document(dish_name)
        dish = dish_ref.get()
        
        if not dish:
            raise ValueError("User does not exist.")
        
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

        except Exception as e:
            print(f"Error retrieving user history: {e}")
            return []
    
    def filter_search(self, ingredient=None, dietary=None):
        if ingredient is not None:
            query = self.ingredients_ref.where('ingredient', '==', ingredient)
        if dietary is not None:
            query = self.dietaries_ref.where('dietary', '==', dietary)
        
        results = query.stream()
        return [review.to_dict().get('dish_name') for review in results]