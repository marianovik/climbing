import logging.config

import db

LOG = logging.getLogger("test.auth")


def test_sign_in(setup_database, client, test_user: db.User):
    db.commit()

    response = client.post(
        "/api/auth/sign-in",
        json={"username": test_user.username, "password": "testtest1"},
    )
    assert response.json["user"] == test_user.to_json()
    assert isinstance(response.json["token"], str)
    assert test_user.parse_token(response.json["token"]).id == test_user.id


def test_validate_token(setup_database, client, test_user: db.User):
    db.commit()
    response = client.post(
        "/api/auth/sign-in",
        json={"username": test_user.username, "password": "testtest1"},
    )
    response = client.get(
        "/api/auth/token/validate",
        headers={"Authorization": f"Bearer {response.json['token']}"},
    )
    assert response.json["success"] is True


def test_sign_up(
    setup_database,
    client,
):

    response = client.post(
        "/api/auth/sign-up",
        json={
            "username": "user_2",
            "password": "testtest1",
            "email": "user_2@example.com",
        },
    )
    user = db.User.query.filter(db.User.username == "user_2").first()
    assert response.json["user"] == user.to_json()
