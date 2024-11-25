from flask import redirect, session, flash, url_for
from functools import wraps

# Store user data in Firebase Firestore
def store_google_user(db, google_user_data):
    google_id = google_user_data.get('id')
    name = google_user_data.get('name')
    email = google_user_data.get('email')

    try:
        # Check if the user already exists in Firestore
        user_ref = db.collection('Users').document(google_id)
        user_doc = user_ref.get()

        if user_doc.exists:
            # If the user exists, update their data
            user_ref.update({
                'name': name,
                'email': email,
                'google_id': google_id
            })
        else:
            # If the user doesn't exist, add new user
            user_ref.set({
                'name': name,
                'email': email,
                'google_id': google_id
            })
    except Exception as e:
        print(f"Error storing user: {e}")

# Logout user
def logout_user():
    session.pop('google_id', None)
    flash('You have been logged out.', 'info')

def get_username(db):
    if session.get('google_id'):
        # Reference to the 'Users' collection
        users_ref = db.collection('Users')
        
        # Query to get the user by google_id from the session
        user_ref = users_ref.where('google_id', '==', session.get('google_id'))
        user_docs = user_ref.get()  # Fetch the documents matching the query
        
        # Assuming only one user document matches, get the first document
        user = user_docs[0]  # Fetch the first matching document
        
        # Return the 'username' field from the document
        return user.to_dict().get('name')


# Get logged in user
def get_logged_in_user():
    return session.get('google_id')

# Delete history function (if needed)
def delete_history_function(db, history_id):
    try:
        history_ref = db.collection('UserSelections').document(history_id)
        history_ref.delete()
        flash('History item deleted successfully.', 'success')
        return True
    except Exception as e:
        flash('An error occurred while deleting the history item.', 'error')
        print(f"Error: {e}")
        return False

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'google_id' not in session:
            return redirect(url_for('google.login'))
        return f(*args, **kwargs)
    return decorated_function

# Rate dish function
def rate_dish_function(db, history_id, rating):
    if not history_id or not rating:
        flash('Invalid input for rating.', 'error')
        return False

    try:
        history_ref = db.collection('UserSelections').document(history_id)
        history_ref.update({
            'rating': int(rating)
        })
        flash('Rating saved successfully!', 'success')
        return True
    except Exception as e:
        flash(f'Error saving rating: {e}', 'error')
        return False
    
def get_dish_statistics(db):
    average_ratings = {}
    selection_counts = {}

    try:
        # Dictionary to hold dish ratings
        dish_ratings = {}
        
        # Retrieve ratings from the 'UserSelections' collection
        ratings_ref = db.collection('UserSelections')
        ratings = ratings_ref.stream()

        # Process ratings and selections in a single pass
        for rating in ratings:
            rating_data = rating.to_dict()
            dish_name = rating_data.get('dish_name')
            rating_value = rating_data.get('rating')

            if dish_name:
                # Count the selections for each dish (only from UserSelections)
                if dish_name not in selection_counts:
                    selection_counts[dish_name] = 0
                selection_counts[dish_name] += 1  # Increase the count for each selection

                # Handle the ratings for dishes (only consider non-None ratings)
                if rating_value is not None:
                    if dish_name not in dish_ratings:
                        dish_ratings[dish_name] = {'total': 0, 'count': 0}
                    dish_ratings[dish_name]['total'] += rating_value
                    dish_ratings[dish_name]['count'] += 1

        # Calculate average ratings for each dish
        for dish_name, data in dish_ratings.items():
            average_rating = data['total'] / data['count']
            if average_rating > 0:  # Only include dishes with non-zero average ratings
                average_ratings[dish_name] = average_rating

        # Ensure every dish from UserSelections is included in selection_counts, even if no rating
        for dish_name in selection_counts:
            if dish_name not in average_ratings:
                average_ratings[dish_name] = 0  # No ratings but included in selections

    except Exception as e:
        print(f"Error fetching dish statistics: {e}")

    # Sorting the results
    average_ratings = dict(sorted(average_ratings.items(), key=lambda item: item[1], reverse=True))
    selection_counts = dict(sorted(selection_counts.items(), key=lambda item: item[1], reverse=True))

    return average_ratings, selection_counts

