from firebase_admin import firestore
from flask import flash

class AggregateManager:
    def __init__(self, db: firestore.Client):
        self.db = db
        self.TASTE_CATEGORIES = ["spiciness", "sweetness", "sourness", "temperature", "texture", "rating", "healthiness"]
    
    def add_dietary_aggregate(self, dish_name, review_data):
        aggregate_ref = self.db.collection("Aggregates").document(dish_name)
        doc = aggregate_ref.get()

        if doc.exists:
            data = doc.to_dict()
            dietary_distribution = data.get("dietary_distribution", {})

            dietary_distribution[review_data] = dietary_distribution.get(review_data, 0) + 1

            data["dietary_distribution"] = dietary_distribution
            aggregate_ref.update(data)
        else:
            aggregate_ref.set({"dietary_distribution": {review_data: 1}})
    
    def add_ingredient_aggregate(self, dish_name, review_data):
        aggregate_ref = self.db.collection("Aggregates").document(dish_name)
        doc = aggregate_ref.get()

        if doc.exists:
            data = doc.to_dict()
            ingredient_distribution = data.get("ingredient_distribution", {})

            ingredient_distribution[review_data] = ingredient_distribution.get(review_data, 0) + 1

            data["ingredient_distribution"] = ingredient_distribution
            aggregate_ref.update(data)
        else:
            aggregate_ref.set({"ingredient_distribution": {review_data: 1}})
    
    def delete_dietary_aggregate(self, dietary):
        if dietary is None:
            flash("Dietary not found!", "error")
            return

        dish_name = dietary['dish_name']
        dietary = dietary['dietary']

        aggregate_ref = self.db.collection("Aggregates").document(dish_name)
        doc = aggregate_ref.get()

        if doc.exists:
            data = doc.to_dict()
            dietary_distribution = data.get("dietary_distribution", {})

            if dietary in dietary_distribution:
                dietary_distribution[dietary] -= 1
                if dietary_distribution[dietary] <= 0:
                    del dietary_distribution[dietary]

            if dietary_distribution:
                data["dietary_distribution"] = dietary_distribution
                aggregate_ref.update(data)
            else:
                aggregate_ref.update({"dietary_distribution": firestore.DELETE_FIELD})

                updated_doc = aggregate_ref.get()
                updated_data = updated_doc.to_dict()
                if not updated_data:  
                    aggregate_ref.delete()

    def delete_ingredient_aggregate(self, ingredient):
        if ingredient is None:
            flash("Ingredient not found!", "error")
            return
        
        dish_name = ingredient['dish_name']
        ingredient = ingredient['ingredient']

        aggregate_ref = self.db.collection("Aggregates").document(dish_name)
        doc = aggregate_ref.get()

        if doc.exists:
            data = doc.to_dict()
            ingredient_distribution = data.get("ingredient_distribution", {})

            if ingredient in ingredient_distribution:
                ingredient_distribution[ingredient] -= 1
                if ingredient_distribution[ingredient] <= 0:
                    del ingredient_distribution[ingredient]

            if ingredient_distribution:
                data["ingredient_distribution"] = ingredient_distribution
                aggregate_ref.update(data)
            else:
                aggregate_ref.update({"ingredient_distribution": firestore.DELETE_FIELD})

                updated_doc = aggregate_ref.get()
                updated_data = updated_doc.to_dict()
                if not updated_data:  
                    aggregate_ref.delete()

    def update_dietary_aggregate(self, dish_name, old_dietary, new_dietary):
        dietary = {'dish_name': dish_name, 'dietary': old_dietary}
        self.delete_dietary_aggregate(dietary)
        self.add_dietary_aggregate(dish_name, new_dietary)
    
    def update_ingredient_aggregate(self, dish_name, old_ingredient, new_ingredient):
        ingredient = {'dish_name': dish_name, 'ingredient': old_ingredient}
        self.delete_ingredient_aggregate(ingredient)
        self.add_ingredient_aggregate(dish_name, new_ingredient)

    def add_aggregate(self, dish_name, review_data):
        aggregate_ref = self.db.collection("Aggregates").document(dish_name)

        doc = aggregate_ref.get()

        if doc.exists:
            data = doc.to_dict()

            total_reviews = data.get("total_reviews", 0) + 1

            for taste in self.TASTE_CATEGORIES:
                data[taste] = ((data.get(taste, 0) * data.get("total_reviews", 0)) + review_data[taste]) / total_reviews

            data["total_reviews"] = total_reviews

            aggregate_ref.update({k: v for k, v in data.items() if k not in ['dietary', 'ingredients']})

        else:
            aggregate_data = {"total_reviews": 1, **review_data}

            aggregate_ref.set(aggregate_data)
    
    def delete_aggregate(self, dish_review):
        if dish_review is None:
            flash("Taste not found!", "error")
            return
        
        dish_name = dish_review['dish_name']
        old_review_data = {
            'spiciness': int(dish_review['spiciness']),
            'sweetness': int(dish_review['sweetness']),
            'sourness': int(dish_review['sourness']),
            'temperature': int(dish_review['temperature']),
            'texture': int(dish_review['texture']),
            'rating': int(dish_review['rating']),
            'healthiness': int(dish_review['healthiness'])
        }
                        
        aggregate_ref = self.db.collection("Aggregates").document(dish_name)
        doc = aggregate_ref.get()

        if doc.exists:
            data = doc.to_dict()
            total_reviews = data.get("total_reviews", 0)

            if total_reviews == 1:
                fields_to_delete = {'temperature', 'total_reviews', 'spiciness', 'sweetness', 'healthiness', 'rating', 'texture', 'sourness'}

                dietary_distribution = data.get("dietary_distribution")
                ingredient_distribution = data.get("ingredient_distribution")

                for field in fields_to_delete:
                    if field in data:
                        del data[field]

                if dietary_distribution is None and ingredient_distribution is None:
                    aggregate_ref.delete()
                else:
                    if dietary_distribution is not None:
                        data["dietary_distribution"] = dietary_distribution
                    if ingredient_distribution is not None:
                        data["ingredient_distribution"] = ingredient_distribution

                    aggregate_ref.set(data)
            else:
                for taste in self.TASTE_CATEGORIES:
                    data[taste] = (data[taste] * total_reviews - old_review_data[taste]) / (total_reviews - 1)

                data["total_reviews"] = total_reviews - 1

                aggregate_ref.update(data)

    def update_aggregate(self, dish_name, old_review_data, new_review_data):
        aggregate_ref = self.db.collection("Aggregates").document(dish_name)
        doc = aggregate_ref.get()

        if doc.exists:
            data = doc.to_dict()
            total_reviews = data.get("total_reviews", 0)

            for taste in self.TASTE_CATEGORIES:
                data[taste] = (data.get(taste, 0) * total_reviews - old_review_data[taste]) / total_reviews

            for taste in self.TASTE_CATEGORIES:
                data[taste] = ((data.get(taste, 0) * total_reviews) + new_review_data[taste]) / total_reviews

            aggregate_ref.update({k: v for k, v in data.items() if k not in ['dietary', 'ingredients']})

        else:
            aggregate_data = {"total_reviews": 1, **new_review_data}
            aggregate_ref.set(aggregate_data)
    
    def get_dish_aggregate(self, dish_name):
        doc_ref = self.db.collection("Aggregates").document(dish_name)
        doc = doc_ref.get()

        if doc.exists:
            return doc.to_dict()
        return {}
    
    def initialize_all_aggregates(self):
        reviews_ref = self.db.collection("UserSelections")
        dietaries_ref = self.db.collection("Dietaries")
        ingredients_ref = self.db.collection("Ingredients")
        aggregates_ref = self.db.collection("Aggregates")

        dishes = set()
        reviews = reviews_ref.stream()
        for review in reviews:
            dish_name = review.to_dict().get("dish_name")
            if dish_name:
                dishes.add(dish_name)

        if not dishes:
            return

        for dish_name in dishes:
            aggregate_ref = aggregates_ref.document(dish_name)
            doc = aggregate_ref.get()

            if doc.exists:
                continue

            dish_reviews = reviews_ref.where("dish_name", "==", dish_name).stream()
            total_reviews = 0
            taste_sums = {taste: 0.0 for taste in self.TASTE_CATEGORIES}

            for review in dish_reviews:
                review_data = review.to_dict()
                total_reviews += 1
                for taste in self.TASTE_CATEGORIES:
                    taste_sums[taste] += review_data.get(taste, 0)

            dietary_reviews = dietaries_ref.where("dish_name", "==", dish_name).stream()
            dietary_count = {}

            for dietary in dietary_reviews:
                dietary_data = dietary.to_dict().get("dietary")
                if dietary_data:
                    dietary_count[dietary_data] = dietary_count.get(dietary_data, 0) + 1
            
            ingredient_reviews = ingredients_ref.where("dish_name", "==", dish_name).stream()
            ingredient_count = {}

            for ingredient in ingredient_reviews:
                ingredient_data = ingredient.to_dict().get("ingredient")
                if ingredient_data:
                    ingredient_count[ingredient_data] = ingredient_count.get(ingredient_data, 0) + 1
            
            if total_reviews == 0:
                aggregate_data = {"total_reviews": 0, **{taste: 0.0 for taste in self.TASTE_CATEGORIES}}
            else:
                aggregate_data = {"total_reviews": total_reviews}
                for taste in self.TASTE_CATEGORIES:
                    aggregate_data[taste] = taste_sums[taste] / total_reviews
                
                if dietary_count:
                    aggregate_data["dietary_distribution"] = dietary_count
                if ingredient_count:
                    aggregate_data["ingredient_distribution"] = ingredient_count
            
            aggregate_ref.set(aggregate_data)
    
    def get_dishes_by_aspect_range(self, aspect, user_level, tolerance=0.5):
        if aspect not in self.TASTE_CATEGORIES:
            raise ValueError(f"Invalid aspect '{aspect}'. Choose from: {self.TASTE_CATEGORIES}")

        min_value = user_level - tolerance
        max_value = user_level + tolerance

        aggregates_ref = self.db.collection("Aggregates")
        query = aggregates_ref.where(aspect, ">=", min_value).where(aspect, "<", max_value)
        results = query.stream()

        matching_dishes = []

        for doc in results:
            dish_name = doc.id
            matching_dishes.append(dish_name)

        return matching_dishes
