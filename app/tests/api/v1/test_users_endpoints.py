"""
Users endpoints testing.
"""


def test_get_user(client, auth_response, get_token, test_user):
    """
    Testing for get authorized user.
    """
    print("""GET - /api/v1/users  - 200""")

    email = test_user["email"]
    name = test_user["name"]
    lastname = test_user["lastName"]
    token = get_token(email)

    user = auth_response(email, name, lastname)
    user = user["user"]
    user["userId"] = test_user["userId"]

    response = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {token}"})

    # The status should be 200
    assert response.status_code == 200
    # The body must be the user in db
    assert response.json() == user


def test_get_user_401(client):
    """
    Testing for get authorized user - Unauthorized.
    """
    print("""GET - /api/v1/users  - 200""")

    response = client.get(
        "/api/v1/users",
        headers={"Authorization": "Bearer bad_token"})

    # The status should be 401
    assert response.status_code == 401
    # The body must be a message for invalid credentials
    assert response.json() == {"detail": "Invalid credentials"}


def test_update_user(client, get_token, test_user):
    """
    Testing for get authorized user.
    """
    print("""PUT - /api/v1/users  - 200""")

    email = test_user["email"]
    name = test_user["name"]
    lastname = test_user["lastName"]
    token = get_token(email)

    response = client.put(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "userId": test_user["userId"],
            "userData": {
                "email": email,
                "firstName": name,
                "lastName": lastname
            }})

    assert response.status_code == 200
    assert response.json() == {"modifiedCount": "0"}
