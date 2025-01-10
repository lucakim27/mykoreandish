from flask import flash
from google.cloud import firestore
from typing import List, Dict, Union
import requests

class Shop:
    def __init__(self, dish_name: str, link: str, timestamp, google_id: str):
        self.dish_name = dish_name
        self.link = link
        self.timestamp = timestamp
        self.google_id = google_id

class ShopManager:
    def __init__(self, db: firestore.Client, firestore_module):
        self.dishes_ref = db.collection('Dishes')
        self.users_ref = db.collection('Users')
        self.prices_ref = db.collection('Shops')
        self.firestore = firestore_module
    
    def add_shop(self, google_id: str, dish_name: str, link: str) -> None:
        user = self._get_user_by_google_id(google_id)
        if not user:
            raise ValueError("User does not exist.")
        
        dish = self._get_dish_by_name(dish_name)
        if not dish:
            raise ValueError("Dish does not exist.")
        
        self.prices_ref.add({
            'google_id': google_id,
            'dish_name': dish_name,
            'link': link,
            'timestamp': self.firestore.SERVER_TIMESTAMP
        })
    
    def update_shop(self, history_id: str, link: str) -> bool:
        if not history_id or not link:
            flash('Invalid input for link.', 'error')
            return False

        try:
            price_ref = self.prices_ref.document(history_id)
            price_ref.update({
                'link': link
            })
            flash('Link saved successfully!', 'success')
            return True
        except Exception as e:
            flash(f'Error saving link: {e}', 'error')
            return False
    
    def delete_shop(self, history_id: str) -> bool:
        try:
            price_ref = self.prices_ref.document(history_id)
            price_ref.delete()
            flash('Shop review deleted successfully.', 'success')
            return True
        except Exception as e:
            flash(f'An error occurred while deleting the shop review: {e}', 'error')
            return False
    
    def get_shop(self, dish_name: str) -> List[Dict[str, Union[str, float]]]:
        prices = self.prices_ref.where('dish_name', '==', dish_name).stream()
        prices_list = self._convert_prices_to_list(prices)
        return sorted(prices_list, key=lambda x: x['timestamp'], reverse=True)
    
    def get_shop_history(self, google_id: str) -> List[Dict[str, Union[str, float]]]:
        prices = self.prices_ref.where('google_id', '==', google_id).stream()
        prices_list = self._convert_prices_to_list(prices)
        return sorted(prices_list, key=lambda x: x['timestamp'], reverse=True)

    def _get_user_by_google_id(self, google_id: str):
        user_ref = self.users_ref.where('google_id', '==', google_id)
        return user_ref.get()

    def _get_dish_by_name(self, dish_name: str):
        dish_ref = self.dishes_ref.document(dish_name)
        return dish_ref.get()

    def _convert_prices_to_list(self, prices) -> List[Dict[str, Union[str, float]]]:
        return [{
            'id': price.id,
            'dish_name': price.to_dict().get('dish_name'),
            'timestamp': price.to_dict().get('timestamp'),
            'link': price.to_dict().get('link'),
            'google_id': price.to_dict().get('google_id'),
            'name': self.extract_place_name(self.resolve_google_maps_link(price.to_dict().get('link')))
        } for price in prices]

    def resolve_google_maps_link(self, shortened_url):
        try:
            # Send a HEAD request to follow the redirect
            response = requests.head(shortened_url, allow_redirects=True)
            full_url = response.url
            return full_url
        except Exception as e:
            return f"Error resolving link: {str(e)}"
    
    def extract_place_name(self, full_url):
        if "/place/" in full_url:
            start = full_url.find("/place/") + len("/place/")
            end = full_url.find("/", start)
            place_name = full_url[start:end].replace("+", " ")
            return place_name
        return None