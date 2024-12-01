from flask import flash, redirect

class Requests:
    def __init__(self, name, description, adjectives):
        self.name = name
        self.description = description
        self.adjectives = adjectives.split(';') if isinstance(adjectives, str) else adjectives

class RequestsManager:
    def __init__(self, db, firestore):
        self.requests_ref = db.collection('Requests')
        self.firestore = firestore

    def add_food_request(self, food_name, description, adjectives):
        """
        Store a user food request in the Firestore 'Requests' collection.
        
        :param food_request: An instance of the FoodRequest class.
        """
        try:
            request_data = {
                'food_name': food_name,
                'description': description,
                'adjectives': adjectives,
                'timestamp': self.firestore.SERVER_TIMESTAMP
            }
            
            self.requests_ref.add(request_data)
            
            print(f"Request for '{food_name}' added successfully!")
            return {"success": True, "message": f"Request for '{food_name}' added successfully!"}
        except Exception as e:
            print(f"Error adding request: {e}")
            return {"success": False, "error": str(e)}
    
    def get_food_request(self, user):

        if not user.get('admin', False):
            return "Access Denied", 403

        requests = []
        for req in self.requests_ref.stream():
            req_data = req.to_dict()
            req_data['id'] = req.id
            requests.append(req_data)

        return requests
    
    def delete_request(self, request_id):
        if not request_id:
            flash('Invalid request ID.', 'error')
            return redirect('/admin')

        # Delete the request from Firestore
        self.requests_ref.document(request_id).delete()
        flash('Request deleted successfully!', 'success')