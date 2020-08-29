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
def test_event():
    """
    Return the test event.
    """
    return {
        "name": "Comic Con 2020",
        "shortDescription": "Marvelous",
        "description": "Marveloussss",
        "titleHeader": "Comic Con",
        "imageHeader": "",
        "imageEvent": "",
        "localTime": "UTC-5",
        "eventId": "929c55f7-f2a6-4488-89ae-fb53a6fcc2fa",
        "organizationName": "Testing",
        "organizationUrl": "testing",
        "template": "template1",
        "url": "comic-con",
        "startDate": "Tue Nov 10 2020 09:00:00 GMT-0600 (Central Standard Time)",
        "speakers": [],
        "agenda": [
            {
                "date": "Tue Nov 10 2020 09:00:00 GMT-0600 (Central Standard Time)",
                "dayId": "",
                "conferences": []
            }
        ],
        "associates": [],
        "collaborators": [],
        "publicationStatus": False
    }


@pytest.fixture()
def test_associated():
    """
    Return the associated test data
    """
    return {
        "name": "Platzi",
        "url": "platzi.com",
        "logo": "",
        "associatedId": "7dd58685-36aa-4428-87a1-62abe74efc5a"
    }


@pytest.fixture()
def test_day():
    """
    Return a day test data.
    """
    return {
        "date": "Wen Nov 11 2020 09:00:00 GMT-0600 (Central Standard Time)",
        "dayId": "62afcd86-e994-4ab3-927c-c37f9aed021d"
    }


@pytest.fixture()
def test_conference():
    """
    Return a conference test data.
    """
    return {
        "conferenceId": "71392d92-d04a-4217-96e8-e0a9b96f853a",
        "speakerId": "1c8ca878-0580-476e-bd32-735d6403604e",
        "speakerName": "Chadwonck Boseman",
        "speakerBio": "He was the great Kin T'chala",
        "twitter": "@chadwickboseman",
        "rol": "Black Panter",
        "speakerPhoto": "",
        "name": "Black Panter",
        "description": "",
        "startHour": "Sat Sep 26 2020 9:00:00 GMT-0500 (Central Daylight Time)",
        "endHour": "Sat Sep 26 2020 10:00:00 GMT-0500 (Central Daylight Time)"
    }


@ pytest.fixture()
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
