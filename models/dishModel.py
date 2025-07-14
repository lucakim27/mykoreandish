import csv
from flask import logging

class Dish:
    def __init__(self, dish_name, description, korean_name, image_url):
        self.dish_name = dish_name
        self.description = description
        self.korean_name = korean_name
        self.image_url = image_url

class DishManager:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def get_all_dishes_in_dictionary(self):
        dishes = self.get_all_dishes()
        return [
            {
                'dish_name': dish.dish_name,
                'korean_name': dish.korean_name,
                'description': dish.description,
                'image_url': dish.image_url
            }
            for dish in dishes
        ]

    def get_all_dishes(self):
        dishes = []
        try:
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    dishes.append(self.row_to_dish(row))
        except Exception as e:
            logging.info(f"Error reading CSV file: {e}")
        return dishes

    def row_to_dish(self, row):
        return Dish(
            dish_name=row.get('dish_name', ''),
            description=row.get('description', ''),
            korean_name=row.get('korean_name', ''),
            image_url=row.get('image_url', '')
        )

    def get_dish_instance(self, name):
        dishes = self.get_all_dishes()
        for dish in dishes:
            if dish.dish_name.lower() == name.lower():
                return dish
        return None
    
    def get_dish_instances(self, names):
        dishes = self.get_all_dishes()
        matched_dishes = []
        for name in names:
            for dish in dishes:
                if dish.dish_name.lower() == name.lower():
                    matched_dishes.append(dish)
                    break

        return matched_dishes

    def all_search(self):
        dishes = self.get_all_dishes()
        return dishes if dishes else [{"dish_name": "No match found", "reason": "Try relaxing the description."}]
    