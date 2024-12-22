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

    def get_dish_statistics(self):
        """Retrieve and calculate statistics for dishes based on user selections."""
        average_ratings = {}
        selection_counts = {}
        average_spiciness = {}
        average_sweetness = {}
        average_texture = {}
        average_healthiness = {}
        average_sourness = {}

        try:
            # Dictionaries to hold dish ratings and new criteria
            dish_ratings = {}
            dish_spiciness = {}
            dish_sweetness = {}
            dish_texture = {}
            dish_healthiness = {}
            dish_sourness = {}

            # Retrieve ratings and criteria from the 'UserSelections' collection
            selections = self.user_selections_ref.stream()

            # Process selections in a single pass
            for selection in selections:
                selection_data = selection.to_dict()
                dish_name = selection_data.get('dish_name')
                rating_value = selection_data.get('rating')
                spiciness_value = selection_data.get('spiciness')
                sweetness_value = selection_data.get('sweetness')
                texture_value = selection_data.get('texture')
                healthiness_value = selection_data.get('healthiness')
                sourness_value = selection_data.get('sourness')  # New field for sourness

                if dish_name:
                    # Count the selections for each dish
                    if dish_name not in selection_counts:
                        selection_counts[dish_name] = 0
                    selection_counts[dish_name] += 1

                    # Handle the ratings for dishes
                    if rating_value is not None:
                        if dish_name not in dish_ratings:
                            dish_ratings[dish_name] = {'total': 0, 'count': 0}
                        dish_ratings[dish_name]['total'] += rating_value
                        dish_ratings[dish_name]['count'] += 1

                    # Handle the spiciness ratings for dishes
                    if spiciness_value is not None:
                        if dish_name not in dish_spiciness:
                            dish_spiciness[dish_name] = {'total': 0, 'count': 0}
                        dish_spiciness[dish_name]['total'] += spiciness_value
                        dish_spiciness[dish_name]['count'] += 1

                    # Handle the sweetness ratings for dishes
                    if sweetness_value is not None:
                        if dish_name not in dish_sweetness:
                            dish_sweetness[dish_name] = {'total': 0, 'count': 0}
                        dish_sweetness[dish_name]['total'] += sweetness_value
                        dish_sweetness[dish_name]['count'] += 1

                    # Handle the texture ratings for dishes
                    if texture_value is not None:
                        if dish_name not in dish_texture:
                            dish_texture[dish_name] = {'total': 0, 'count': 0}
                        dish_texture[dish_name]['total'] += texture_value
                        dish_texture[dish_name]['count'] += 1

                    # Handle the healthiness ratings for dishes
                    if healthiness_value is not None:
                        if dish_name not in dish_healthiness:
                            dish_healthiness[dish_name] = {'total': 0, 'count': 0}
                        dish_healthiness[dish_name]['total'] += healthiness_value
                        dish_healthiness[dish_name]['count'] += 1

                    # Handle the sourness ratings for dishes
                    if sourness_value is not None:
                        if dish_name not in dish_sourness:
                            dish_sourness[dish_name] = {'total': 0, 'count': 0}
                        dish_sourness[dish_name]['total'] += sourness_value
                        dish_sourness[dish_name]['count'] += 1

            # Calculate average ratings for each dish
            for dish_name, data in dish_ratings.items():
                average_rating = data['total'] / data['count']
                average_ratings[dish_name] = average_rating

            # Calculate average spiciness for each dish
            for dish_name, data in dish_spiciness.items():
                average_spiciness[dish_name] = data['total'] / data['count']

            # Calculate average sweetness for each dish
            for dish_name, data in dish_sweetness.items():
                average_sweetness[dish_name] = data['total'] / data['count']

            # Calculate average texture for each dish
            for dish_name, data in dish_texture.items():
                average_texture[dish_name] = data['total'] / data['count']

            # Calculate average healthiness for each dish
            for dish_name, data in dish_healthiness.items():
                average_healthiness[dish_name] = data['total'] / data['count']

            # Calculate average sourness for each dish
            for dish_name, data in dish_sourness.items():
                average_sourness[dish_name] = data['total'] / data['count']

            # Ensure every dish from UserSelections is included in statistics
            for dish_name in selection_counts:
                if dish_name not in average_ratings:
                    average_ratings[dish_name] = 0  # No ratings but included in selections
                if dish_name not in average_spiciness:
                    average_spiciness[dish_name] = 0  # No spiciness data but included in selections
                if dish_name not in average_sweetness:
                    average_sweetness[dish_name] = 0  # No sweetness data but included in selections
                if dish_name not in average_texture:
                    average_texture[dish_name] = 0  # No texture data but included in selections
                if dish_name not in average_healthiness:
                    average_healthiness[dish_name] = 0  # No healthiness data but included in selections
                if dish_name not in average_sourness:
                    average_sourness[dish_name] = 0  # No sourness data but included in selections

        except Exception as e:
            print(f"Error fetching dish statistics: {e}")

        # Sorting the results
        average_ratings = dict(sorted(average_ratings.items(), key=lambda item: item[1], reverse=True))
        average_spiciness = dict(sorted(average_spiciness.items(), key=lambda item: item[1], reverse=True))
        average_sweetness = dict(sorted(average_sweetness.items(), key=lambda item: item[1], reverse=True))
        average_texture = dict(sorted(average_texture.items(), key=lambda item: item[1], reverse=True))
        average_healthiness = dict(sorted(average_healthiness.items(), key=lambda item: item[1], reverse=True))
        average_sourness = dict(sorted(average_sourness.items(), key=lambda item: item[1], reverse=True))
        selection_counts = dict(sorted(selection_counts.items(), key=lambda item: item[1], reverse=True))

        return average_ratings, selection_counts, average_spiciness, average_sweetness, average_texture, average_healthiness, average_sourness
    
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
    
    def filter_dishes(self, spiciness, sweetness, sourness, texture, temperature, healthiness, dietary):
        """
        WIP
        """
        print(spiciness, sweetness, sourness, texture, temperature, healthiness, dietary)