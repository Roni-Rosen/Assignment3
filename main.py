from flask import Flask
import dishes
import meals

app = Flask(__name__)


# DISHES ROUTES
@app.route('/dishes', methods=['POST'])
def call_create_dish():
    return dishes.create_dish()


@app.route('/dishes', methods=['GET'])
def call_get_dishes():
    return dishes.get_dishes()


@app.route('/dishes', methods=['DELETE'])
def call_delete_dishes():
    return dishes.delete_dishes()


@app.route('/dishes/<dish_id_or_name>', methods=['DELETE'])
def call_delete_dish(dish_id_or_name):
    return dishes.delete_dish(dish_id_or_name, meals.meals)


@app.route('/dishes/<dish_id_or_name>', methods=['GET'])
def call_get_dish(dish_id_or_name):
    return dishes.get_dish(dish_id_or_name)


# MEALS ROUTES
@app.route('/meals', methods=['GET'])
def call_get_meals():
    return meals.get_meals()


@app.route('/meals', methods=['POST'])
def call_create_meal():
    return meals.create_meal()


@app.route('/meals/<int:meal_id>', methods=['GET'])
def call_get_meal_by_id(meal_id):
    return meals.get_meal_by_id(meal_id)


@app.route('/meals/<int:meal_id>', methods=['DELETE'])
def call_delete_meal_by_id(meal_id):
    return meals.delete_meal_by_id(meal_id)


@app.route('/meals/<string:meal_name>', methods=['GET'])
def call_get_meal_by_name(meal_name):
    return meals.get_meal_by_name(meal_name)


@app.route('/meals/<string:meal_name>', methods=['DELETE'])
def call_delete_meal_by_name(meal_name):
    return meals.delete_meal_by_name(meal_name)


@app.route('/meals/<int:meal_id>', methods=['PUT'])
def call_update_meal_by_id(meal_id):
    return meals.update_meal_by_id(meal_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
