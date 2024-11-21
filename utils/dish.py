import csv

class Dish:
    def __init__(self, dish_name, dietary_restrictions, health_goals, meal_type, time_to_prepare,
                 ingredient_availability, cooking_equipment, budget, occasion, taste_preferences, sustainability):
        self.dish_name = dish_name
        self.dietary_restrictions = dietary_restrictions.split(';')
        self.health_goals = health_goals.split(';')
        self.meal_type = meal_type.split(';')
        self.time_to_prepare = time_to_prepare
        self.ingredient_availability = ingredient_availability
        self.cooking_equipment = cooking_equipment.split(';')
        self.budget = budget
        self.occasion = occasion.split(';')
        self.taste_preferences = taste_preferences.split(';')
        self.sustainability = sustainability

    def matches_criteria(self, criteria):
        for key, value in criteria.items():
            if value != 'any':
                attribute = getattr(self, key, None)
                if not attribute:
                    return False
                
                if isinstance(attribute, list):
                    if value.lower() not in map(str.lower, map(str.strip, attribute)):
                        return False
                else:
                    if value.lower() != attribute.lower():
                        return False
        return True

class DishManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dishes = self.load_data()

    def load_data(self):
        dishes = []
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                dish = Dish(
                    dish_name=row['dish_name'],
                    dietary_restrictions=row['dietary_restrictions'],
                    health_goals=row['health_goals'],
                    meal_type=row['meal_type'],
                    time_to_prepare=row['time_to_prepare'],
                    ingredient_availability=row['ingredient_availability'],
                    cooking_equipment=row['cooking_equipment'],
                    budget=row['budget'],
                    occasion=row['occasion'],
                    taste_preferences=row['taste_preferences'],
                    sustainability=row['sustainability']
                )
                dishes.append(dish)
        return dishes

    def make_recommendation(self, **criteria):
        filtered_dishes = [dish for dish in self.dishes if dish.matches_criteria(criteria)]
        if filtered_dishes:
            return filtered_dishes
        else:
            return [{"dish_name": "No match found", "reason": "Try relaxing the filters."}]
    
    def get_food_by_name(self, name):
        for dish in self.dishes:
            if dish.dish_name.lower() == name.lower():
                return dish
        return None
