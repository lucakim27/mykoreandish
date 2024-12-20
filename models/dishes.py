import csv
import re
from flask import flash, redirect
from nltk.corpus import stopwords

class Dish:
    def __init__(self, dish_name, description, adjectives, spiciness, dietary, ingredients):
        self.dish_name = dish_name
        self.description = description
        self.adjectives = adjectives.split(';') if isinstance(adjectives, str) else adjectives
        self.spiciness = spiciness
        self.dietary = dietary.split(';') if isinstance(dietary, str) else dietary
        self.ingredients = ingredients.split(';') if isinstance(ingredients, str) else ingredients

    def matches_description(self, input):
        # Preprocess input: tokenize and remove stop words
        stop_words = set(stopwords.words('english'))
        tokens = re.findall(r'\b\w+\b', input)  # Extract words from input
        filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]

        # Perform case-insensitive matching
        dish_name_lower = self.dish_name.lower()
        description_lower = self.description.lower()
        adjectives_lower = [adj.lower() for adj in self.adjectives]
        spiciness_lower = self.spiciness.lower()
        dietary_lower = [die.lower() for die in self.dietary]
        ingredients_lower = [ing.lower() for ing in self.ingredients]

        # Check if any meaningful token matches the description or adjectives
        for token in filtered_tokens:
            if token in dish_name_lower or token in description_lower or token in adjectives_lower or token in spiciness_lower or token in dietary_lower or token in ingredients_lower:
                return True

        return False
    
    def filter_criteria(self, adjectives, spiciness, dietary, ingredients):
        adjectives_input = [adj for adj in self.adjectives]
        spiciness_input = self.spiciness
        dietary_input = [die for die in self.dietary]
        ingredients_input = [ing for ing in self.ingredients]
        if adjectives == 'Any' and spiciness == 'Any' and dietary == 'Any' and ingredients == 'Any':
            return True
        elif adjectives in adjectives_input or spiciness == spiciness_input or dietary in dietary_input or ingredients in ingredients_input:
            return True
        else:
            return False

    
class DishManager:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def get_all_dishes(self):
        dishes = []
        try:
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    dishes.append(self.row_to_dish(row))
        except Exception as e:
            print(f"Error reading CSV file: {e}")
        return dishes

    def row_to_dish(self, row):
        return Dish(
            dish_name=row.get('dish_name', ''),
            description=row.get('description', ''),
            adjectives=row.get('adjectives', ''),
            spiciness=row.get('spiciness', ''),
            dietary=row.get('dietary', ''),
            ingredients=row.get('ingredients', '')
        )

    def get_dish_instance(self, name):
        dishes = self.get_all_dishes()  # Fetch all dishes from the CSV
        for dish in dishes:
            if dish.dish_name.lower() == name.lower():  # Case-insensitive matching
                return dish
        print(f"No dish found with name: '{name}'")
        return None

    def make_recommendation(self, description, adjectives, spiciness, dietary, ingredients):
        dishes = self.get_all_dishes()
        if description is None:
            filtered_dishes = [dish for dish in dishes if dish.filter_criteria(adjectives, spiciness, dietary, ingredients)]
        else:
            filtered_dishes = [dish for dish in dishes if dish.matches_description(description)]
        if filtered_dishes:
            return filtered_dishes
        else:
            return [{"dish_name": "No match found", "reason": "Try relaxing the filters."}]
    
    def filter_criteria(self):
        dishes = self.get_all_dishes()
        adjectives = set()
        spiciness = set()
        dietary = set()
        ingredients = set()

        for dish in dishes:
            if dish.adjectives:
                adjectives.update(dish.adjectives)
            if dish.spiciness:
                spiciness.add(dish.spiciness)
            if dish.dietary:
                dietary.update(dish.dietary)
            if dish.ingredients:
                ingredients.update(dish.ingredients)

        return adjectives, spiciness, dietary, ingredients

    def add_dish(self, dish_name, description, adjectives, spiciness, dietary, ingredients):
        if not dish_name or not description or not adjectives:
            flash('All fields are required!', 'error')
            return redirect('/admin')

        # Add the food item to the CSV file
        try:
            with open(self.csv_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['dish_name', 'description', 'adjectives', 'spiciness', 'dietary', 'ingredients'])
                writer.writerow({
                    'dish_name': dish_name,
                    'description': description,
                    'adjectives': adjectives,
                    'spiciness': spiciness,
                    'dietary': dietary,
                    'ingredients': ingredients
                })
            flash('Food added successfully!', 'success')
        except Exception as e:
            flash(f"Error adding dish: {e}", 'error')
