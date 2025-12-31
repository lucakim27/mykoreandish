from firebase_admin import firestore
from src.models.favoriteModel import FavoriteManager
from src.models.noteModel import NoteManager
from src.models.userModel import UserManager
from src.models.dishModel import DishManager
from src.models.ingredientModel import IngredientManager
from src.models.dietaryModel import DietaryManager
from src.models.tasteModel import TasteManager
from src.models.aggregateModel import AggregateManager
from src.models.nutrientModel import NutrientManager
from src.models.priceModel import PriceManager

user_manager = UserManager()
dish_manager = DishManager(csv_file='src/data/dishes.csv')
ingredient_manager = IngredientManager(firestore)
dietary_manager = DietaryManager(firestore)
taste_manager = TasteManager(firestore)
aggregate_manager = AggregateManager()
nutrient_manager = NutrientManager(firestore)
favorite_manager = FavoriteManager(firestore)
price_manager = PriceManager('src/data/locations.csv', firestore)
note_manager = NoteManager(firestore)
