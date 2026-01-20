import csv
import logging

class DishManager:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def get_all_dishes(self):
        dishes = []
        try:
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    dishes.append(
                        {
                            'dish_name': row.get('dish_name', ''),
                            'description': row.get('description', ''),
                            'korean_name': row.get('korean_name', ''),
                            'image_url': row.get('image_url', '')
                        }
                    )
        except Exception as e:
            logging.info(f"Error reading CSV file: {e}")
        return dishes

    def get_dish_instance(self, name):
        dishes = self.get_all_dishes()
        for dish in dishes:
            if dish['dish_name'].lower() == name.lower():
                return dish
        return None
    
    def get_dishes_instance(self, names):
        dishes = self.get_all_dishes()
        matched_dishes = []
        for name in names:
            for dish in dishes:
                if dish['dish_name'].lower() == name.lower():
                    matched_dishes.append(dish)
                    break
        return matched_dishes