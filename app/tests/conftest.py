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
    return {"name": "Stan", "lastName": "Lee", "email": "stan@gmail.com"}


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
