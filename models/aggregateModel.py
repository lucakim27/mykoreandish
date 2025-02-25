from firebase_admin import firestore

class AggregateManager:
    def __init__(self, db: firestore.Client):
        self.db = db
        self.TASTE_CATEGORIES = ["spiciness", "sweetness", "sourness", "temperature", "texture", "rating", "healthiness"]

    def add_aggregate(self, dish_name, review_data):
        aggregate_ref = self.db.collection("Aggregates").document(dish_name)

        doc = aggregate_ref.get()

        if doc.exists:
            data = doc.to_dict()
            total_reviews = data["total_reviews"] + 1

            for taste in self.TASTE_CATEGORIES:
                data[taste] = ((data[taste] * data["total_reviews"]) + review_data[taste]) / total_reviews

            data["total_reviews"] = total_reviews

            aggregate_ref.update(data)
        else:
            aggregate_data = {"total_reviews": 1, **review_data}
            aggregate_ref.set(aggregate_data)

        print(f"Review added for {dish_name} and aggregates updated.")
    
    def delete_aggregate(self, dish_name, old_review_data):
        aggregate_ref = self.db.collection("Aggregates").document(dish_name)
        doc = aggregate_ref.get()

        if doc.exists:
            data = doc.to_dict()
            total_reviews = data["total_reviews"]

            if total_reviews == 1:
                aggregate_ref.delete()
                print(f"Review for {dish_name} has been deleted, and aggregate has been removed.")
                return True
            else:
                for taste in self.TASTE_CATEGORIES:
                    data[taste] = (data[taste] * total_reviews - old_review_data[taste]) / (total_reviews - 1)

                data["total_reviews"] = total_reviews - 1

                aggregate_ref.update(data)

                print(f"Review for {dish_name} has been deleted and aggregates updated.")
                return True
        else:
            print(f"No aggregate found for {dish_name}.")
            return False
    
    def update_aggregate(self, dish_name, old_review_data, new_review_data):
        aggregate_ref = self.db.collection("Aggregates").document(dish_name)
        doc = aggregate_ref.get()

        if doc.exists:
            data = doc.to_dict()
            total_reviews = data["total_reviews"]

            for taste in self.TASTE_CATEGORIES:
                data[taste] = (data[taste] * total_reviews - old_review_data[taste]) / total_reviews

            for taste in self.TASTE_CATEGORIES:
                data[taste] = ((data[taste] * total_reviews) + new_review_data[taste]) / total_reviews

            aggregate_ref.update(data)

            print(f"Aggregates updated for {dish_name}.")
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
        aggregates_ref = self.db.collection("Aggregates")

        dishes = set()
        reviews = reviews_ref.stream()
        for review in reviews:
            dish_name = review.to_dict().get("dish_name")
            if dish_name:
                dishes.add(dish_name)

        if not dishes:
            print("No dishes found in UserSelections.")
            return

        print(f"Found {len(dishes)} unique dishes. Initializing aggregates...")

        for dish_name in dishes:
            aggregate_ref = aggregates_ref.document(dish_name)
            doc = aggregate_ref.get()

            if doc.exists:
                print(f"Aggregate for {dish_name} already exists. Skipping.")
                continue

            dish_reviews = reviews_ref.where("dish_name", "==", dish_name).stream()
            
            total_reviews = 0
            taste_sums = {taste: 0.0 for taste in self.TASTE_CATEGORIES}

            for review in dish_reviews:
                review_data = review.to_dict()
                total_reviews += 1
                for taste in self.TASTE_CATEGORIES:
                    taste_sums[taste] += review_data.get(taste, 0)

            if total_reviews == 0:
                print(f"⚠️ No existing reviews for {dish_name}. Initializing empty aggregate.")
                aggregate_data = {"total_reviews": 0, **{taste: 0.0 for taste in self.TASTE_CATEGORIES}}
            else:
                aggregate_data = {"total_reviews": total_reviews}
                for taste in self.TASTE_CATEGORIES:
                    aggregate_data[taste] = taste_sums[taste] / total_reviews

            aggregate_ref.set(aggregate_data)
            print(f"Aggregate initialized for {dish_name} with {total_reviews} reviews.")

    # def get_top_n_by_aspect(self, top_n=3):
    #     aggregates_ref = self.db.collection("Aggregates")
        
    #     taste_categories = ["spiciness", "sweetness", "sourness", "temperature", "texture", "rating", "healthiness", "total_reviews"]
        
    #     top_dishes_by_aspect = {}

    #     for aspect in taste_categories:
            
    #         query = aggregates_ref.order_by(aspect, direction=firestore.Query.DESCENDING).limit(top_n)
    #         results = query.stream()

    #         top_dishes = []

    #         for doc in results:
    #             dish_name = doc.id
    #             data = doc.to_dict()
    #             aspect_value = data.get(aspect, 0)
    #             top_dishes.append({"dish_name": dish_name, aspect: aspect_value})

    #         if top_dishes:
    #             top_dishes_by_aspect[aspect] = top_dishes
    #         else:
    #             top_dishes_by_aspect[aspect] = None

    #     return top_dishes_by_aspect

    def verify_and_fix_all_aggregates(self):
        reviews_ref = self.db.collection("UserSelections")
        aggregates_ref = self.db.collection("Aggregates")

        dishes = set()
        reviews = reviews_ref.stream()
        for review in reviews:
            dish_name = review.to_dict().get("dish_name")
            if dish_name:
                dishes.add(dish_name)

        if not dishes:
            print("⚠️ No dishes found in UserSelections.")
            return

        print(f"🔍 Checking and fixing aggregates for {len(dishes)} dishes...")

        for dish_name in dishes:
            self.verify_and_fix_aggregate(dish_name)

        print("✅ Finished verifying and fixing all aggregates.")

    def verify_and_fix_aggregate(self, dish_name):
        reviews_ref = self.db.collection("UserSelections")
        aggregate_ref = self.db.collection("Aggregates").document(dish_name)

        dish_reviews = reviews_ref.where("dish_name", "==", dish_name).stream()
        
        total_reviews = 0
        taste_sums = {taste: 0.0 for taste in self.TASTE_CATEGORIES}

        for review in dish_reviews:
            review_data = review.to_dict()
            total_reviews += 1
            for taste in self.TASTE_CATEGORIES:
                taste_sums[taste] += review_data.get(taste, 0)

        if total_reviews == 0:
            print(f"⚠️ No existing reviews for {dish_name}. Removing invalid aggregate.")
            aggregate_ref.delete()
            return False

        correct_aggregate = {"total_reviews": total_reviews}
        for taste in self.TASTE_CATEGORIES:
            correct_aggregate[taste] = taste_sums[taste] / total_reviews

        doc = aggregate_ref.get()
        if doc.exists:
            existing_aggregate = doc.to_dict()

            is_correct = True
            for key, correct_value in correct_aggregate.items():
                if abs(existing_aggregate.get(key, 0) - correct_value) > 0.001:
                    is_correct = False
                    break  # If any value is wrong, we must fix it

            if is_correct:
                print(f"✅ Aggregate for {dish_name} is correct. No changes needed.")
                return True
            else:
                print(f"⚠️ Aggregate for {dish_name} is incorrect. Fixing it now...")
                aggregate_ref.set(correct_aggregate)
                print(f"✅ Fixed aggregate for {dish_name}.")
                return True
        else:
            print(f"⚠️ No aggregate found for {dish_name}. Creating a new one.")
            aggregate_ref.set(correct_aggregate)
            print(f"✅ Aggregate created for {dish_name}.")
            return True
    
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
