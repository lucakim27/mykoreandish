from flask import flash


class Price:
    def __init__(self, name, description, adjectives):
        self.name = name
        self.description = description
        self.adjectives = adjectives.split(';') if isinstance(adjectives, str) else adjectives

class PriceManager:
    def __init__(self, db, firestore):
        self.dishes_ref = db.collection('Dishes')
        self.users_ref = db.collection('Users')
        self.prices_ref = db.collection('Prices')
        self.firestore = firestore
    
    def add_price(self, google_id, dish_name, price, location):
        user_ref = self.users_ref.where('google_id', '==', google_id)
        user = user_ref.get()

        if not user:
            raise ValueError("User does not exist.")
        
        dish_ref = self.dishes_ref.document(dish_name)  # Ensure dish_name is used correctly
        dish = dish_ref.get()
        
        if not dish:
            raise ValueError("Dish does not exist.")
        
        # Add selection to the UserSelections collection with rating as None
        self.prices_ref.add({
            'google_id': google_id,
            'dish_name': dish_name,
            'price': price,
            'location': location,
            'timestamp': self.firestore.SERVER_TIMESTAMP
        })
    
    def update_price(self, history_id, price):
        if not history_id or not price:
            flash('Invalid input for price.', 'error')
            return False

        try:
            price_ref = self.prices_ref.document(history_id)
            price_ref.update({
                'price': price
            })
            flash('Price saved successfully!', 'success')
            return True
        except Exception as e:
            flash(f'Error saving price: {e}', 'error')
            return False
    
    def delete_price(self, history_id):
        """Delete a history item from the 'UserSelections' collection."""
        try:
            price_ref = self.prices_ref.document(history_id)
            price_ref.delete()
            flash('Price review deleted successfully.', 'success')
            return True
        except Exception as e:
            flash('An error occurred while deleting the price review.', 'error')
            print(f"Error: {e}")
            return False
    
    def get_price(self, dish_name):
        price_ref = self.prices_ref.where('dish_name', '==', dish_name)
        prices = price_ref.stream()
        
        prices_list = [{
                'id': price.id,  # Firestore document ID as 'id'
                'dish_name': price.to_dict().get('dish_name'),
                'timestamp': price.to_dict().get('timestamp'),
                'location': price.to_dict().get('location'),
                'google_id': price.to_dict().get('google_id'),
                'price': price.to_dict().get('price')
            } for price in prices]
    
        if not prices_list:
            return []

        # Sort the prices list by 'timestamp' in descending order
        prices_list.sort(key=lambda x: x['timestamp'], reverse=True)
        return prices_list
    
    def total_review_len(self):
        price_ref = self.prices_ref
        prices = price_ref.stream()

        if not prices:
            return []
        
        total_price = {}

        for price in prices:
            if price.to_dict().get('dish_name') in total_price:
                total_price[price.to_dict().get('dish_name')] += 1
            else:
                total_price[price.to_dict().get('dish_name')] = 1
        
        return total_price
    
    def get_price_history(self, google_id):
        price_ref = self.prices_ref.where('google_id', '==', google_id)
        prices = price_ref.stream()
        
        prices_list = [{
                'id': price.id,  # Firestore document ID as 'id'
                'dish_name': price.to_dict().get('dish_name'),
                'timestamp': price.to_dict().get('timestamp'),
                'location': price.to_dict().get('location'),
                'price': price.to_dict().get('price')
            } for price in prices]
    
        if not prices_list:
            return []

        # Sort the prices list by 'timestamp' in descending order
        prices_list.sort(key=lambda x: x['timestamp'], reverse=True)
        return prices_list