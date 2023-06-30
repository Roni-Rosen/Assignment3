from flask import jsonify, request
from dishes import dishes, dishes_dict

# Define the initial meals dictionary
meals = {}
meal_id_counter = 1


# Define a function to compute the total calories, sodium, and sugar for a meal
def compute_meal_nutrition(meal):
    appetizer = dishes[meal["appetizer"] - 1]
    main_dish = dishes[meal["main"] - 1]
    dessert = dishes[meal["dessert"] - 1]
    total_calories = appetizer["cal"] + main_dish["cal"] + dessert["cal"]
    total_sodium = appetizer["sodium"] + main_dish["sodium"] + dessert["sodium"]
    total_sugar = appetizer["sugar"] + main_dish["sugar"] + dessert["sugar"]
    meal["cal"] = total_calories
    meal["sodium"] = total_sodium
    meal["sugar"] = total_sugar


# Define the endpoint to retrieve all meals
def get_meals():
    return jsonify(meals)


# Define the endpoint to create a new meal
def create_meal():
    global meal_id_counter

    if not request.content_type == 'application/json':
        return '0', 415

    data = request.get_json()

    # Check if all the required parameters are present
    if not all(param in data for param in ['name', 'appetizer', 'main', 'dessert']):
        # -1 means that one of the required parameters was not given or not specified correctly. Status code 422
        # (Unprocessable Entity)
        return '-1', 422

    # Check if a meal with the same name already exists
    if any(meal['name'] == data['name'] for meal in meals.values()):
        # -2 means that a meal of the given name already exists. Status code 422 (Unprocessable Entity)
        return '-2', 422

    # Check if the appetizer, main, and dessert dishes exist
    if any(dish_id not in dishes_dict.keys() for dish_id in [data['appetizer'], data['main'], data['dessert']]):
        # -6 means that one of the sent dish IDs (appetizer, main, dessert) does not exist. Status code 422
        # (Unprocessable Entity)
        return '-6', 422

    # Create the new meal
    meal_id = meal_id_counter
    meal_id_counter += 1

    data['ID'] = meal_id
    compute_meal_nutrition(data)
    meals[meal_id] = data

    return str(meal_id), 201


# Define the endpoint to get a specific meal by ID
def get_meal_by_id(meal_id):
    meal = next((meal for meal in meals.values() if meal['ID'] == meal_id), None)
    if meal is None:
        return '-5', 404
    return jsonify(meal)


# Define the endpoint to delete a specific meal by ID
def delete_meal_by_id(meal_id):
    meal = next((meal for meal in meals.values() if meal['ID'] == meal_id), None)
    if meal is None:
        return '-5', 404
    del meals[meal['ID']]
    return str(meal['ID']), 200


# Define the endpoint to get a specific meal by name
def get_meal_by_name(meal_name):
    meal = next((meal for meal in meals.values() if meal['name'] == meal_name), None)
    if meal is None:
        return '-5', 404
    return jsonify(meal)


# Define the endpoint to delete a specific meal by name
def delete_meal_by_name(meal_name):
    meal = next((meal for meal in meals.values() if meal['name'] == meal_name), None)
    if meal is None:
        return '-5', 404
    del meals[meal['ID']]
    return str(meal['ID']), 200


# Define the endpoint to delete a specific meal by id
def update_meal_by_id(meal_id):
    meal = next((meal for meal in meals.values() if meal['ID'] == meal_id), None)
    if meal is None:
        return '-5', 404

    if not request.content_type == 'application/json':
        return '0', 415

    data = request.get_json()

    # Check if all the required parameters are present
    if not all(param in data for param in ['name', 'appetizer', 'main', 'dessert']):
        # -1 means that one of the required parameters was not given or not specified correctly. Status code 422
        # (Unprocessable Entity)
        return '-1', 422

    # Check if a meal with the same name already exists
    if any(m['name'] == data['name'] and m['ID'] != meal_id for m in meals.values()):
        # -2 means that a meal of the given name already exists. Status code 422 (Unprocessable Entity)
        return '-2', 422

    # Check if the appetizer, main, and dessert dishes exist
    if any(dish_id not in dishes_dict.keys() for dish_id in [data['appetizer'], data['main'], data['dessert']]):
        # -6 means that one of the sent dish IDs (appetizer, main, dessert) does not exist. Status code 422
        # (Unprocessable Entity)
        return '-6', 422

    # Update the existing meal with the new data
    data['ID'] = meal_id
    compute_meal_nutrition(data)
    meals[meal_id] = data

    return str(meal_id), 200
