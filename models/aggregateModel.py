from firebase_admin import firestore

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
    
    def delete_dietary_aggregate(self, dish_name, dietary):
        aggregate_ref = self.db.collection("Aggregates").document(dish_name)
        doc = aggregate_ref.get()

        if doc.exists:
            data = doc.to_dict()
            dietary_distribution = data.get("dietary_distribution", {})

            if dietary in dietary_distribution:
                dietary_distribution[dietary] -= 1
                if dietary_distribution[dietary] <= 0:
                    del dietary_distribution[dietary]

            if dietary_distribution:  # Update only if there are remaining dietary entries
                data["dietary_distribution"] = dietary_distribution
                aggregate_ref.update(data)
            else:  
                # Remove the dietary_distribution field instead of deleting the document
                aggregate_ref.update({"dietary_distribution": firestore.DELETE_FIELD})

                # Check if other fields exist; if none, delete the document
                updated_doc = aggregate_ref.get()
                updated_data = updated_doc.to_dict()
                if not updated_data:  
                    aggregate_ref.delete()

    def delete_ingredient_aggregate(self, dish_name, ingredient):
        aggregate_ref = self.db.collection("Aggregates").document(dish_name)
        doc = aggregate_ref.get()

        if doc.exists:
            data = doc.to_dict()
            ingredient_distribution = data.get("ingredient_distribution", {})

            if ingredient in ingredient_distribution:
                ingredient_distribution[ingredient] -= 1
                if ingredient_distribution[ingredient] <= 0:
                    del ingredient_distribution[ingredient]

            if ingredient_distribution:  # Update only if there are remaining ingredient entries
                data["ingredient_distribution"] = ingredient_distribution
                aggregate_ref.update(data)
            else:  
                # Remove the ingredient_distribution field instead of deleting the document
                aggregate_ref.update({"ingredient_distribution": firestore.DELETE_FIELD})

                # Check if other fields exist; if none, delete the document
                updated_doc = aggregate_ref.get()
                updated_data = updated_doc.to_dict()
                if not updated_data:  
                    aggregate_ref.delete()

    def update_dietary_aggregate(self, dish_name, old_dietary, new_dietary):
        self.delete_dietary_aggregate(dish_name, old_dietary)
        self.add_dietary_aggregate(dish_name, new_dietary)
    
    def update_ingredient_aggregate(self, dish_name, old_ingredient, new_ingredient):
        self.delete_ingredient_aggregate(dish_name, old_ingredient)
        self.add_ingredient_aggregate(dish_name, new_ingredient)

    def add_aggregate(self, dish_name, review_data):
        aggregate_ref = self.db.collection("Aggregates").document(dish_name)

        doc = aggregate_ref.get()

        if doc.exists:
            data = doc.to_dict()

            # Initialize total_reviews if it doesn't exist
            total_reviews = data.get("total_reviews", 0) + 1

            # Update taste categories
            for taste in self.TASTE_CATEGORIES:
                data[taste] = ((data.get(taste, 0) * data.get("total_reviews", 0)) + review_data[taste]) / total_reviews

            data["total_reviews"] = total_reviews

            # Update aggregate excluding dietary and ingredient fields
            aggregate_ref.update({k: v for k, v in data.items() if k not in ['dietary', 'ingredients']})

        else:
            aggregate_data = {"total_reviews": 1, **review_data}

            # Set new aggregate document, excluding dietary and ingredient fields
            aggregate_ref.set(aggregate_data)
    
    def delete_aggregate(self, dish_name, old_review_data):
        aggregate_ref = self.db.collection("Aggregates").document(dish_name)
        doc = aggregate_ref.get()

        if doc.exists:
            data = doc.to_dict()
            total_reviews = data.get("total_reviews", 0)

            if total_reviews == 1:
                # Prepare to delete taste fields and total_reviews
                fields_to_delete = {'temperature', 'total_reviews', 'spiciness', 'sweetness', 'healthiness', 'rating', 'texture', 'sourness'}

                # Get existing fields or set as empty only if they exist
                dietary_distribution = data.get("dietary_distribution")  # This will return None if not present
                ingredient_distribution = data.get("ingredient_distribution")  # This will return None if not present

                # Delete taste fields and total_reviews
                for field in fields_to_delete:
                    if field in data:
                        del data[field]

                # Check if both dietary_distribution and ingredient_distribution are missing
                if dietary_distribution is None and ingredient_distribution is None:
                    aggregate_ref.delete()  # Delete the entire document if no reviews or distributions remain
                else:
                    # Add back the dietary_distribution and ingredient_distribution only if they existed
                    if dietary_distribution is not None:
                        data["dietary_distribution"] = dietary_distribution
                    if ingredient_distribution is not None:
                        data["ingredient_distribution"] = ingredient_distribution

                    # Update the document in Firebase
                    aggregate_ref.set(data)  # Using set to replace the document
            else:
                # Update the aggregate with new totals after review deletion
                for taste in self.TASTE_CATEGORIES:
                    data[taste] = (data[taste] * total_reviews - old_review_data[taste]) / (total_reviews - 1)

                data["total_reviews"] = total_reviews - 1

                # Update the document with the modified data
                aggregate_ref.update(data)

            return True
        else:
            return False

    def update_aggregate(self, dish_name, old_review_data, new_review_data):
        aggregate_ref = self.db.collection("Aggregates").document(dish_name)
        doc = aggregate_ref.get()

        if doc.exists:
            data = doc.to_dict()
            # Initialize total_reviews if it doesn't exist
            total_reviews = data.get("total_reviews", 0)

            # Update taste categories based on old review data
            for taste in self.TASTE_CATEGORIES:
                data[taste] = (data.get(taste, 0) * total_reviews - old_review_data[taste]) / total_reviews

            # Add new review data to taste categories
            for taste in self.TASTE_CATEGORIES:
                data[taste] = ((data.get(taste, 0) * total_reviews) + new_review_data[taste]) / total_reviews

            # Update aggregate excluding dietary and ingredient fields
            aggregate_ref.update({k: v for k, v in data.items() if k not in ['dietary', 'ingredients']})

        else:
            aggregate_data = {"total_reviews": 1, **new_review_data}
            # Set new aggregate document, excluding dietary and ingredient fields
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
                
                if dietary_count:  # Only add if not empty
                    aggregate_data["dietary_distribution"] = dietary_count
                if ingredient_count:  # Only add if not empty
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
