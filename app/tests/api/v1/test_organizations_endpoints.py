"""
Organizations endpoints testing.
"""

from uuid import uuid4
import pytest


# @pytest.mark.skip(reason="Evite create many organization")
def test_create_organization(client, get_token, dummy_user, test_organization):
    """
    Testing for create a organization.
    """
    token = get_token(dummy_user["email"])
    body = {
        "userId": dummy_user["userId"],
        "organizationData": {
            "organizationLogo": test_organization["organizationLogo"],
            "organizationName": str(uuid4())
        }
    }

    response = client.post(
        "/api/v1/organizations",
        headers={"Authorization": f"Bearer {token}"},
        json=body)

    actuall = response.json()
    assert response.status_code == 201
    assert actuall["organizationLogo"] == test_organization["organizationLogo"]
    assert isinstance(actuall["organizationId"], str)


def test_update_organization(client, get_token, dummy_user, test_organization):
    """
    Testing for update a organization.
    """
    token = get_token(dummy_user["email"])
    body = {
        "userId": dummy_user["userId"],
        "organizationData": {
            "organizationId": test_organization["organizationId"],
            "organizationLogo": test_organization["organizationLogo"],
            "organizationName": test_organization["organizationName"]
        }
    }

    response = client.put(
        "/api/v1/organizations",
        headers={"Authorization": f"Bearer {token}"},
        json=body)

    actuall = response.json()
    assert response.status_code == 200
    assert actuall == {
        "modifiedCount": "0",
        "url": {
            "organizationLogo": test_organization["organizationLogo"]}}


def test_update_organization_401(client, dummy_user, test_organization):
    """
    Testing for update a organization - Unauthorized.
    """
    body = {
        "userId": dummy_user["userId"],
        "organizationData": {
            "organizationId": test_organization["organizationId"],
            "organizationLogo": test_organization["organizationLogo"],
            "organizationName": test_organization["organizationName"]
        }
    }

    response = client.put("/api/v1/organizations", json=body)

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
