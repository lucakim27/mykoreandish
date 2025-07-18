import csv
import logging
from typing import Any
from flask import flash
from google.cloud import firestore
from datetime import datetime, timezone

class Price:
    def __init__(self, dish_name, price, country, state, google_id, timestamp):
        self.dish_name = dish_name
        self.price = price
        self.country = country
        self.state = state
        self.google_id = google_id
        self.timestamp = timestamp

class UserNotFoundError(Exception):
    pass

class PriceManager:
    def __init__(self, csv_file, db: firestore.Client, firestore_module: Any):
        self.csv_file = csv_file
        self.users_ref = db.collection('Users')
        self.firestore = firestore_module
        self.prices_ref = db.collection('Prices')
    
    def _get_user(self, google_id: str) -> Any:
        user_ref = self.users_ref.where('google_id', '==', google_id)
        user = user_ref.get()
        if not user:
            raise UserNotFoundError("User does not exist.")
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
            price_instance = Price(dish_name, price, country, state, google_id, self.firestore.SERVER_TIMESTAMP)
            self.prices_ref.add({
                'google_id': price_instance.google_id,
                'dish_name': price_instance.dish_name,
                'price': price_instance.price,
                'country': price_instance.country,
                'state': price_instance.state,
                'timestamp': price_instance.timestamp
            })
            flash('Ingredient added successfully!', 'success')
        except UserNotFoundError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash(f'Error adding ingredient: {e}', 'error')
    
    def get_price_info(self, name, selected_country):
        prices_ref = self.prices_ref \
            .where('country', '==', selected_country) \
            .where('dish_name', '==', name)
        prices = prices_ref.stream()

        price_state_list = []
        for price_doc in prices:
            data = price_doc.to_dict()
            price = data.get('price')
            state = data.get('state')
            timestamp = data.get('timestamp')  # adjust key if needed
            # Convert Firestore timestamp to Python datetime if necessary
            if hasattr(timestamp, 'to_datetime'):
                timestamp = timestamp.to_datetime()
            if price is not None and state is not None and timestamp is not None:
                price_state_list.append({
                    'price': price,
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