from typing import List, Dict, Any
from google.cloud import firestore

class Requests:
    def __init__(self, name: str, description: str, adjectives: str):
        self.name = name
        self.description = description
        self.adjectives = adjectives.split(';') if isinstance(adjectives, str) else adjectives

class RequestsManager:
    def __init__(self, db: firestore.Client, firestore_module: Any):
        self.requests_ref = db.collection('Requests')
        self.firestore = firestore_module

    def add_food_request(self, food_name: str, description: str, adjectives: str, spiciness: str, dietary: str, ingredients: str) -> Dict[str, Any]:
        """
        Store a user food request in the Firestore 'Requests' collection.
        
        :param food_name: Name of the food.
        :param description: Description of the food.
        :param adjectives: Adjectives describing the food.
        :param spiciness: Spiciness level of the food.
        :param dietary: Dietary information of the food.
        :param ingredients: Ingredients of the food.
        :return: A dictionary with the success status and message.
        """
        try:
            request_data = {
                'food_name': food_name,
                'description': description,
                'adjectives': adjectives,
                'spiciness': spiciness,
                'dietary': dietary,
                'ingredients': ingredients,
                'timestamp': self.firestore.SERVER_TIMESTAMP
            }
            
            self.requests_ref.add(request_data)
            
            print(f"Request for '{food_name}' added successfully!")
            return {"success": True, "message": f"Request for '{food_name}' added successfully!"}
        except firestore.exceptions.FirestoreError as e:
            print(f"Error adding request: {e}")
            return {"success": False, "error": str(e)}
    
    def get_food_request(self) -> List[Dict[str, Any]]:
        requests = []
        for req in self.requests_ref.stream():
            req_data = req.to_dict()
            req_data['id'] = req.id
            requests.append(req_data)

        return requests
    
    def delete_request(self, request_id: str) -> Dict[str, Any]:
        if not request_id:
            return {"success": False, "message": "Invalid request ID."}

        try:
            # Delete the request from Firestore
            self.requests_ref.document(request_id).delete()
            return {"success": True, "message": "Request deleted successfully!"}
        except firestore.exceptions.FirestoreError as e:
            return {"success": False, "error": str(e)}