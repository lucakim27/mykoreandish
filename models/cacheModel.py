import logging
from firebase_admin import firestore
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, db: firestore.Client):
        self.db = db
        self.taste_cache: List[Dict] = []
        logger.info("CacheManager initialized")
        self._load_dishes()  # Load data at startup
        self._setup_listener()  # Set up real-time updates

    def _load_dishes(self) -> None:
        """Loads dishes once at startup and calculates the average spiciness."""
        try:
            taste_ref = self.db.collection("UserSelections").stream()
            tastes = [doc.to_dict() for doc in taste_ref]

            dish_taste = {}
            for taste in tastes:
                dish_name = taste.get("dish_name", 0)
                spiciness = taste.get("spiciness", 0)
                temperature = taste.get("temperature", 0)
                healthiness = taste.get("healthiness", 0)
                rating = taste.get("rating", 0)
                sourness = taste.get("sourness", 0)
                sweetness = taste.get("sweetness", 0)
                texture = taste.get("texture", 0)

                if dish_name in dish_taste:
                    dish_taste[dish_name]['spiciness'].append(spiciness)
                    dish_taste[dish_name]['temperature'].append(temperature)
                    dish_taste[dish_name]['healthiness'].append(healthiness)
                    dish_taste[dish_name]['rating'].append(rating)
                    dish_taste[dish_name]['sourness'].append(sourness)
                    dish_taste[dish_name]['sweetness'].append(sweetness)
                    dish_taste[dish_name]['texture'].append(texture)
                else:
                    dish_taste[dish_name] = {}
                    dish_taste[dish_name]['spiciness'] = [spiciness]
                    dish_taste[dish_name]['temperature'] = [temperature]
                    dish_taste[dish_name]['healthiness'] = [healthiness]
                    dish_taste[dish_name]['rating'] = [rating]
                    dish_taste[dish_name]['sourness'] = [sourness]
                    dish_taste[dish_name]['sweetness'] = [sweetness]
                    dish_taste[dish_name]['texture'] = [texture]

            self.taste_cache = [
                {
                    "dish_name": dish_name,
                    "average_spiciness": round(sum(dish_aspects['spiciness']) / len(dish_aspects['spiciness'])),
                    "average_temperature": round(sum(dish_aspects['temperature']) / len(dish_aspects['temperature'])),
                    "average_healthiness": round(sum(dish_aspects['healthiness']) / len(dish_aspects['healthiness'])),
                    "average_rating": round(sum(dish_aspects['rating']) / len(dish_aspects['rating'])),
                    "average_sourness": round(sum(dish_aspects['sourness']) / len(dish_aspects['sourness'])),
                    "average_sweetness": round(sum(dish_aspects['sweetness']) / len(dish_aspects['sweetness'])),
                    "average_texture": round(sum(dish_aspects['texture']) / len(dish_aspects['texture']))
                }
                for dish_name, dish_aspects in dish_taste.items()
            ]

            logger.info("Cache has been initialised.")

        except Exception as e:
            logger.error(f"Error loading dishes: {e}")

    def _setup_listener(self) -> None:
        """Sets up Firestore real-time listener to update cache on changes."""
        def on_snapshot(col_snapshot, changes, read_time):
            self._load_dishes()
            logger.info("Cache has been updated.")
        try:
            self.db.collection("UserSelections").on_snapshot(on_snapshot)
        except Exception as e:
            logger.error(f"Error setting up listener: {e}")

    def get_cached_taste(self) -> List[Dict]:
        """Returns cached dishes."""
        return self.taste_cache

    def get_dishes_by_spiciness(self, spiciness: int) -> List[Dict]:
        """Returns dishes with the specified spiciness."""
        result = []
        for dish in self.taste_cache:
            if int(dish['average_spiciness']) == int(spiciness):
                result.append(dish['dish_name'])
        
        return result
    
    def get_dishes_by_temperature(self, temperature: int) -> List[Dict]:
        """Returns dishes with the specified temperature."""
        result = []
        for dish in self.taste_cache:
            if int(dish['average_temperature']) == int(temperature):
                result.append(dish['dish_name'])
        
        return result

    def get_dishes_by_healthiness(self, healthiness: int) -> List[Dict]:
        """Returns dishes with the specified healthiness."""
        result = []
        for dish in self.taste_cache:
            if int(dish['average_healthiness']) == int(healthiness):
                result.append(dish['dish_name'])
        
        return result

    def get_dishes_by_rating(self, rating: int) -> List[Dict]:
        """Returns dishes with the specified rating."""
        result = []
        for dish in self.taste_cache:
            if int(dish['average_rating']) == int(rating):
                result.append(dish['dish_name'])
        
        return result

    def get_dishes_by_sourness(self, sourness: int) -> List[Dict]:
        """Returns dishes with the specified sourness."""
        result = []
        for dish in self.taste_cache:
            if int(dish['average_sourness']) == int(sourness):
                result.append(dish['dish_name'])
        
        return result

    def get_dishes_by_sweetness(self, sweetness: int) -> List[Dict]:
        """Returns dishes with the specified sweetness."""
        result = []
        for dish in self.taste_cache:
            if int(dish['average_sweetness']) == int(sweetness):
                result.append(dish['dish_name'])
        
        return result

    def get_dishes_by_texture(self, texture: int) -> List[Dict]:
        """Returns dishes with the specified texture."""
        result = []
        for dish in self.taste_cache:
            if int(dish['average_texture']) == int(texture):
                result.append(dish['dish_name'])
        
        return result

    def get_top_spicy(self, top_n=3):
        """Returns the top N dishes by spiciness."""
        top_spicy = sorted(self.taste_cache, key=lambda x: x["average_spiciness"], reverse=True)[:top_n]
        return top_spicy
    
    def get_top_sweet(self, top_n=3):
        """Returns the top N dishes by sweetness."""
        top_sweet = sorted(self.taste_cache, key=lambda x: x["average_sweetness"], reverse=True)[:top_n]
        return top_sweet

    def get_top_sour(self, top_n=3):
        """Returns the top N dishes by sourness."""
        top_sour = sorted(self.taste_cache, key=lambda x: x["average_sourness"], reverse=True)[:top_n]
        return top_sour
    
    def get_top_healthy(self, top_n=3):
        """Returns the top N dishes by healthiness."""
        top_healthy = sorted(self.taste_cache, key=lambda x: x["average_healthiness"], reverse=True)[:top_n]
        return top_healthy
    
    def get_top_temperature(self, top_n=3):
        """Returns the top N dishes by temperature."""
        top_temperature = sorted(self.taste_cache, key=lambda x: x["average_temperature"], reverse=True)[:top_n]
        return top_temperature
    
    def get_top_rating(self, top_n=3):
        """Returns the top N dishes by rating."""
        top_rating = sorted(self.taste_cache, key=lambda x: x["average_rating"], reverse=True)[:top_n]
        return top_rating
    
    def get_top_texture(self, top_n=3):
        """Returns the top N dishes by texture."""
        top_texture = sorted(self.taste_cache, key=lambda x: x["average_texture"], reverse=True)[:top_n]
        return top_texture