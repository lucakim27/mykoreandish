import csv
import logging
from typing import Any
from flask import flash
from config.db import get_db

class PriceManager:
    def __init__(self, csv_file, firestore_module: Any):
        self.csv_file = csv_file
        self.db = get_db()
        self.users_ref = self.db.collection('Users')
        self.firestore = firestore_module
        self.prices_ref = self.db.collection('Prices')
    
    def _get_user(self, google_id: str) -> Any:
        user_ref = self.users_ref.where('google_id', '==', google_id)
        user = user_ref.get()
        if not user:
            raise ValueError("User does not exist.")
        return user

    def get_all_locations(self):
        locations = {'countries': set(), 'cities': set(), 'country_to_cities': {}}
        try:
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    country = row['country']
                    city = row['state']
                    locations['countries'].add(country)
                    locations['cities'].add(city)
                    if country not in locations['country_to_cities']:
                        locations['country_to_cities'][country] = []
                    locations['country_to_cities'][country].append(city)
        except Exception as e:
            logging.info(f"Error reading CSV file: {e}")
        return {
            'countries': list(locations['countries']),
            'cities': list(locations['cities']),
            'country_to_cities': locations['country_to_cities']
        }
    
    def add_price(self, dish_name: str, google_id: str, price: float, country: str, state: str) -> None:
        try:
            self._get_user(google_id)
            self.prices_ref.add({
                'google_id': google_id,
                'dish_name': dish_name,
                'price': price,
                'country': country,
                'state': state,
                'timestamp': self.firestore.SERVER_TIMESTAMP
            })
            flash('Ingredient added successfully!', 'success')
        except ValueError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash(f'Error adding ingredient: {e}', 'error')
    
    def get_price_info(self, name):
        prices_ref = self.prices_ref \
            .where('dish_name', '==', name)
        prices = prices_ref.stream()

        price_state_list = []
        for price_doc in prices:
            data = price_doc.to_dict()
            price = data.get('price')
            country = data.get('country')
            state = data.get('state')
            timestamp = data.get('timestamp')
            if hasattr(timestamp, 'to_datetime'):
                timestamp = timestamp.to_datetime()
            if price is not None and state is not None and timestamp is not None:
                price_state_list.append({
                    'price': price,
                    'country': country,
                    'state': state,
                    'timestamp': timestamp
                })
        return price_state_list
    
    def get_available_countries(self, name):
        prices_ref = self.prices_ref.where('dish_name', '==', name)
        prices = prices_ref.stream()
        countries = set()
        for price_doc in prices:
            data = price_doc.to_dict()
            country = data.get('country')
            if country:
                countries.add(country)
        return sorted(countries)
    
    def get_price_history(self, google_id):
        prices_ref = self.prices_ref.where('google_id', '==', google_id)
        prices = prices_ref.stream()
        prices_list = [{
                'id': price.id,
                'dish_name': price.to_dict().get('dish_name'),
                'price': price.to_dict().get('price'),
                'country': price.to_dict().get('country'),
                'state': price.to_dict().get('state'),
                'timestamp': price.to_dict().get('timestamp')
            } for price in prices]
        if not prices_list:
            return []
        prices_list.sort(key=lambda x: x['timestamp'], reverse=True)
        return prices_list
    
    def update_price(self, history_id, new_price, new_country, new_state):
        if not history_id or not new_price:
            flash('Invalid input for price.', 'error')
            return False
        try:
            price_ref = self.prices_ref.document(history_id)
            price_ref.update({
                'price': new_price,
                'country': new_country,
                'state': new_state
            })
            flash('Price saved successfully!', 'success')
            return True
        except Exception as e:
            flash(f'Error saving price: {e}', 'error')
            return False
    
    def delete_price(self, history_id):
        if history_id:
            try:
                price_ref = self.prices_ref.document(history_id)
                price_ref.delete()
                flash('Price review deleted successfully.', 'success')
            except Exception as e:
                flash(f'An error occurred while deleting the price review: {e}', 'error')