from typing import List, Dict, Any
from flask import flash
import csv
from collections import defaultdict
from project.config.db import get_db

class IngredientManager:
    def __init__(self, firestore_module: Any):
        self.db = get_db()
        self.users_ref = self.db.collection('Users')
        self.ingredients_ref = self.db.collection('Ingredients')
        self.firestore = firestore_module
    
    def _get_user(self, google_id: str) -> Any:
        user_ref = self.users_ref.where('google_id', '==', google_id)
        user = user_ref.get()
        if not user:
            raise ValueError("User does not exist.")
        return user
    
    def get_ingredient_instance(self, name):
        ingredients = self.get_all_ingredients()
        for ingredient in ingredients:
            if ingredient['ingredient'].lower() == name.lower():
                return ingredient
        return None
    
    def get_ingredients_instance(self, names: List[str]) -> List[Dict[str, str]]:
        ingredients = self.get_all_ingredients()
        matched_ingredients = []
        for name in names:
            for ingredient in ingredients:
                if ingredient['ingredient'].lower() == name.lower():
                    matched_ingredients.append(ingredient)
                    break
                
        return matched_ingredients
    
    def add_ingredient(self, dish_name: str, google_id: str, ingredient: str) -> None:
        try:
            self._get_user(google_id)
            self.ingredients_ref.add({
                'google_id': google_id,
                'dish_name': dish_name,
                'ingredient': ingredient,
                'timestamp': self.firestore.SERVER_TIMESTAMP
            })
            flash('Ingredient added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding ingredient: {e}', 'error')
    
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
    
    def get_ingredient_review_by_id(self, history_id):
        review_doc = self.ingredients_ref.document(history_id).get()
        if review_doc.exists:
            review_data = review_doc.to_dict()
            dish_name = review_data.get("dish_name")
            ingredient = review_data.get("ingredient")
            return {
                "dish_name": dish_name,
                "ingredient": ingredient
            }
        else:
            return None
    
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
        if history_id:
            try:
                ingredient_ref = self.ingredients_ref.document(history_id)
                ingredient_ref.delete()
                flash('Ingredient review deleted successfully.', 'success')
            except Exception as e:
                flash(f'An error occurred while deleting the ingredient review: {e}', 'error')
        else:
            flash('Invalid history ID.', 'error')
        
    def get_all_ingredients(self) -> List[Dict[str, str]]:
        ingredients = []
        try:
            with open('csv/ingredients.csv', mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    ingredients.append({
                        'ingredient': row['ingredient'],
                        'description': row['description'],
                        'korean_name': row['korean_name'],
                        'image_url': row['image_url']
                    })
        except Exception as e:
            flash(f'Error reading ingredients from CSV: {e}', 'error')
        return ingredients
    
    def get_dishes_by_ingredient(self, ingredient: str) -> List[str]:
        dishes = []
        try:
            ingredient_ref = self.ingredients_ref.where('ingredient', '==', ingredient)
            ingredients = ingredient_ref.stream()
            for ingredient in ingredients:
                if not ingredient.to_dict().get('dish_name') in dishes:
                    dishes.append(ingredient.to_dict().get('dish_name'))
        except Exception as e:
            flash(f'Error retrieving dishes from Firestore: {e}', 'error')
        return dishes
    
    def get_ingredients_by_dish(self, dish_name: str) -> List[str]:
        ingredients = []
        try:
            ingredient_ref = self.ingredients_ref.where('dish_name', '==', dish_name)
            ingredients = ingredient_ref.stream()
            ingredients = [ingredient.to_dict().get('ingredient') for ingredient in ingredients]
        except Exception as e:
            flash(f'Error retrieving ingredients from Firestore: {e}', 'error')
        return ingredients

    def get_similar_dishes(self, current_dish_name: str, top_n: int = 5) -> List[Dict[str, Any]]:
        try:
            dish_metadata = {}
            try:
                with open('csv/dishes.csv', mode='r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        dish_metadata[row['dish_name']] = {
                            "korean_name": row.get('korean_name', row['dish_name']),
                            "thumbnail_url": row.get('thumbnail_url', '')
                        }
            except Exception as e:
                flash(f"Error reading dishes from CSV: {e}", "error")
                return []
            current_ingredient_docs = self.ingredients_ref.where("dish_name", "==", current_dish_name).stream()
            current_ingredients = set(
                doc.to_dict()["ingredient"].strip().lower()
                for doc in current_ingredient_docs
            )
            if not current_ingredients:
                return []
            dish_ingredient_map = defaultdict(set)
            all_ingredient_docs = self.ingredients_ref.stream()
            for doc in all_ingredient_docs:
                data = doc.to_dict()
                dish = data["dish_name"]
                ingredient = data["ingredient"].strip().lower()
                if dish != current_dish_name:
                    dish_ingredient_map[dish].add(ingredient)
            scored_similars = []
            for dish, ingredients in dish_ingredient_map.items():
                shared = current_ingredients & ingredients
                score = len(shared)
                if score > 0 and dish in dish_metadata:
                    dish_data = dish_metadata[dish]
                    scored_similars.append({
                        "dish_name": dish,
                        "korean_name": dish_data["korean_name"],
                        "thumbnail_url": dish_data["thumbnail_url"],
                        "shared_ingredients": list(shared),
                        "score": score
                    })
            scored_similars.sort(key=lambda x: x["score"], reverse=True)
            return scored_similars[:top_n]
        except Exception as e:
            flash(f"Error finding similar dishes: {e}", "error")
            return []

