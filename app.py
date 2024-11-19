from flask import Flask, render_template, request
from utils.filter import DishManager

manager = DishManager('csv/dishes.csv')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/recommendation', methods=['POST'])
def recommendation():
    criteria = {key: value.lower() for key, value in request.form.items()}
    recommendation = manager.make_recommendation(**criteria)
    return render_template('recommendation.html', recommendation=recommendation)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)