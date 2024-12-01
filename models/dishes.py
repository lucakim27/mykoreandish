import re
from flask import flash, redirect
from nltk.corpus import stopwords

class Dish:
    def __init__(self, dish_name, description, adjectives):
        self.dish_name = dish_name
        self.description = description
        self.adjectives = adjectives.split(';') if isinstance(adjectives, str) else adjectives

    def matches_description(self, input):
        # Preprocess input: tokenize and remove stop words
        stop_words = set(stopwords.words('english'))
        tokens = re.findall(r'\b\w+\b', input)  # Extract words from input
        filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]

        # Perform case-insensitive matching
        description_lower = self.description.lower()
        adjectives_lower = [adj.lower() for adj in self.adjectives]

        # Check if any meaningful token matches the description or adjectives
        for token in filtered_tokens:
            if token in description_lower or token in adjectives_lower:
                return True

        return False

class DishManager:
    def __init__(self, db):
        self.dishes_ref = db.collection('Dishes')

    def get_all_dishes(self):
        dishes = self.dishes_ref.stream()
        return [self.row_to_dish(dish) for dish in dishes]

    def row_to_dish(self, dish_doc):
        data = dish_doc.to_dict()
        return Dish(
            dish_name=data.get('dish_name', ''),
            description=data.get('description', ''),
            adjectives=data.get('adjectives', '')
        )

    def make_recommendation(self, input):
        dishes = self.get_all_dishes()
        filtered_dishes = [dish for dish in dishes if dish.matches_description(input)]
        if filtered_dishes:
            return filtered_dishes
        else:
            return [{"dish_name": "No match found", "reason": "Try relaxing the filters."}]

    def get_dish_instance(self, name):
        try:
            dish_query = self.dishes_ref.where('dish_name', '==', name).limit(1)
            dishes = list(dish_query.stream())
            if dishes:
                return self.row_to_dish(dishes[0])
            else:
                print(f"No dish found with name: '{name}'")
                return None
        except Exception as e:
            print(f"Error fetching dish by name: {e}")
            return None
    
    def add_dish(self, dish_name, description, adjectives):
        if not dish_name or not description or not adjectives:
            flash('All fields are required!', 'error')
            return redirect('/admin')

        # Add the food item to the Firestore 'foods' collection
        self.dishes_ref.add({
            'dish_name': dish_name,
            'description': description,
            'adjectives': adjectives  # Store adjectives as a list
        })
        
        flash('Food added successfully!', 'success')