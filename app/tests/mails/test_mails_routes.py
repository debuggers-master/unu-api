"""
Mails routes testing.
"""
import pytest


@pytest.mark.skip(reason="No send many emails")
def test_send_welcome_email(client):
    """
    Testing send welcome email.
    """
    res = client.post(
        "/api/v1/mails/welcome?email=emanuelosva@gmail.com&name=Emanuel")

    actual = res.json()
    assert actual == {"detail": "Emails sended"}


@pytest.mark.skip(reason="No send many emails")
def test_send_event_alert_email(client):
    """
    Testing send welcome email.
    """
    res = client.post(
        "/api/v1/mails/alert?eventId=01497d8a-14b0-4a1b-9218-9e08acdf182f")

    actual = res.json()
    assert actual == {"detail": "Emails sended"}
