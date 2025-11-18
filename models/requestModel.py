from typing import List, Dict, Any
from flask import flash
from google.cloud import firestore

class RequestManager:
    def __init__(self, db: firestore.Client, firestore_module: Any):
        self.requests_ref = db.collection('Requests')
        self.firestore = firestore_module
    
    def add_food_request(self, name, description) -> Dict[str, Any]:
        try:
            request_data = {
                'food_name': name,
                'description': description,
                'timestamp': self.firestore.SERVER_TIMESTAMP
            }
            self.requests_ref.add(request_data)
            flash(f"Request for '{name}' added successfully!", 'success')
        except firestore.exceptions.FirestoreError as e:
            flash(f'Error adding request: {e}', 'error')
    
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