"""
Auth endpoints test
"""

# Expected constants
LOGIN_RESPONSE = {
    "access_token": "",
    "token_type": "Bearer",
    "user": {
        "email": "emanuelosva@gmail.com",
        "firstName": "Emanuel",
        "lastName": "Osorio",
        "user_id": "0097e6e1-94de-40d6-b7fd-1487b1e9c56d",
        "organizations": [
            {
                "name": "Debuggers Club",
                "url": "https://debuggers.com",
                "user_id": "some_id",
                "organization_id": "id_organization"
            }
        ],
        "collaborations": [
            {
                "event_id": "c370c4b045dec770bd95apadid",
                "url": "platzi/master",
                "name": "Platzi Master"
            }
        ]
    }
}


# ------------------- Test functions --------------------- #

def test_login_succes(client):
    """
    Test login endpoint,
    """
    print("""POST - /auth/login  - 200 Ok""")
    body = {"email": "emanuelosva@gmail.com", "password": "user123"}
    response = client.post('/auth/login', json=body)
    # Should response status 200
    assert response.status_code == 200
    # Should response with the correct data
    actuall = response.json()
    actuall["access_token"] = ""
    assert actuall == LOGIN_RESPONSE


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
