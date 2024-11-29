from firebase_admin import firestore
import re
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
    def __init__(self, dishes_ref, users_ref, user_selections_ref):
        self.dishes_ref = dishes_ref
        self.users_ref = users_ref
        self.user_selections_ref = user_selections_ref

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