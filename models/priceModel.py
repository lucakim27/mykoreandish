# from flask import flash
# import csv
# from google.cloud import firestore
# from typing import List, Dict, Union

# class Price:
#     def __init__(self, name: str, price: float, currency: str, timestamp, google_id: str):
#         self.name = name
#         self.price = price
#         self.currency = currency
#         self.timestamp = timestamp
#         self.google_id = google_id

# class PriceManager:
#     def __init__(self, db: firestore.Client, firestore_module):
#         self.dishes_ref = db.collection('Dishes')
#         self.users_ref = db.collection('Users')
#         self.prices_ref = db.collection('Prices')
#         self.firestore = firestore_module
    
#     def add_price(self, google_id: str, dish_name: str, price: float, currency: str) -> None:
#         user = self._get_user_by_google_id(google_id)
#         if not user:
#             raise ValueError("User does not exist.")
        
#         dish = self._get_dish_by_name(dish_name)
#         if not dish:
#             raise ValueError("Dish does not exist.")
        
#         self.prices_ref.add({
#             'google_id': google_id,
#             'dish_name': dish_name,
#             'price': price,
#             'currency': currency,
#             'timestamp': self.firestore.SERVER_TIMESTAMP
#         })
    
#     def update_price(self, history_id: str, price: float, currency: str) -> bool:
#         if not history_id or not price:
#             flash('Invalid input for price.', 'error')
#             return False

#         try:
#             price_ref = self.prices_ref.document(history_id)
#             price_ref.update({
#                 'price': price,
#                 'currency': currency
#             })
#             flash('Price saved successfully!', 'success')
#             return True
#         except Exception as e:
#             flash(f'Error saving price: {e}', 'error')
#             return False
    
#     def delete_price(self, history_id: str) -> bool:
#         try:
#             price_ref = self.prices_ref.document(history_id)
#             price_ref.delete()
#             flash('Price review deleted successfully.', 'success')
#             return True
#         except Exception as e:
#             flash(f'An error occurred while deleting the price review: {e}', 'error')
#             return False
    
#     def get_price(self, dish_name: str) -> List[Dict[str, Union[str, float]]]:
#         prices = self.prices_ref.where('dish_name', '==', dish_name).stream()
#         prices_list = self._convert_prices_to_list(prices)
#         return sorted(prices_list, key=lambda x: x['timestamp'], reverse=True)
    
#     def total_review_len(self) -> Dict[str, int]:
#         prices = self.prices_ref.stream()
#         total_price = {}
#         for price in prices:
#             dish_name = price.to_dict().get('dish_name')
#             if dish_name in total_price:
#                 total_price[dish_name] += 1
#             else:
#                 total_price[dish_name] = 1
#         return total_price
    
#     def get_price_history(self, google_id: str) -> List[Dict[str, Union[str, float]]]:
#         prices = self.prices_ref.where('google_id', '==', google_id).stream()
#         prices_list = self._convert_prices_to_list(prices)
#         return sorted(prices_list, key=lambda x: x['timestamp'], reverse=True)
    
#     def get_all_currency(self) -> List[Dict[str, str]]:
#         try:
#             with open('csv/currency.csv', mode='r') as file:
#                 csv_reader = csv.DictReader(file)
#                 return [{'Code': row['Code'], 'Currency': row['Currency']} for row in csv_reader]
#         except FileNotFoundError:
#             flash('Currency file not found.', 'error')
#             return []
#         except Exception as e:
#             flash(f'An error occurred while reading the currency file: {e}', 'error')
#             return []

#     def _get_user_by_google_id(self, google_id: str):
#         user_ref = self.users_ref.where('google_id', '==', google_id)
#         return user_ref.get()

#     def _get_dish_by_name(self, dish_name: str):
#         dish_ref = self.dishes_ref.document(dish_name)
#         return dish_ref.get()

#     def _convert_prices_to_list(self, prices) -> List[Dict[str, Union[str, float]]]:
#         return [{
#             'id': price.id,
#             'dish_name': price.to_dict().get('dish_name'),
#             'timestamp': price.to_dict().get('timestamp'),
#             'currency': price.to_dict().get('currency'),
#             'google_id': price.to_dict().get('google_id'),
#             'price': price.to_dict().get('price')
#         } for price in prices]
