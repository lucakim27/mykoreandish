import sqlite3
from contextlib import closing
from datetime import datetime

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
    def get_all_dishes(self):
        with closing(sqlite3.connect('data/app.db')) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM dishes')
            rows = cursor.fetchall()
        return [self.row_to_dish(row) for row in rows]

    def row_to_dish(self, row):
        return Dish(
            dish_name=row[1],
            dietary_restrictions=row[2],
            health_goals=row[3],
            meal_type=row[4],
            time_to_prepare=row[5],
            ingredient_availability=row[6],
            cooking_equipment=row[7],
            budget=row[8],
            occasion=row[9],
            taste_preferences=row[10],
            sustainability=row[11]
        )

    def make_recommendation(self, **criteria):
        dishes = self.get_all_dishes()
        filtered_dishes = [dish for dish in dishes if dish.matches_criteria(criteria)]
        if filtered_dishes:
            return filtered_dishes
        else:
            return [{"dish_name": "No match found", "reason": "Try relaxing the filters."}]

    def get_food_by_name(self, name):
        with closing(sqlite3.connect('data/app.db')) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM dishes WHERE LOWER(dish_name) = ?', (name.lower(),))
            row = cursor.fetchone()
        if row:
            return self.row_to_dish(row)
        return None

    def add_selection(self, username, dish_name):
        with sqlite3.connect('data/app.db') as conn:
            cursor = conn.cursor()

            # Get user ID
            cursor.execute('SELECT id FROM Users WHERE username = ?', (username,))
            user_id = cursor.fetchone()
            if not user_id:
                raise ValueError("User does not exist.")
            user_id = user_id[0]

            # Get dish ID
            cursor.execute('SELECT id FROM Dishes WHERE dish_name = ?', (dish_name,))
            dish_id = cursor.fetchone()
            if not dish_id:
                raise ValueError("Dish does not exist.")
            dish_id = dish_id[0]

            # Insert into UserSelections
            cursor.execute(
                'INSERT INTO UserSelections (user_id, dish_id, timestamp) VALUES (?, ?, ?)',
                (user_id, dish_id, datetime.now())
            )
            conn.commit()

    def get_user_history(self, username):
        with sqlite3.connect('data/app.db') as conn:
            cursor = conn.cursor()

            # Get user ID
            cursor.execute('SELECT id FROM Users WHERE username = ?', (username,))
            user_id = cursor.fetchone()
            if not user_id:
                return []  # No history if user doesn't exist
            user_id = user_id[0]

            # Get history of dishes selected by the user along with ratings
            cursor.execute('''
                SELECT UserSelections.id, Dishes.dish_name, UserSelections.timestamp, UserSelections.rating
                FROM UserSelections
                JOIN Dishes ON UserSelections.dish_id = Dishes.id
                WHERE UserSelections.user_id = ?
                ORDER BY UserSelections.timestamp DESC
            ''', (user_id,))
            return cursor.fetchall()
