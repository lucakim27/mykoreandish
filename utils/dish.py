from firebase_admin import firestore

class Dish:
    def __init__(self, dish_name, dietary_restrictions, health_goals, meal_type, time_to_prepare,
                 ingredient_availability, cooking_equipment, budget, occasion, taste_preferences, sustainability):
        self.dish_name = dish_name
        self.dietary_restrictions = dietary_restrictions.split(';') if isinstance(dietary_restrictions, str) else dietary_restrictions
        self.health_goals = health_goals.split(';') if isinstance(health_goals, str) else health_goals
        self.meal_type = meal_type.split(';') if isinstance(meal_type, str) else meal_type
        self.time_to_prepare = time_to_prepare
        self.ingredient_availability = ingredient_availability
        self.cooking_equipment = cooking_equipment.split(';') if isinstance(cooking_equipment, str) else cooking_equipment
        self.budget = budget
        self.occasion = occasion.split(';') if isinstance(occasion, str) else occasion
        self.taste_preferences = taste_preferences.split(';') if isinstance(taste_preferences, str) else taste_preferences
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
    def __init__(self, dishes_ref, users_ref, user_selections_ref, requests_ref):
        self.dishes_ref = dishes_ref
        self.users_ref = users_ref
        self.user_selections_ref = user_selections_ref
        self.requests_ref = requests_ref

    def get_all_dishes(self):
        dishes = self.dishes_ref.stream()  # Firestore stream of dishes
        return [self.row_to_dish(dish) for dish in dishes]

    def row_to_dish(self, dish_doc):
        data = dish_doc.to_dict()  # Get document data as a dictionary
        return Dish(
            dish_name=data.get('dish_name', ''),  # Correctly get dish_name from the document field
            dietary_restrictions=data.get('dietary_restrictions', ''),
            health_goals=data.get('health_goals', ''),
            meal_type=data.get('meal_type', ''),
            time_to_prepare=data.get('time_to_prepare', ''),
            ingredient_availability=data.get('ingredient_availability', ''),
            cooking_equipment=data.get('cooking_equipment', ''),
            budget=data.get('budget', ''),
            occasion=data.get('occasion', ''),
            taste_preferences=data.get('taste_preferences', ''),
            sustainability=data.get('sustainability', '')
        )

    def make_recommendation(self, **criteria):
        dishes = self.get_all_dishes()
        filtered_dishes = [dish for dish in dishes if dish.matches_criteria(criteria)]
        if filtered_dishes:
            return filtered_dishes
        else:
            return [{"dish_name": "No match found", "reason": "Try relaxing the filters."}]

    def add_selection(self, google_id, dish_name, rating=None):
        """Add a food selection without a rating initially."""
        user_ref = self.users_ref.where('google_id', '==', google_id)
        user = user_ref.get()

        if not user:
            raise ValueError("User does not exist.")
        
        dish_ref = self.dishes_ref.document(dish_name)  # Ensure dish_name is used correctly
        dish = dish_ref.get()
        
        if not dish:
            raise ValueError("User does not exist.")
        
        # Add selection to the UserSelections collection with rating as None
        self.user_selections_ref.add({
            'google_id': google_id,
            'dish_name': dish_name,
            'rating': rating,  # This will be None if no rating is provided
            'timestamp': firestore.SERVER_TIMESTAMP
        })

    def get_user_history(self, google_id):
        try:
            # Query to get the user document by google_id
            user_ref = self.users_ref.where('google_id', '==', google_id)
            user_docs = user_ref.get()

            if not user_docs:
                return []  # Return empty list if user doesn't exist

            # Assuming only one user document will match, get the first document
            user = user_docs[0]  # user_docs is a list of documents

            # Query to get all selections by the user using the google_id
            user_selections_ref = self.user_selections_ref.where('google_id', '==', user.to_dict().get('google_id'))
            selections = user_selections_ref.stream()  # Stream selections

            # Return user selections as a list of dictionaries
            return [{
                'id': selection.id,  # Firestore document ID as 'id'
                'dish_name': selection.to_dict().get('dish_name'),
                'timestamp': selection.to_dict().get('timestamp'),
                'rating': selection.to_dict().get('rating')
            } for selection in selections]

        except Exception as e:
            print(f"Error retrieving user history: {e}")
            return []  # Return an empty list if an error occurs

    def get_food_by_name(self, name):
        """Fetch a dish by its name from Firestore."""
        try:
            # Query the 'Dishes' collection for a document with the given dish_name
            dish_ref = self.dishes_ref.where('dish_name', '==', name).limit(1)
            dishes = dish_ref.stream()

            # If a dish is found, return it
            for dish_doc in dishes:
                return self.row_to_dish(dish_doc)
            
            # If no dish is found, return None
            return None
        except Exception as e:
            print(f"Error fetching dish by name: {e}")
            return None
    
    def add_food_request(self, food_name, description, criteria, image_url=None):
        """
        Store a user food request in the Firestore 'Requests' collection.
        
        :param food_name: Name of the requested food.
        :param description: Description of the requested food.
        :param criteria: A dictionary containing the criteria (e.g., dietary restrictions, meal type).
        :param image_url: Optional image URL for the requested food.
        """
        try:
            # Create a dictionary for the request data
            request_data = {
                'food_name': food_name,
                'description': description,
                'criteria': criteria,  # Store all criteria as a dictionary
                'image_url': image_url,
                'timestamp': firestore.SERVER_TIMESTAMP  # Add a timestamp
            }
            
            # Add the request to the 'Requests' collection
            self.requests_ref.add(request_data)
            
            print(f"Request for '{food_name}' added successfully!")
            return {"success": True, "message": f"Request for '{food_name}' added successfully!"}
        except Exception as e:
            print(f"Error adding request: {e}")
            return {"success": False, "error": str(e)}
