from flask import flash

class UserSelection:
    def __init__(self, history_id, dish_name, rating=None):
        self.history_id = history_id
        self.dish_name = dish_name
        self.rating = rating

class UserSelectionManager:
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

    def get_dish_statistics(self, dish_name):
        """Retrieve and calculate statistics for a specific dish based on user selections."""
        average_ratings = {}
        selection_counts = {}
        average_spiciness = {}
        average_sweetness = {}
        average_texture = {}
        average_healthiness = {}
        average_sourness = {}
        average_temperature = {}

        try:
            # Dictionaries to hold dish ratings and new criteria
            dish_ratings = {}
            dish_spiciness = {}
            dish_sweetness = {}
            dish_texture = {}
            dish_healthiness = {}
            dish_sourness = {}
            dish_temperature = {}

            # Retrieve ratings and criteria from the 'UserSelections' collection for the specific dish
            selections = self.user_selections_ref.where('dish_name', '==', dish_name).stream()

            # Process selections in a single pass
            for selection in selections:
                selection_data = selection.to_dict()
                rating_value = selection_data.get('rating')
                spiciness_value = selection_data.get('spiciness')
                sweetness_value = selection_data.get('sweetness')
                texture_value = selection_data.get('texture')
                healthiness_value = selection_data.get('healthiness')
                sourness_value = selection_data.get('sourness')  # New field for sourness
                temperature_value = selection_data.get('temperature')

                # Count the selections for the dish
                if dish_name not in selection_counts:
                    selection_counts[dish_name] = 0
                selection_counts[dish_name] += 1

                # Handle the ratings for the dish
                if rating_value is not None:
                    if dish_name not in dish_ratings:
                        dish_ratings[dish_name] = {'total': 0, 'count': 0}
                    dish_ratings[dish_name]['total'] += rating_value
                    dish_ratings[dish_name]['count'] += 1

                if temperature_value is not None:
                    if dish_name not in dish_temperature:
                        dish_temperature[dish_name] = {'total': 0, 'count': 0}
                    dish_temperature[dish_name]['total'] += temperature_value
                    dish_temperature[dish_name]['count'] += 1

                # Handle the spiciness ratings for the dish
                if spiciness_value is not None:
                    if dish_name not in dish_spiciness:
                        dish_spiciness[dish_name] = {'total': 0, 'count': 0}
                    dish_spiciness[dish_name]['total'] += spiciness_value
                    dish_spiciness[dish_name]['count'] += 1

                # Handle the sweetness ratings for the dish
                if sweetness_value is not None:
                    if dish_name not in dish_sweetness:
                        dish_sweetness[dish_name] = {'total': 0, 'count': 0}
                    dish_sweetness[dish_name]['total'] += sweetness_value
                    dish_sweetness[dish_name]['count'] += 1

                # Handle the texture ratings for the dish
                if texture_value is not None:
                    if dish_name not in dish_texture:
                        dish_texture[dish_name] = {'total': 0, 'count': 0}
                    dish_texture[dish_name]['total'] += texture_value
                    dish_texture[dish_name]['count'] += 1

                # Handle the healthiness ratings for the dish
                if healthiness_value is not None:
                    if dish_name not in dish_healthiness:
                        dish_healthiness[dish_name] = {'total': 0, 'count': 0}
                    dish_healthiness[dish_name]['total'] += healthiness_value
                    dish_healthiness[dish_name]['count'] += 1

                # Handle the sourness ratings for the dish
                if sourness_value is not None:
                    if dish_name not in dish_sourness:
                        dish_sourness[dish_name] = {'total': 0, 'count': 0}
                    dish_sourness[dish_name]['total'] += sourness_value
                    dish_sourness[dish_name]['count'] += 1

            # Calculate average ratings for the dish
            if dish_name in dish_ratings:
                average_ratings[dish_name] = dish_ratings[dish_name]['total'] / dish_ratings[dish_name]['count']

            # Calculate average spiciness for the dish
            if dish_name in dish_spiciness:
                average_spiciness[dish_name] = dish_spiciness[dish_name]['total'] / dish_spiciness[dish_name]['count']

            # Calculate average sweetness for the dish
            if dish_name in dish_sweetness:
                average_sweetness[dish_name] = dish_sweetness[dish_name]['total'] / dish_sweetness[dish_name]['count']

            # Calculate average texture for the dish
            if dish_name in dish_texture:
                average_texture[dish_name] = dish_texture[dish_name]['total'] / dish_texture[dish_name]['count']

            # Calculate average healthiness for the dish
            if dish_name in dish_healthiness:
                average_healthiness[dish_name] = dish_healthiness[dish_name]['total'] / dish_healthiness[dish_name]['count']

            # Calculate average sourness for the dish
            if dish_name in dish_sourness:
                average_sourness[dish_name] = dish_sourness[dish_name]['total'] / dish_sourness[dish_name]['count']

            # Calculate average temperature for the dish
            if dish_name in dish_temperature:
                average_temperature[dish_name] = dish_temperature[dish_name]['total'] / dish_temperature[dish_name]['count']

        except Exception as e:
            print(f"Error fetching dish statistics: {e}")
            
        return average_ratings, selection_counts, average_spiciness, average_sweetness, average_texture, average_healthiness, average_sourness, average_temperature
    
    def add_selection(self, google_id, dish_name, spiciness, sweetness, sourness, texture, temperature, healthiness, rating):
        """Add a food selection without a rating initially."""
        user_ref = self.users_ref.where('google_id', '==', google_id)
        user = user_ref.get()

        if not user:
            raise ValueError("User does not exist.")
        
        dish_ref = self.dishes_ref.document(dish_name)  # Ensure dish_name is used correctly
        dish = dish_ref.get()
        
        if not dish:
            raise ValueError("User does not exist.")
        
        # Add selection to the UserSelections collection with rating as None
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
            # Query to get the user document by google_id
            user_ref = self.users_ref.where('google_id', '==', google_id)
            user_docs = user_ref.get()

            if not user_docs:
                return []  # Return empty list if user doesn't exist

            # Assuming only one user document will match, get the first document
            user = user_docs[0]  # user_docs is a list of documents

            # Query to get all selections by the user using the google_id
            user_selections_ref = self.user_selections_ref.where('google_id', '==', user.to_dict().get('google_id'))
            selections = user_selections_ref.stream()  # Stream selections

            # Return user selections as a list of dictionaries
            return [{
                'id': selection.id,  # Firestore document ID as 'id'
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
            return []  # Return an empty list if an error occurs
    
    def filter_search(self, ingredient=None, dietary=None):
        if ingredient is not None:
            query = self.ingredients_ref.where('ingredient', '==', ingredient)
        if dietary is not None:
            query = self.dietaries_ref.where('dietary', '==', dietary)
        
        results = query.stream()
        return [review.to_dict().get('dish_name') for review in results]