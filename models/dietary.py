
class Dietary:
    def __init__(self, dish_name, dietary):
        self.dish_name = dish_name
        self.dietary = dietary

class DietaryManager:
    def __init__(self, db, firestore):
        # self.dishes_ref = db.collection('Dishes')
        self.users_ref = db.collection('Users')
        # self.prices_ref = db.collection('Prices')
        self.dietaries_ref = db.collection('Dietaries')
        self.firestore = firestore
    
    def addDietary(self, dish_name, google_id, dietary):
        user_ref = self.users_ref.where('google_id', '==', google_id)
        user = user_ref.get()

        if not user:
            raise ValueError("User does not exist.")

        self.dietaries_ref.add({
            'google_id': google_id,
            'dish_name': dish_name,
            'dietary': dietary,
            'timestamp': self.firestore.SERVER_TIMESTAMP
        })
    
    def getDietary(self, dish_name):
        dietary_ref = self.dietaries_ref.where('dish_name', '==', dish_name)
        dietaries = dietary_ref.stream()
        
        dietaries_list = [{
                'dietary': dietary.to_dict().get('dietary')
            } for dietary in dietaries]
    
        if not dietaries_list:
            return []

        dietary_count = {
            'Vegetarian': 0,
            'Halal': 0,
            'Vegan': 0,
            'Seafood': 0
        }

        for dietary in dietaries_list:
            if dietary['dietary'] in dietary_count:
                dietary_count[dietary['dietary']] += 1

        return dietary_count