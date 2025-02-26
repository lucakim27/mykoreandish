from typing import List, Dict, Any
from flask import flash
from google.cloud import firestore

class Favorite:
    def __init__(self, dish_name: str, google_id: str):
        self.dish_name = dish_name
        self.google_id = google_id

class UserNotFoundError(Exception):
    pass

class FavoriteManager:
    def __init__(self, db: firestore.Client, firestore_module: Any):
        self.users_ref = db.collection('Users')
        self.favorites_ref = db.collection('Favorites')
        self.firestore = firestore_module
    
    def _get_user(self, google_id: str) -> Any:
        user_ref = self.users_ref.where('google_id', '==', google_id)
        user = user_ref.get()
        if not user:
            raise UserNotFoundError("User does not exist.")
        return user

    def add_favorite(self, dish_name, google_id):
        try:        
            self._get_user(google_id)  # Ensure the user exists
            
            dish_ref = self.favorites_ref.document(dish_name)  # Reference the dish document
            dish_doc = dish_ref.get()

            if dish_doc.exists:
                # Append google_id if it's not already in the list
                dish_ref.update({
                    'favorited_by': self.firestore.ArrayUnion([google_id])
                })
            else:
                # Create a new document if it doesn't exist
                dish_ref.set({
                    'favorited_by': [google_id]
                })

            flash('Favorite added successfully!', 'success')

        except UserNotFoundError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash(f'Error adding favorite: {e}', 'error')
    
    def delete_favorite(self, dish_name, google_id):
        try:
            self._get_user(google_id)  # Ensure the user exists

            dish_ref = self.favorites_ref.document(dish_name)  # Reference the dish document
            dish_doc = dish_ref.get()

            if dish_doc.exists:
                dish_data = dish_doc.to_dict()
                favorited_by = dish_data.get("favorited_by", [])

                if google_id in favorited_by:
                    # Remove user from the list
                    dish_ref.update({
                        'favorited_by': self.firestore.ArrayRemove([google_id])
                    })
                    
                    # Check if list is now empty; delete document if true
                    if len(favorited_by) == 1:  # After removal, it would be empty
                        dish_ref.delete()

                    flash('Favorite removed successfully!', 'success')
                else:
                    flash('User has not favorited this dish.', 'info')
            else:
                flash('Dish not found in favorites.', 'error')

        except UserNotFoundError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash(f'Error removing favorite: {e}', 'error')
    
    def get_all_favorites(self, user):
        try:
            user_favorites = []  # List to store favorited dishes

            # Get all dish documents from Firestore
            dishes = self.favorites_ref.stream()  

            for dish in dishes:
                dish_data = dish.to_dict()
                favorited_by = dish_data.get("favorited_by", [])

                # If user is in the favorited_by list, add dish name to the list
                if user['google_id'] in favorited_by:
                    user_favorites.append(dish.id)  # dish.id is the document name (dish_name)

            return user_favorites  # List of dish names favorited by the user

        except Exception as e:
            return []
