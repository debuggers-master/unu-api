"""
Pytest Fixtures
"""

import pytest
from starlette.testclient import TestClient

from app.main import app
from auth.services import create_access_token


@pytest.fixture(scope="module")
def client():
    """
    Test client fixture.
    """
    client = TestClient(app)
    yield client


@pytest.fixture()
def get_token():
    """
    Return a function to generate a token
    """
    def _acces_toke(email):
        token = create_access_token({"sub": email})
        return token
    return _acces_toke


@pytest.fixture()
def test_user():
    """
    Return the test user
    """
    return {
        "name": "Stan",
        "lastName": "Lee",
        "email": "stan@gmail.com",
        "password": "user123",
        "userId": "aabe7a81-2f32-43ff-a767-c13a776fbf4c"
    }


@pytest.fixture()
def dummy_user():
    """
    Return the test user dummy for all operations
    """
    return {
        "name": "Steve",
        "lastName": "Jobs",
        "email": "jobs@apple.com",
        "password": "user123",
        "userId": "08d6a082-20ee-4aa6-9f02-64a89086e990"
    }


@pytest.fixture()
def test_organization():
    """
    Return the test organization
    """
    return {
        "organizationLogo": "",
        "organizationName": "Testing",
        "organizationId": "b86e537e-48c7-483c-815f-2665d5618f38",
        "organizationUrl": "testing",
        "events": []
    }


@pytest.fixture()
def auth_response():
    """
    Return a custom login response.
    """
    def _response(email, name, lastname):
        return {
            "access_token": "",
            "token_type": "Bearer",
            "user": {
                "email": f"{email}",
                "firstName": f"{name}",
                "lastName": f"{lastname}",
                "userId": "",
                "organizations": [],
                "myEvents": [],
                "collaborations": []
            }
        }
    return _response
