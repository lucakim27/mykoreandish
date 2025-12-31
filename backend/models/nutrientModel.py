from typing import List, Dict, Any
from flask import flash
import csv
from backend.config.db import get_db

class NutrientManager:
    def __init__(self, firestore_module: Any):
        self.db = get_db()
        self.users_ref = self.db.collection('Users')
        self.nutrients_ref = self.db.collection('Nutrients')
        self.firestore = firestore_module
    
    def _get_user(self, google_id: str) -> Any:
        user_ref = self.users_ref.where('google_id', '==', google_id)
        user = user_ref.get()
        if not user:
            raise ValueError("User does not exist.")
        return user

    def get_all_nutrients(self) -> List[Dict[str, str]]:
        nutrients = []
        try:
            with open('data/nutrients.csv', mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    nutrients.append({
                        'nutrient': row['name']
                    })
        except Exception as e:
            flash(f'Error reading ingredients from CSV: {e}', 'error')

        return nutrients

    def add_nutrient_review(self, ingredient: str, google_id: str, nutrient: str) -> None:
        try:
            self._get_user(google_id)
            self.nutrients_ref.add({
                'google_id': google_id,
                'ingredient': ingredient,
                'nutrient': nutrient,
                'timestamp': self.firestore.SERVER_TIMESTAMP
            })
            flash('Nutrient added successfully!', 'success')
        except ValueError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash(f'Error adding nutrient: {e}', 'error')
    
    def get_ingredient_nutrients(self, ingredient: str):
        nutrient_ref = self.nutrients_ref.where("ingredient", "==", ingredient)
        nutrients = nutrient_ref.stream()

        nutrient_count = {}
        for doc in nutrients:
            nutrient = doc.to_dict().get("nutrient")
            nutrient_count[nutrient] = nutrient_count.get(nutrient, 0) + 1

        return [
            {"nutrient": k, "count": v}
            for k, v in nutrient_count.items()
        ]

    def get_nutrient_history(self, google_id: str) -> List[Dict[str, Any]]:
        nutrient_ref = self.nutrients_ref.where('google_id', '==', google_id)
        nutrients = nutrient_ref.stream()
        
        nutrients_list = [{
                'id': nutrient.id,
                'ingredient': nutrient.to_dict().get('ingredient'),
                'timestamp': nutrient.to_dict().get('timestamp'),
                'nutrient': nutrient.to_dict().get('nutrient')
            } for nutrient in nutrients]
    
        if not nutrients_list:
            return []

        nutrients_list.sort(key=lambda x: x['timestamp'], reverse=True)
        return nutrients_list
    
    def update_nutrient_review(self, history_id: str, nutrient: str) -> bool:
        if not history_id or not nutrient:
            flash('Invalid input for ingredient.', 'error')
            return False

        try:
            nutrient_ref = self.nutrients_ref.document(history_id)
            nutrient_ref.update({
                'nutrient': nutrient
            })
            flash('Nutrient saved successfully!', 'success')
            return True
        except Exception as e:
            flash(f'Error saving nutrient: {e}', 'error')
            return False
    
    def delete_nutrient(self, history_id: str) -> bool | None:
        if history_id:
            try:
                nutrient_ref = self.nutrients_ref.document(history_id)
                nutrient_ref.delete()
                flash('Nutrient review deleted successfully.', 'success')
            except Exception as e:
                flash(f'An error occurred while deleting the nutrient review: {e}', 'error')
    
    def get_ingredients_by_nutrient(self, nutrient: str) -> List[str]:
        try:
            nutrient_ref = self.nutrients_ref.where('nutrient', '==', nutrient)
            nutrients = nutrient_ref.stream()
            
            ingredients = [nutrient.to_dict().get('ingredient') for nutrient in nutrients]
            
            if not ingredients:
                return []
            
            return ingredients
        except Exception as e:
            flash(f'Error retrieving ingredients: {e}', 'error')
            return []
    
    def get_nutrients_count(self):
        return self.nutrients_ref.count().get()[0][0].value