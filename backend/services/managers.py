from firebase_admin import firestore
from backend.models.favoriteModel import FavoriteManager
from backend.models.noteModel import NoteManager
from backend.models.userModel import UserManager
from backend.models.dishModel import DishManager
from backend.models.ingredientModel import IngredientManager
from backend.models.dietaryModel import DietaryManager
from backend.models.tasteModel import TasteManager
from backend.models.aggregateModel import AggregateManager
from backend.models.nutrientModel import NutrientManager
from backend.models.priceModel import PriceManager

user_manager = UserManager()
dish_manager = DishManager(csv_file='data/dishes.csv')
ingredient_manager = IngredientManager(firestore)
dietary_manager = DietaryManager(firestore)
taste_manager = TasteManager(firestore)
aggregate_manager = AggregateManager()
nutrient_manager = NutrientManager(firestore)
favorite_manager = FavoriteManager(firestore)
price_manager = PriceManager('data/locations.csv', firestore)
note_manager = NoteManager(firestore)
