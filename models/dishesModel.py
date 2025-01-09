import csv
import re
from flask import flash, redirect
from nltk.corpus import stopwords

class Dish:
    def __init__(self, dish_name, description):
        self.dish_name = dish_name
        self.description = description

    def matches_description(self, input):
        # Preprocess input: tokenize and remove stop words
        stop_words = set(stopwords.words('english'))
        tokens = re.findall(r'\b\w+\b', input)  # Extract words from input
        filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]

        # Perform case-insensitive matching
        dish_name_lower = self.dish_name.lower()
        description_lower = self.description.lower()

        # Check if any meaningful token matches the dish_name or description
        for token in filtered_tokens:
            if token in dish_name_lower or token in description_lower:
                return True

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
            description=row.get('description', '')
        )

    def get_dish_instance(self, name):
        dishes = self.get_all_dishes()  # Fetch all dishes from the CSV
        for dish in dishes:
            if dish.dish_name.lower() == name.lower():  # Case-insensitive matching
                return dish
        print(f"No dish found with name: '{name}'")
        return None
    
    def get_dish_instances(self, names):
        dishes = self.get_all_dishes()  # Fetch all dishes from the CSV
        matched_dishes = []
        for name in names:
            for dish in dishes:
                if dish.dish_name.lower() == name.lower():  # Case-insensitive matching
                    matched_dishes.append(dish)
                    break
            else:
                print(f"No dish found with name: '{name}'")
        return matched_dishes

    def description_search(self, description):
        dishes = self.get_all_dishes()
        if description:
            filtered_dishes = [dish for dish in dishes if dish.matches_description(description)]
        else:
            return [{"dish_name": "No match found", "reason": "Try providing a description."}]
        
        return filtered_dishes if filtered_dishes else [{"dish_name": "No match found", "reason": "Try relaxing the description."}]
    
    def all_search(self):
        dishes = self.get_all_dishes()
        return dishes if dishes else [{"dish_name": "No match found", "reason": "Try relaxing the description."}]

    def add_dish(self, dish_name, description):
        if not dish_name or not description:
            flash('All fields are required!', 'error')
            return redirect('/admin')

        # Add the food item to the CSV file
        try:
            with open(self.csv_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['dish_name', 'description'])
                writer.writerow({
                    'dish_name': dish_name,
                    'description': description
                })
            flash('Food added successfully!', 'success')
        except Exception as e:
            flash(f"Error adding dish: {e}", 'error')
