import pytest
import requests

base_url = "http://localhost:8000"  # Assuming Flask app is running locally on port 8000

# Test data
dish_data = ["orange", "spaghetti", "apple pie"]
meal_data = {"name": "delicious", "appetizer": None, "main": None, "dessert": None}


@pytest.mark.order1
def test_post_dishes():
    ids = []
    for dish_name in dish_data:
        response = requests.post(f"{base_url}/dishes", json={"name": dish_name})
        assert response.status_code == 201
        dish_id = int(response.text)
        ids.append(dish_id)
    assert len(set(ids)) == 3  # all 3 IDs are unique
    meal_data["appetizer"], meal_data["main"], meal_data["dessert"] = ids


@pytest.mark.order2
def test_get_dish_by_id():
    response = requests.get(f"{base_url}/dishes/{meal_data['appetizer']}")
    assert response.status_code == 200
    assert 0.9 <= response.json()["sodium"] <= 1.1


@pytest.mark.order3
def test_get_all_dishes():
    response = requests.get(f"{base_url}/dishes")
    assert response.status_code == 200
    assert len(response.json()) == 3

#
# @pytest.mark.order4
# def test_post_invalid_dish():
#     response = requests.post(f"{base_url}/dishes", json={"name": "blah"})
#     assert response.text == '-3'
#     assert response.status_code in [400, 404, 422]
#
#
# @pytest.mark.order5
# def test_post_dish_with_existing_name():
#     response = requests.post(f"{base_url}/dishes", json={"name": "orange"})
#     assert response.text == '-2'
#     assert response.status_code in [400, 404, 422]
#
#
# @pytest.mark.order6
# def test_post_meal():
#     response = requests.post(f"{base_url}/meals", json=meal_data)
#     assert response.status_code == 201
#     assert int(response.text) > 0
#
#
# @pytest.mark.order7
# def test_get_all_meals():
#     response = requests.get(f"{base_url}/meals")
#     assert response.status_code == 200
#     assert len(response.json()) == 1
#     assert 400 <= response.json()[list(response.json().keys())[0]]["cal"] <= 500
#
#
# @pytest.mark.order8
# def test_post_meal_with_existing_name():
#     response = requests.post(f"{base_url}/meals", json=meal_data)
#     assert response.text == '-2'
#     assert response.status_code in [400, 422]
