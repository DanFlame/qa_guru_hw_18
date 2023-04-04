import logging
import requests
from pytest_voluptuous import S
from requests import Response
from schema.schema import \
    user_register_successful_schema, \
    user_create_successful_schema, \
    user_update_successful_schema, \
    user_register_unsuccessful_schema


def test_create_user_successful():
    response: Response = requests.post(
        url="https://reqres.in/api/users",
        json={
            "name": "Daniel",
            "job": "Undertaker"
        }
    )
    logging.info(response.json())

    assert response.status_code == 201
    assert response.json() == S(user_create_successful_schema)
    assert response.json()["name"] == "Daniel"
    assert response.json()["job"] == "Undertaker"
    assert response.json()["id"] is not None
    assert response.json()["createdAt"] is not None


def test_put_update_user_successful():
    response: Response = requests.put(
        url="https://reqres.in/api/users/2",
        json={
            "name": "Daniel",
            "job": "Corpse"
        }
    )
    logging.info(response.json())

    assert response.status_code == 200
    assert response.json()["name"] == "Daniel"
    assert response.json()["job"] == "Corpse"
    assert response.json()["updatedAt"] is not None
    assert response.json() == S(user_update_successful_schema)


def test_patch_update_user_successful():
    response: Response = requests.patch(
        url="https://reqres.in/api/users/2",
        json={
            "name": "Daniel",
            "job": "Corpse"
        }
    )
    logging.info(response.json())

    assert response.status_code == 200
    assert response.json()["name"] == "Daniel"
    assert response.json()["job"] == "Corpse"
    assert response.json()["updatedAt"] is not None
    assert response.json() == S(user_update_successful_schema)


def test_delete_user_successful():
    response: Response = requests.delete(
        url="https://reqres.in/api/users/2"
    )

    assert response.status_code == 204


def test_register_successful():
    response: Response = requests.post(
        url='https://reqres.in/api/register',
        json={
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        }
    )
    logging.info(response.json())

    assert response.status_code == 200
    assert response.json() == S(user_register_successful_schema)
    assert response.json()["id"] == 4 and response.json()["token"] == "QpwL5tke4Pnpja7X4"


def test_register_unsuccessful_no_password():
    response: Response = requests.post(
        url='https://reqres.in/api/register',
        json={
            "email": "eve.holt@reqres.in",
        }
    )
    logging.info(response.json())

    assert response.status_code == 400
    assert response.json() == S(user_register_unsuccessful_schema)
    assert response.json()["error"] == "Missing password"


def test_register_unsuccessful_no_email():
    response: Response = requests.post(
        url='https://reqres.in/api/register',
        json={
            "password": "eve.holt@reqres.in",
        }
    )
    logging.info(response.json())

    assert response.status_code == 400
    assert response.json() == S(user_register_unsuccessful_schema)
    assert response.json()["error"] == "Missing email or username"
