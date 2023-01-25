import logging

import db

LOG = logging.getLogger("tests.gym")


def test_create_gym(
    setup_database, client, test_user: db.User, test_token: str, test_geo
):
    db.commit()
    data = {
        "title": "Test",
        "description": "Test Desc",
        "owner_id": test_user.id,
        "city": "Wroclaw",
        "address": "Wroclaw",
    }
    response = client.post(
        "/gym/",
        json=data,
        headers={"Authorization": f"Bearer {test_token}"},
    )
    print(response.text)
    gym = db.Gym.query.filter(db.Gym.title == "Test").one()
    assert gym.to_json() == response.json


def test_get_gym(setup_database, client, test_gym):
    db.commit()
    response = client.get(
        f"/gym/{test_gym.id}",
    )
    assert test_gym.to_json() == response.json


def test_update_gym(setup_database, client, test_gym, test_token):
    data = {
        "title": "Custom Test",
    }
    db.commit()
    client.put(
        f"/gym/{test_gym.id}",
        headers={"Authorization": f"Bearer {test_token}"},
        json=data,
    )
    assert test_gym.title == "Custom Test"
