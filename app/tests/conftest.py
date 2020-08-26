"""
Pytest Fixtures
"""

import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    """
    Test client fixture.
    """
    client = TestClient(app)
    yield client  # testing happens here


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
