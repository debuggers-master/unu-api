"""
Events endpoints testing.
"""

from uuid import uuid4
import pytest


# @pytest.mark.skip(reason="Don't create many events")
def test_create_events(client, test_event, get_token, dummy_user):
    """
    Testing for create events.
    """
    token = get_token(dummy_user["email"])
    body = {
        "name": dummy_user["email"],
        "template": test_event["template"],
        "url": test_event["url"],
        "startDate": test_event["startDate"],
        "organizationName": test_event["organizationName"]
    }

    response = client.post(
        "/api/v1/events/",
        headers={"Authorization": f"Bearer {token}"},
        json=body)

    event_id = response.json()["eventId"]
    assert response.status_code == 201
    assert isinstance(event_id, str)


def test_update_event(client, test_event, get_token, dummy_user):
    """
    Testing for update a event.
    """
    token = get_token(dummy_user["email"])
    body = {
        "eventId": test_event["eventId"],
        "eventData": {
            "name": test_event["name"],
            "shortDescription": test_event["shortDescription"],
            "description": test_event["description"],
            "titleHeader": test_event["titleHeader"],
            "imageHeader": test_event["imageHeader"],
            "imageEvent": test_event["imageEvent"],
            "localTime": test_event["localTime"]
        }
    }

    response = client.put(
        "/api/v1/events/",
        headers={"Authorization": f"Bearer {token}"},
        json=body)

    assert response.status_code == 200
    assert response.json() == {"modifiedCount": 0}


def test_event_count_participants(client, test_event, get_token, dummy_user):
    """
    Testing for get event
    """
    token = get_token(dummy_user["email"])
    event_id = test_event["eventId"]

    response = client.get(
        f"/api/v1/events/count-participants?eventId={event_id}",
        headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert isinstance(response.json()["participants"], int)


# @pytest.mark.skip(reason="Don't create many associateds")
def test_event_add_associated(
        client, test_event, get_token, dummy_user, test_associated):
    """
    Testing for add associated
    """
    token = get_token(dummy_user["email"])
    body = {
        "eventId": test_event["eventId"],
        "associatedData": {
            "name": test_associated["name"],
            "url": test_associated["url"],
            "logo": test_associated["logo"]
        }
    }

    response = client.post(
        "/api/v1/events/associates",
        headers={"Authorization": f"Bearer {token}"},
        json=body)

    assert response.status_code == 201
    assert isinstance(response.json()["associatedId"], str)


def test_event_update_associated(
        client, test_event, get_token, dummy_user, test_associated):
    """
    Testing for update associated
    """
    token = get_token(dummy_user["email"])
    body = {
        "eventId": test_event["eventId"],
        "associatedData": {
            "name": test_associated["name"],
            "url": test_associated["url"],
            "logo": test_associated["logo"],
            "associatedId": test_associated["associatedId"]
        }
    }

    response = client.put(
        "/api/v1/events/associates",
        headers={"Authorization": f"Bearer {token}"},
        json=body)

    assert response.status_code == 200
    assert response.json() == {"modifiedCount": 0}


# @pytest.mark.skip(reason="")
def test_event_add_day(
        client, test_event, get_token, dummy_user):
    """
    Testing for add days
    """
    token = get_token(dummy_user["email"])

    body = {
        "eventId": test_event["eventId"],
        "dayData": {
            "date": str(uuid4())
        }
    }

    response = client.post(
        "/api/v1/events/day",
        headers={"Authorization": f"Bearer {token}"},
        json=body)

    assert response.status_code == 201
    assert isinstance(response.json()["dayId"], str)


def test_event_update_day(
        client, test_event, get_token, dummy_user, test_day):
    """
    Testing for add days
    """
    token = get_token(dummy_user["email"])

    body = {
        "eventId": test_event["eventId"],
        "dayData": {
            "date": str(uuid4()),
            "dayId": test_day["dayId"]
        }
    }

    response = client.put(
        "/api/v1/events/day",
        headers={"Authorization": f"Bearer {token}"},
        json=body)

    assert response.status_code == 200
    assert response.json() == {"modifiedCount": 1}


def test_event_add_conference(
        client, test_event, get_token, dummy_user, test_day, test_conference):
    """
    Testing for add days
    """
    token = get_token(dummy_user["email"])

    body = {
        "dayId": test_day["dayId"],
        "eventId": test_event["eventId"],
        "conferenceData": {
            "speakerName": test_conference["speakerName"],
            "speakerBio": test_conference["speakerBio"],
            "twitter": test_conference["twitter"],
            "rol": test_conference["rol"],
            "speakerPhoto": test_conference["speakerPhoto"],
            "name": test_conference["name"],
            "description": test_conference["description"],
            "startHour": test_conference["startHour"],
            "endHour": test_conference["endHour"]
        }
    }

    response = client.post(
        "/api/v1/events/conference",
        headers={"Authorization": f"Bearer {token}"},
        json=body)

    response_body = response.json()
    assert response.status_code == 201
    assert isinstance(response_body["conferenceId"], str)
    assert isinstance(response_body["speakerId"], str)


def test_event_update_conference(
        client, test_event, get_token, dummy_user, test_day, test_conference):
    """
    Testing for add days
    """
    token = get_token(dummy_user["email"])

    body = {
        "dayId": test_day["dayId"],
        "eventId": test_event["eventId"],
        "conferenceData": {
            "speakerName": test_conference["speakerName"],
            "speakerBio": test_conference["speakerBio"],
            "twitter": test_conference["twitter"],
            "rol": test_conference["rol"],
            "speakerPhoto": test_conference["speakerPhoto"],
            "name": test_conference["name"],
            "description": test_conference["description"],
            "startHour": test_conference["startHour"],
            "endHour": test_conference["endHour"],
            "conferenceId": test_conference["conferenceId"],
            "speakerId": "string"
        }
    }

    response = client.put(
        "/api/v1/events/conference",
        headers={"Authorization": f"Bearer {token}"},
        json=body)

    assert response.status_code == 200
    assert response.json() == {"modifiedCount": 1}


def test_event_register_participants(client, test_event):
    """
    Testing for register a participants
    """
    email = f"participant_{str(uuid4())}@mail.com"
    body = {
        "email": email,
        "eventId": test_event["eventId"]
    }

    response = client.post(
        "/api/v1/participants",
        json=body)

    assert response.status_code == 201
    assert response.json() == {"registered": True}


def test_event_change_status(client, test_event, get_token, dummy_user):
    """
    Testing for change event status.
    """
    token = get_token(dummy_user["email"])
    event_id = test_event["eventId"]

    response = client.put(
        f"/api/v1/events/change-status?actualStatus=false&eventId={event_id}",
        headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {"actualStatus": True}
