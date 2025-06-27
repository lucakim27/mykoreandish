from typing import List, Dict, Any
from flask import flash
from google.cloud import firestore
import csv

class Nutrient:
    def __init__(self, ingredient: str, nutrient: str, google_id: str, timestamp: Any):
        self.ingredient = ingredient
        self.nutrient = nutrient
        self.google_id = google_id
        self.timestamp = timestamp

class UserNotFoundError(Exception):
    pass

class NutrientManager:
    def __init__(self, db: firestore.Client, firestore_module: Any):
        self.users_ref = db.collection('Users')
        self.nutrients_ref = db.collection('Nutrients')
        self.firestore = firestore_module
    
    def _get_user(self, google_id: str) -> Any:
        user_ref = self.users_ref.where('google_id', '==', google_id)
        user = user_ref.get()
        if not user:
            raise UserNotFoundError("User does not exist.")
        return user

    def get_all_nutrients(self) -> List[Dict[str, str]]:
        nutrients = []
        try:
            with open('csv/nutrients.csv', mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    nutrients.append({
                        'nutrient': row['name']
                    })
        except Exception as e:
            flash(f'Error reading ingredients from CSV: {e}', 'error')

        return nutrients

    def add_nutrient(self, ingredient: str, google_id: str, nutrient: str) -> None:
        try:
            self._get_user(google_id)
            nutrient_instance = Nutrient(ingredient, nutrient, google_id, self.firestore.SERVER_TIMESTAMP)
            self.nutrients_ref.add({
                'google_id': nutrient_instance.google_id,
                'ingredient': nutrient_instance.ingredient,
                'nutrient': nutrient_instance.nutrient,
                'timestamp': nutrient_instance.timestamp
            })
            flash('Nutrient added successfully!', 'success')
        except UserNotFoundError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash(f'Error adding nutrient: {e}', 'error')
    
    def get_nutrient(self, ingredient: str) -> Dict[str, int]:
        nutrient_ref = self.nutrients_ref.where('ingredient', '==', ingredient)
        nutrients = nutrient_ref.stream()
        
        nutrients_list = [nutrient.to_dict().get('nutrient') for nutrient in nutrients]

        total = 0
        nutrient_count = {}
        for nutrient in nutrients_list:
            if nutrient in nutrient_count:
                nutrient_count[nutrient] += 1
                total += 1
            else:
                nutrient_count[nutrient] = 1
                total += 1
        
        if total != 0:
            for nutrient in nutrient_count:
                nutrient_count[nutrient] = round(nutrient_count[nutrient] / total * 100, 1)

        return nutrient_count

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
    
    def update_nutrient(self, history_id: str, nutrient: str) -> bool:
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