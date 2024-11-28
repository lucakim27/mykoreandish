class Requests:
    def __init__(self, name, description, adjectives, requests_ref, firestore):
        self.name = name
        self.description = description
        self.adjectives = adjectives
        self.requests_ref = requests_ref
        self.firestore = firestore

    def add_food_request(self):
        """
        Store a user food request in the Firestore 'Requests' collection.
        
        :param food_name: Name of the requested food.
        :param description: Description of the requested food.
        :param criteria: A dictionary containing the criteria (e.g., dietary restrictions, meal type).
        :param image_url: Optional image URL for the requested food.
        """
        try:
            request_data = {
                'food_name': self.name,
                'description': self.description,
                'adjectives': self.adjectives,
                'timestamp': self.firestore.SERVER_TIMESTAMP
            }
            
            self.requests_ref.add(request_data)
            
            print(f"Request for '{self.name}' added successfully!")
            return {"success": True, "message": f"Request for '{self.name}' added successfully!"}
        except Exception as e:
            print(f"Error adding request: {e}")
            return {"success": False, "error": str(e)}