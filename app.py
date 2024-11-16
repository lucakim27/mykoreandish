from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/recommendation', methods=['POST'])
def recommendation():
    # Get form values
    dietary_restrictions = request.form.get('dietary_restrictions', '')
    cuisine_preferences = request.form.get('cuisine_preference', '')
    # Add other form fields here...

    # Process the values to make a recommendation
    recommendation = make_recommendation(
        dietary_restrictions=dietary_restrictions,
        cuisine_preferences=cuisine_preferences,
        # Pass other form values...
    )

    # Render the recommendation to the user
    return render_template('recommendation.html', recommendation=recommendation)

def make_recommendation(dietary_restrictions, cuisine_preferences):
    print(dietary_restrictions, cuisine_preferences)
    # Replace this with your recommendation logic
    if dietary_restrictions == "vegetarian" and cuisine_preferences == "asian":
        return "Try a delicious vegetarian stir-fry!"
    elif cuisine_preferences == "european":
        return "How about some pasta with fresh vegetables?"
    else:
        return "Explore a variety of recipes that match your preferences!"