from flask import jsonify, request
import requests

dishes = []
dishes_dict = {}
names_dict = {}
dish_id_counter = 1

MY_API_KEY = 'FtxdYthk+dBazFA94J8aLQ==RLidx1IzcrA5wkUT'


# function to add a dish to the dictionaries
def add_dish_to_dicts(dish):
    dishes_dict[dish['ID']] = dish
    names_dict[dish['name']] = dish['ID']


# function to remove a dish from the dictionaries
def remove_dish_from_dicts(dish_id):
    dish = dishes_dict[dish_id]
    name = dish['name']
    del dishes_dict[dish_id]
    del names_dict[name]


def create_dish():
    global dish_id_counter

    # 0 means that request content-type is not application/json. Status code 415 (Unsupported Media Type)
    if not request.content_type == 'application/json':
        return '0', 415

    try:
        data = request.get_json()
    except:
        return '0', 415

    # -1 means that 'name' parameter was not specified in the message body. Status code 422 (Unprocessable Content)
    if not data or 'name' not in data:
        return '-1', 422

    name = data['name']
    id = None

    # Check if dish of given name already exists
    # -2 means that dish of given name already exists. Status code 422 (Unprocessable Content)
    for dish in names_dict:
        if dish == name:
            return '-2', 422

    # Query nutrition API to get dish information

    query = name
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
    response = requests.get(api_url, headers={'X-Api-Key': MY_API_KEY})

    # -3 means that api.api-ninjas.com/v1/nutrition does not recognize this dish name. Status code 422
    # (Unprocessable Content)
    if response.status_code == 404 or not response.json():
        return '-3', 422
    # -4 means that api.api-ninjas.com/v1/nutrition was not reachable. Status code 504 (Gateway Timeout)
    elif response.status_code >= 500:
        return '-4', 504

    dish_info = response.json()

    # Check if we have multiple dishes in the response
    if len(dish_info) > 1:
        # Combine the values for 'calories', 'sodium', 'sugar', and 'serving_size_g' from all components
        combined_info = {
            'cal': sum(d['calories'] for d in dish_info),
            'sodium': sum(d['sodium_mg'] for d in dish_info),
            'sugar': sum(d['sugar_g'] for d in dish_info),
            'size': sum(d['serving_size_g'] for d in dish_info)
        }
    else:
        # Use the information from the first component
        combined_info = {
            'cal': dish_info[0]['calories'],
            'sodium': dish_info[0]['sodium_mg'],
            'sugar': dish_info[0]['sugar_g'],
            'size': dish_info[0]['serving_size_g']
        }

    id = dish_id_counter
    dish_id_counter += 1

    # Create dish object with retrieved information
    dish = {
        'ID': id,
        'name': name,
        'cal': combined_info['cal'],
        'size': combined_info['size'],
        'sodium': combined_info['sodium'],
        'sugar': combined_info['sugar']
    }

    dishes.append(dish)
    add_dish_to_dicts(dish)
    return str(id), 201


# GET request to return all dishes indexed by ID
def get_dishes():
    return jsonify(dishes_dict)


# DELETE method for /dishes
def delete_dishes():
    return 'This method is not allowed for the requested URL', 405


# DELETE method for /dishes/{ID} and /dishes/{name}
def delete_dish(dish_id_or_name, meals):
    # Check if the dish exists
    if dish_id_or_name.isdigit():
        # Get the dish by ID
        if int(dish_id_or_name) in dishes_dict:
            dish_id = int(dish_id_or_name)
            del dishes_dict[dish_id]
            del names_dict[dishes[dish_id - 1]['name']]
        else:
            return '-5', 404

    else:
        # Get the dish by name
        if dish_id_or_name in names_dict:
            dish_name = dish_id_or_name
            dish_id = names_dict[dish_name]
            del names_dict[dish_name]
            del dishes_dict[dish_id]
        else:
            return '-5', 404

    # Iterate through all the meals
    for meal in meals.values():
        # Check if the deleted dish is an appetizer
        if meal['appetizer'] == dish_id:
            meal['appetizer'] = None
        # Check if the deleted dish is a main
        if meal['main'] == dish_id:
            meal['main'] = None
        # Check if the deleted dish is a dessert
        if meal['dessert'] == dish_id:
            meal['dessert'] = None

    # Return the ID of the deleted dish
    return str(dish_id), 200


# GET method for /dishes/{ID} and /dishes/{name}
def get_dish(dish_id_or_name):
    if dish_id_or_name.isdigit():
        # Get the dish by ID
        if int(dish_id_or_name) in dishes_dict:
            dish_id = int(dish_id_or_name)
            dish_name = dishes_dict[dish_id]['name']
        else:
            return '-5', 404

    else:
        # Get the dish by name
        if dish_id_or_name in names_dict:
            dish_name = dish_id_or_name
            dish_id = names_dict[dish_name]
        else:
            return '-5', 404

    # Return the dish information
    return jsonify({
        'ID': dish_id,
        'name': dish_name,
        'cal': dishes[dish_id - 1]['cal'],
        'sodium': dishes[dish_id - 1]['sodium'],
        'sugar': dishes[dish_id - 1]['sugar']
    }), 200
