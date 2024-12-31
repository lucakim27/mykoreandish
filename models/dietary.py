
from flask import flash


class Dietary:
    def __init__(self, dish_name, dietary):
        self.dish_name = dish_name
        self.dietary = dietary

class DietaryManager:
    def __init__(self, db, firestore):
        # self.dishes_ref = db.collection('Dishes')
        self.users_ref = db.collection('Users')
        # self.prices_ref = db.collection('Prices')
        self.dietaries_ref = db.collection('Dietaries')
        self.firestore = firestore
    
    def addDietary(self, dish_name, google_id, dietary):
        user_ref = self.users_ref.where('google_id', '==', google_id)
        user = user_ref.get()

        if not user:
            raise ValueError("User does not exist.")

        self.dietaries_ref.add({
            'google_id': google_id,
            'dish_name': dish_name,
            'dietary': dietary,
            'timestamp': self.firestore.SERVER_TIMESTAMP
        })
    
    def getDietary(self, dish_name):
        dietary_ref = self.dietaries_ref.where('dish_name', '==', dish_name)
        dietaries = dietary_ref.stream()
        
        dietaries_list = [{
                'dietary': dietary.to_dict().get('dietary')
            } for dietary in dietaries]
    
        if not dietaries_list:
            return []

        dietary_count = {
            'Vegetarian': 0,
            'Halal': 0,
            'Vegan': 0,
            'Seafood': 0
        }

        for dietary in dietaries_list:
            if dietary['dietary'] in dietary_count:
                dietary_count[dietary['dietary']] += 1

        return dietary_count
    
    def get_dietary_history(self, google_id):
        dietary_ref = self.dietaries_ref.where('google_id', '==', google_id)
        dietaries = dietary_ref.stream()
        
        dietaries_list = [{
                'id': dietary.id,  # Firestore document ID as 'id'
                'dish_name': dietary.to_dict().get('dish_name'),
                'timestamp': dietary.to_dict().get('timestamp'),
                'dietary': dietary.to_dict().get('dietary')
            } for dietary in dietaries]
    
        if not dietaries_list:
            return []

        # Sort the prices list by 'timestamp' in descending order
        dietaries_list.sort(key=lambda x: x['timestamp'], reverse=True)
        return dietaries_list
    
    def update_dietary(self, history_id, dietary):
        if not history_id or not dietary:
            flash('Invalid input for dietary.', 'error')
            return False

        try:
            dietary_ref = self.dietaries_ref.document(history_id)
            dietary_ref.update({
                'dietary': dietary
            })
            flash('Dietary saved successfully!', 'success')
            return True
        except Exception as e:
            flash(f'Error saving price: {e}', 'error')
            return False
    
    def delete_dietary(self, history_id):
        """Delete a history item from the 'UserSelections' collection."""
        try:
            dietary_ref = self.dietaries_ref.document(history_id)
            dietary_ref.delete()
            flash('Dietary review deleted successfully.', 'success')
            return True
        except Exception as e:
            flash('An error occurred while deleting the price review.', 'error')
            print(f"Error: {e}")
            return False