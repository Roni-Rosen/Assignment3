import requests
import json

url = "http://localhost:8000/dishes"

with open('query.txt', 'r') as query_file, open('response.txt', 'w') as response_file:
    for food_item in query_file:
        food_item = food_item.strip()

        # send a POST request to create the food item
        data = {'name': food_item}
        response = requests.post(url, json=data)

        if response.status_code == 201:
            dish_id = response.text

            # send a GET request to retrieve the food item
            response = requests.get(f"{url}/{dish_id}")

            if response.status_code == 200:
                data = json.loads(response.text)

                # write the response to the response.txt file
                response_file.write(
                    f"{food_item} contains {data['cal']} calories, {data['sodium']} mgs of sodium, and {data['sugar']} grams of sugar\n"
                )
