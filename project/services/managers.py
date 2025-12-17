from firebase_admin import firestore
from project.models.favoriteModel import FavoriteManager
from project.models.noteModel import NoteManager
from project.models.userModel import UserManager
from project.models.dishModel import DishManager
from project.models.ingredientModel import IngredientManager
from project.models.dietaryModel import DietaryManager
from project.models.tasteModel import TasteManager
from project.models.aggregateModel import AggregateManager
from project.models.nutrientModel import NutrientManager
from project.models.priceModel import PriceManager

user_manager = UserManager()
dish_manager = DishManager(csv_file='csv/dishes.csv')
ingredient_manager = IngredientManager(firestore)
dietary_manager = DietaryManager(firestore)
selection_manager = TasteManager(firestore)
aggregate_manager = AggregateManager()
nutrient_manager = NutrientManager(firestore)
favorite_manager = FavoriteManager(firestore)
price_manager = PriceManager('csv/locations.csv', firestore)
note_manager = NoteManager(firestore)
