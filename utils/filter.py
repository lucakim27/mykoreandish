import csv

def load_data(file_path):
    dishes = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dishes.append(row)
    return dishes

def make_recommendation(**criteria):
    dishes = load_data('csv/dishes.csv')
    filtered_dishes = []

    for dish in dishes:
        match = True
        
        for key, value in criteria.items():

            if value != 'any':
                dish_value = dish.get(key, '').lower()

                dish_values = [item.strip().lower() for item in dish_value.split(';')]

                if value not in dish_values:
                    match = False
                    break

        if match:
            filtered_dishes.append(dish)
            
    if len(filtered_dishes):
        return filtered_dishes
    else:
        [{"Dish Name": "No match found", "Reason": "Try relaxing the filters."}]
