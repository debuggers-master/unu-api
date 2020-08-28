"""
Auth endpoints test
"""
import pytest


def test_login_succes(client, auth_response):
    """
    Test login endpoint,
    """
    print("""POST - /auth/login  - 200 Ok""")

    email = "stan@gmail.com"
    name = "Stan"
    lastname = "Lee"
    body = {"email": f"{email}", "password": "user123"}
    response = client.post('/auth/login', json=body)
    # Should response status 200
    assert response.status_code == 200
    # Should response with the correct data
    actuall = response.json()
    actuall["access_token"] = ""
    actuall["user"]["userId"] = ""
    assert actuall == auth_response(email, name, lastname)


def test_login_bad_password(client):
    """
    Test login endpint when a bad password is sent.
    """
    print("""POST - /auth/login  - 401 Unauthorized - Bad password""")

    body = {"email": "emanuelosva@gmail.com", "password": "bad_password"}
    response = client.post('/auth/login', json=body)
    # Should response status 401
    assert response.status_code == 401
    # Should response with the correct data
    actuall = response.json()
    expected = {"detail": "Invalid credentials"}
    assert actuall == expected


def test_login_bad_email(client):
    """
    Test login endpint when a bad password is sent.
    """
    print("""POST - /auth/login  - 401 Unauthorized - Bad email""")
    body = {"email": "bad_email@gmail.com", "password": "user123"}
    response = client.post('/auth/login', json=body)
    # Should response status 401
    assert response.status_code == 401
    # Should response with the correct data
    actuall = response.json()
    expected = {"detail": "Invalid credentials"}
    assert actuall == expected


def test_signup_user_exists(client):
    """
    Test login endpoint,
    """
    print("""POST - /auth/login  - 409 Conflict""")
    body = {
        "email": "emanuelosva@gmail.com",
        "password": "user123",
        "firstName": "Nicole",
        "lastName": "Chapaval"
    }
    response = client.post('/auth/signup', json=body)
    # Should response status 200
    assert response.status_code == 409
    # Should response with the correct data
    actuall = response.json()
    expected = {"detail": "The email already exists"}
    assert actuall == expected


@pytest.mark.skip(reason="To not create many users")
def test_signup_succes(client, auth_response):
    """
    Test login endpoint,
    """
    print("""POST - /auth/signup  - 200 Ok""")

    email = "vickytone@hey.com"
    name = "Vicky"
    lastname = "Stone"
    body = {
        "email": f"{email}",
        "firstName": f"{name}",
        "lastName": f"{lastname}",
        "password": "user123"
    }
    response = client.post('/auth/signup', json=body)
    # Should response status 200
    assert response.status_code == 201
    # Should response with the correct data
    actuall = response.json()
    actuall["access_token"] = ""
    actuall["user"]["userId"] = ""
    assert actuall == auth_response(email, name, lastname)
