from typing import List, Dict, Any
from flask import flash
from google.cloud import firestore

class Requests:
    def __init__(self, name: str, description: str, timestamp: Any):
        self.name = name
        self.description = description
        self.timestamp = timestamp

class RequestsManager:
    def __init__(self, db: firestore.Client, firestore_module: Any):
        self.requests_ref = db.collection('Requests')
        self.firestore = firestore_module

    def add_food_request(self, name, description) -> Dict[str, Any]:
        try:
            request_instance = Requests(name, description, self.firestore.SERVER_TIMESTAMP)
            
            request_data = {
                'food_name': request_instance.name,
                'description': request_instance.description,
                'timestamp': request_instance.timestamp
            }
            
            self.requests_ref.add(request_data)
            flash(f"Request for '{request_instance.name}' added successfully!")
        except firestore.exceptions.FirestoreError as e:
            flash(f'Error adding request: {e}', 'error')
            print(f"Error: {e}")
    
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
            self.requests_ref.document(request_id).delete()
            return {"success": True, "message": "Request deleted successfully!"}
        except firestore.exceptions.FirestoreError as e:
            return {"success": False, "error": str(e)}