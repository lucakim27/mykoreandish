import csv
from flask import flash
from google.cloud import firestore
from typing import List, Dict, Any

class Dietary:
    def __init__(self, dish_name: str, dietary: str, google_id: str, timestamp: str):
        self.dish_name = dish_name
        self.dietary = dietary
        self.google_id = google_id
        self.timestamp = timestamp

class UserNotFoundError(Exception):
    pass

class DietaryManager:
    def __init__(self, db: firestore.Client, firestore_module: Any):
        self.users_ref = db.collection('Users')
        self.dietaries_ref = db.collection('Dietaries')
        self.firestore = firestore_module

    def _get_user(self, google_id: str) -> Any:
        user_ref = self.users_ref.where('google_id', '==', google_id)
        user = user_ref.get()
        if not user:
            raise UserNotFoundError("User does not exist.")
        return user

    def add_dietary(self, dish_name: str, google_id: str, dietary: str) -> None:
        try:
            self._get_user(google_id)
            dietary_instance = Dietary(dish_name, dietary, google_id, self.firestore.SERVER_TIMESTAMP)
            self.dietaries_ref.add({
                'google_id': dietary_instance.google_id,
                'dish_name': dietary_instance.dish_name,
                'dietary': dietary_instance.dietary,
                'timestamp':dietary_instance.timestamp
            })
            flash('Dietary added successfully!', 'success')
        except UserNotFoundError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash(f'Error adding dietary: {e}', 'error')
    
    def get_dietary_review_by_id(self, history_id):
        review_doc = self.dietaries_ref.document(history_id).get()

        if review_doc.exists:
            review_data = review_doc.to_dict()

            dish_name = review_data.get("dish_name")
            dietary = review_data.get("dietary")

            return {
                "dish_name": dish_name,
                "dietary": dietary
            }
        else:
            return None

    def get_dietary_history(self, google_id: str) -> List[Dict[str, Any]]:
        dietary_ref = self.dietaries_ref.where('google_id', '==', google_id)
        dietaries = dietary_ref.stream()
        dietaries_list = [{
            'id': dietary.id,
            'dish_name': dietary.to_dict().get('dish_name'),
            'timestamp': dietary.to_dict().get('timestamp'),
            'dietary': dietary.to_dict().get('dietary')
        } for dietary in dietaries]

        if not dietaries_list:
            return []

        return dietaries_list

    def update_dietary(self, history_id: str, dietary: str) -> bool:
        if not history_id or not dietary:
            flash('Invalid input for dietary.', 'error')
            return False

        try:
            dietary_ref = self.dietaries_ref.document(history_id)
            dietary_ref.update({'dietary': dietary})
            flash('Dietary saved successfully!', 'success')
            return True
        except Exception as e:
            flash(f'Error saving dietary: {e}', 'error')
            return False

    def delete_dietary(self, history_id: str) -> bool | None:
        if history_id:
            try:
                dietary_ref = self.dietaries_ref.document(history_id)
                dietary_ref.delete()
                flash('Dietary review deleted successfully.', 'success')
            except Exception:
                flash('An error occurred while deleting the dietary review.', 'error')
        else:
            flash('Invalid history ID.', 'error')

    def get_all_dietaries(self) -> List[Dict[str, str]]:
        dietaries = []
        try:
            with open('csv/dietary.csv', mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    dietaries.append({
                        'dietary': row['Dietary']
                    })
        except Exception as e:
            flash(f'Error reading ingredients from CSV: {e}', 'error')
        
        return dietaries
    
    def get_dishes_by_ingredient(self, ingredient: str) -> List[str]:
        dietary_ref = self.dietaries_ref.where('dietary', '==', ingredient)
        dietaries = dietary_ref.stream()
        dish_names = []
        for dietary in dietaries:
            d = dietary.to_dict()
            if d is not None and 'dish_name' in d:
                dish_names.append(d['dish_name'])

        dish_names = list(set(dish_names))

        if not dish_names:
            return []

        return dish_names