import csv
from flask import flash
from google.cloud import firestore
from typing import List, Dict, Any

class Dietary:
    def __init__(self, dish_name: str, dietary: str):
        self.dish_name = dish_name
        self.dietary = dietary

class UserNotFoundError(Exception):
    pass

class DietaryManager:
    DIETARY_TYPES = ['Vegetarian', 'Halal', 'Vegan', 'Seafood', 'Broth', 'Contain Meat']

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

    def _create_dietary_instance(self, dish_name: str, dietary: str) -> Dietary:
        return Dietary(dish_name, dietary)

    def add_dietary(self, dish_name: str, google_id: str, dietary: str) -> None:
        try:
            self._get_user(google_id)
            dietary_instance = self._create_dietary_instance(dish_name, dietary)
            self.dietaries_ref.add({
                'google_id': google_id,
                'dish_name': dietary_instance.dish_name,
                'dietary': dietary_instance.dietary,
                'timestamp': self.firestore.SERVER_TIMESTAMP
            })
            flash('Dietary added successfully!', 'success')
        except UserNotFoundError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash(f'Error adding dietary: {e}', 'error')
            print(f"Error: {e}")

    def get_dietary(self, dish_name: str) -> Dict[str, int]:
        dietary_ref = self.dietaries_ref.where('dish_name', '==', dish_name)
        dietaries = dietary_ref.stream()
        dietaries_list = [Dietary(dietary.to_dict().get('dish_name'), dietary.to_dict().get('dietary')) for dietary in dietaries]

        if not dietaries_list:
            return {}

        dietary_count = {dietary_type: 0 for dietary_type in self.DIETARY_TYPES}

        for dietary in dietaries_list:
            if dietary.dietary in dietary_count:
                dietary_count[dietary.dietary] += 1

        return dietary_count

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

        dietaries_list.sort(key=lambda x: x['timestamp'], reverse=True)
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
            print(f"Error: {e}")
            return False

    def delete_dietary(self, history_id: str) -> bool:
        try:
            dietary_ref = self.dietaries_ref.document(history_id)
            dietary_ref.delete()
            flash('Dietary review deleted successfully.', 'success')
            return True
        except Exception as e:
            flash('An error occurred while deleting the dietary review.', 'error')
            print(f"Error: {e}")
            return False

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