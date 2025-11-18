from typing import Any
from flask import flash
from google.cloud import firestore

class FavoriteManager:
    def __init__(self, db: firestore.Client, firestore_module: Any):
        self.users_ref = db.collection('Users')
        self.favorites_ref = db.collection('Favorites')
        self.firestore = firestore_module
    
    def _get_user(self, google_id: str) -> Any:
        user_ref = self.users_ref.where('google_id', '==', google_id)
        user = user_ref.get()
        if not user:
            raise ValueError("User does not exist.")
        return user

    def add_favorite(self, dish_name, google_id):
        try:        
            self._get_user(google_id)
            dish_ref = self.favorites_ref.document(dish_name)
            dish_doc = dish_ref.get()
            if dish_doc.exists:
                dish_ref.update({
                    'favorited_by': self.firestore.ArrayUnion([google_id])
                })
            else:
                dish_ref.set({
                    'favorited_by': [google_id]
                })
            flash('Favorite added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding favorite: {e}', 'error')
    
    def delete_favorite(self, dish_name, google_id):
        try:
            self._get_user(google_id)
            dish_ref = self.favorites_ref.document(dish_name)
            dish_doc = dish_ref.get()
            if dish_doc.exists:
                dish_data = dish_doc.to_dict()
                favorited_by = dish_data.get("favorited_by", [])
                if google_id in favorited_by:
                    dish_ref.update({
                        'favorited_by': self.firestore.ArrayRemove([google_id])
                    })
                    if len(favorited_by) == 1:
                        dish_ref.delete()
                    flash('Favorite removed successfully!', 'success')
                else:
                    flash('User has not favorited this dish.', 'info')
            else:
                flash('Dish not found in favorites.', 'error')
        except Exception as e:
            flash(f'Error removing favorite: {e}', 'error')
    
    def get_all_favorites(self, user):
        try:
            user_favorites = []
            dishes = self.favorites_ref.stream()  
            for dish in dishes:
                dish_data = dish.to_dict()
                favorited_by = dish_data.get("favorited_by", [])
                if user['google_id'] in favorited_by:
                    user_favorites.append(dish.id)
            return user_favorites
        except Exception:
            return []
