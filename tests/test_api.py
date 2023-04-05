import logging
import os
from dotenv import load_dotenv
from pytest_voluptuous import S
from schema.schema import \
    user_register_successful_schema, \
    user_create_successful_schema, \
    user_update_successful_schema, \
    user_register_unsuccessful_schema

load_dotenv()
API_URL_REQRES = os.getenv("API_URL_REQRES")


def test_create_user_successful(reqres):
    response = reqres.post(
        url="/users",
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


def test_put_update_user_successful(reqres):
    response = reqres.put(
        url="/users/2",
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


def test_patch_update_user_successful(reqres):
    response = reqres.patch(
        url="/users/2",
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


def test_delete_user_successful(reqres):
    response = reqres.delete(
        url="/users/2"
    )

    assert response.status_code == 204


def test_register_successful(reqres):
    response = reqres.post(
        url='/register',
        json={
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        }
    )
    logging.info(response.json())

    assert response.status_code == 200
    assert response.json() == S(user_register_successful_schema)
    assert response.json()["id"] == 4 and response.json()["token"] == "QpwL5tke4Pnpja7X4"


def test_register_unsuccessful_no_password(reqres):
    response = reqres.post(
        url='/register',
        json={
            "email": "eve.holt@reqres.in",
        }
    )
    logging.info(response.json())

    assert response.status_code == 400
    assert response.json() == S(user_register_unsuccessful_schema)
    assert response.json()["error"] == "Missing password"


def test_register_unsuccessful_no_email(reqres):
    response = reqres.post(
        url='/register',
        json={
            "password": "eve.holt@reqres.in",
        }
    )
    logging.info(response.json())

    assert response.status_code == 400
    assert response.json() == S(user_register_unsuccessful_schema)
    assert response.json()["error"] == "Missing email or username"
