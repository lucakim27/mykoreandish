from flask import flash
from firebase_admin import firestore

class UserSelection:
    def __init__(self, history_id, dish_name, rating=None):
        self.history_id = history_id
        self.dish_name = dish_name
        self.rating = rating

class UserSelectionManager:
    def __init__(self, db):
        self.db = db
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

    def update_review(self, history_id, rating, price, restaurant):
        """Rate a dish by updating its rating in the 'UserSelections' collection."""
        if not history_id or not rating:
            flash('Invalid input for rating.', 'error')
            return False

        try:
            history_ref = self.user_selections_ref.document(history_id)
            history_ref.update({
                'rating': int(rating),
                'price': float(price),
                'restaurant': restaurant
            })
            flash('Rating saved successfully!', 'success')
            return True
        except Exception as e:
            flash(f'Error saving rating: {e}', 'error')
            return False

    def get_dish_statistics(self):
        """Retrieve and calculate statistics for dishes based on user selections."""
        average_ratings = {}
        average_prices = {}
        selection_counts = {}

        try:
            # Dictionaries to hold dish ratings and prices
            dish_ratings = {}
            dish_prices = {}

            # Retrieve ratings and prices from the 'UserSelections' collection
            selections = self.user_selections_ref.stream()

            # Process selections in a single pass
            for selection in selections:
                selection_data = selection.to_dict()
                dish_name = selection_data.get('dish_name')
                rating_value = selection_data.get('rating')
                price_value = selection_data.get('price')

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

                    # Handle the prices for dishes
                    if price_value is not None:
                        if dish_name not in dish_prices:
                            dish_prices[dish_name] = {'total': 0, 'count': 0}
                        dish_prices[dish_name]['total'] += price_value
                        dish_prices[dish_name]['count'] += 1

            # Calculate average ratings for each dish
            for dish_name, data in dish_ratings.items():
                average_rating = data['total'] / data['count']
                average_ratings[dish_name] = average_rating

            # Calculate average prices for each dish
            for dish_name, data in dish_prices.items():
                average_price = data['total'] / data['count']
                average_prices[dish_name] = average_price

            # Ensure every dish from UserSelections is included in statistics
            for dish_name in selection_counts:
                if dish_name not in average_ratings:
                    average_ratings[dish_name] = 0  # No ratings but included in selections
                if dish_name not in average_prices:
                    average_prices[dish_name] = 0  # No prices but included in selections

        except Exception as e:
            print(f"Error fetching dish statistics: {e}")

        # Sorting the results
        average_ratings = dict(sorted(average_ratings.items(), key=lambda item: item[1], reverse=True))
        average_prices = dict(sorted(average_prices.items(), key=lambda item: item[1], reverse=True))
        selection_counts = dict(sorted(selection_counts.items(), key=lambda item: item[1], reverse=True))

        return average_ratings, average_prices, selection_counts

    
    
    def add_selection(self, google_id, dish_name, price, rating, restaurant):
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
            'price': float(price),
            'rating': int(rating),
            'restaurant': restaurant,
            'timestamp': firestore.SERVER_TIMESTAMP
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
                'price': selection.to_dict().get('price'),
                'restaurant': selection.to_dict().get('restaurant'),
                'rating': selection.to_dict().get('rating')
            } for selection in selections]

        except Exception as e:
            print(f"Error retrieving user history: {e}")
            return []  # Return an empty list if an error occurs
        