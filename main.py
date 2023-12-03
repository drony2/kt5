import allure
import pytest
from pydantic import BaseModel
import requests


class Pet(BaseModel):
    id: int
    name: str
    status: str


PETSTORE_BASE_URL = "https://petstore.swagger.io/v2"


@pytest.fixture
def generate_data():
    return {"id": 1, "name": "Cat", "status": "NotAvailable"}


def test_create_pet(generate_data):
    response = requests.post(f"{PETSTORE_BASE_URL}/pet", json=generate_data)
    assert response.status_code == 200

    expected_data = generate_data
    actual_data = response.json()

    with allure.step("Verify the created pet using Pydantic"):
        assert_dict_contains_subset(expected_data, actual_data)


def assert_dict_contains_subset(expected, actual):
    for key, value in expected.items():
        assert key in actual, f"Key '{key}' not found in actual dictionary."
        assert actual[key] == value, f"Value mismatch for key '{key}': expected {value}, got {actual[key]}."


@allure.title("Test Get Pet by ID")
def test_get_pet_by_id():
    id = 1
    response = requests.get(f"{PETSTORE_BASE_URL}/pet/{id}")
    assert response.status_code == 200

    with allure.step(f"Verify the pet with ID {id} using Pydantic"):
        pet = Pet(**response.json())
        assert pet.id == id


@allure.title("Test Delete Pet")
def test_delete_pet():
    id = 1
    response = requests.delete(f"{PETSTORE_BASE_URL}/pet/{id}")
    assert response.status_code == 200

    with allure.step(f"Verify the pet with ID {id} is deleted"):
        response = requests.get(f"{PETSTORE_BASE_URL}/pet/{id}")
        assert response.status_code == 404


if __name__ == "__main__":
    pytest.main()
