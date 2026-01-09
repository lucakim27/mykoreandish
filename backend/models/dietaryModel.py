import csv
from os import abort
from flask import flash
from typing import List, Dict, Any
from backend.config.db import get_db
from backend.config.config import FileConfig

class DietaryManager:
    def __init__(self, firestore_module: Any):
        self.db = get_db()
        self.users_ref = self.db.collection('Users')
        self.dietaries_ref = self.db.collection('Dietaries')
        self.firestore = firestore_module

    def _get_user(self, google_id: str) -> Any:
        user_ref = self.users_ref.where('google_id', '==', google_id)
        user = user_ref.get()
        if not user:
            raise ValueError("User does not exist.")
        return user

    def add_dietary_review(self, dish_name: str, google_id: str, dietary: str) -> None:
        try:
            self._get_user(google_id)
            dietary_instance = {
                'google_id': google_id,
                'dish_name': dish_name,
                'dietary': dietary,
                'timestamp': self.firestore.SERVER_TIMESTAMP
            }
            self.dietaries_ref.add(dietary_instance)
            flash('Dietary review added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding dietary review: {e}', 'error')
    
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

    def delete_dietary(self, history_id: str) -> bool:
        if not history_id:
            return False

        dietary_ref = self.dietaries_ref.document(history_id)
        doc = dietary_ref.get()

        if not doc.exists:
            return False

        dietary_ref.delete()
        return True

    def get_all_dietaries(self) -> List[Dict[str, str]]:
        dietaries = []
        try:
            with open(FileConfig.DIETARY_FILE, mode='r') as file:
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
    
    def get_dietary_preference(self, google_id: str) -> str | None:
        try:
            user = self._get_user(google_id)
            user_data = user[0].to_dict()
            return user_data.get('dietary_preference', None)
        except Exception:
            return None

    def get_all_reviews(self) -> List[Dict[str, Any]]:
        reviews = []
        try:
            dietary_docs = self.dietaries_ref.stream()
            for doc in dietary_docs:
                review_data = doc.to_dict()
                review_data['id'] = doc.id
                reviews.append(review_data)
        except Exception as e:
            flash(f'Error retrieving dietary reviews: {e}', 'error')
        return reviews