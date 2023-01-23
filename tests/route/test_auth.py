import logging.config

import db

LOG = logging.getLogger("test.auth")


def test_sign_in(setup_database, test_client, test_user: db.User):
    db.commit()

    response = test_client.post(
        "/auth/sign-in", json={"username": test_user.username, "password": "testtest1"}
    )
    assert response.json["user"] == test_user.to_json()
    assert isinstance(response.json["token"], str)
    assert test_user.parse_token(response.json["token"]).id == test_user.id


def test_validate_token(setup_database, test_client, test_user: db.User):
    db.commit()
    response = test_client.post(
        "/auth/sign-in", json={"username": test_user.username, "password": "testtest1"}
    )
    response = test_client.get(
        "/auth/token/validate",
        headers={"Authorization": f"Bearer {response.json['token']}"},
    )
    assert response.json["success"] is True


def test_sign_up(
    setup_database,
    test_client,
):

    response = test_client.post(
        "/auth/sign-up",
        json={
            "username": "user_2",
            "password": "testtest1",
            "email": "user_2@example.com",
        },
    )
    user = db.User.query.filter(db.User.username == "user_2").first()
    assert response.json["user"] == user.to_json()
