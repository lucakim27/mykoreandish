from typing import List, Dict, Any
from flask import flash
from google.cloud import firestore
import csv

class Ingredient:
    def __init__(self, dish_name: str, ingredient: str):
        self.dish_name = dish_name
        self.ingredient = ingredient

class IngredientManager:
    def __init__(self, db: firestore.Client, firestore_module: Any):
        self.users_ref = db.collection('Users')
        self.ingredients_ref = db.collection('Ingredients')
        self.firestore = firestore_module
    
    def add_ingredient(self, dish_name: str, google_id: str, ingredient: str) -> None:
        user_ref = self.users_ref.where('google_id', '==', google_id)
        user = user_ref.get()

        if not user:
            raise ValueError("User does not exist.")

        self.ingredients_ref.add({
            'google_id': google_id,
            'dish_name': dish_name,
            'ingredient': ingredient,
            'timestamp': self.firestore.SERVER_TIMESTAMP
        })
    
    def get_ingredient(self, dish_name: str) -> Dict[str, int]:
        ingredient_ref = self.ingredients_ref.where('dish_name', '==', dish_name)
        ingredients = ingredient_ref.stream()
        
        ingredients_list = [ingredient.to_dict().get('ingredient') for ingredient in ingredients]
    
        if not ingredients_list:
            return {}

        ingredient_count = {}
        for ingredient in ingredients_list:
            if ingredient in ingredient_count:
                ingredient_count[ingredient] += 1
            else:
                ingredient_count[ingredient] = 1

        return ingredient_count
    
    def get_ingredient_history(self, google_id: str) -> List[Dict[str, Any]]:
        ingredient_ref = self.ingredients_ref.where('google_id', '==', google_id)
        ingredients = ingredient_ref.stream()
        
        ingredients_list = [{
                'id': ingredient.id,
                'dish_name': ingredient.to_dict().get('dish_name'),
                'timestamp': ingredient.to_dict().get('timestamp'),
                'ingredient': ingredient.to_dict().get('ingredient')
            } for ingredient in ingredients]
    
        if not ingredients_list:
            return []

        ingredients_list.sort(key=lambda x: x['timestamp'], reverse=True)
        return ingredients_list
    
    def update_ingredient(self, history_id: str, ingredient: str) -> bool:
        if not history_id or not ingredient:
            flash('Invalid input for ingredient.', 'error')
            return False

        try:
            ingredient_ref = self.ingredients_ref.document(history_id)
            ingredient_ref.update({
                'ingredient': ingredient
            })
            flash('Ingredient saved successfully!', 'success')
            return True
        except Exception as e:
            flash(f'Error saving ingredient: {e}', 'error')
            return False
    
    def delete_ingredient(self, history_id: str) -> bool:
        try:
            ingredient_ref = self.ingredients_ref.document(history_id)
            ingredient_ref.delete()
            flash('Ingredient review deleted successfully.', 'success')
            return True
        except Exception as e:
            flash(f'An error occurred while deleting the ingredient review: {e}', 'error')
            return False
        
    def get_all_ingredients(self) -> List[Dict[str, str]]:
        ingredients = []
        try:
            with open('csv/ingredients.csv', mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    ingredients.append({
                        'ingredient': row['ingredient']
                    })
        except Exception as e:
            flash(f'Error reading ingredients from CSV: {e}', 'error')
        
        return ingredients