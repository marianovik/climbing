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
        "city_id": 2,
        "address": "Wroclaw",
    }
    response = client.post(
        "/api/gym/",
        json=data,
        headers={"Authorization": f"Bearer {test_token}"},
    )
    gym = db.Gym.query.filter(db.Gym.title == "Test").one()
    assert {**gym.to_json(), "is_owner": True} == response.json


def test_get_gym(setup_database, client, test_gym):
    db.commit()
    response = client.get(
        f"/api/gym/{test_gym.id}",
    )
    assert {**test_gym.to_json(), "is_owner": False} == response.json


def test_update_gym(setup_database, client, test_gym, test_token):
    data = {
        "title": "Custom Test",
    }
    db.commit()
    res = client.put(
        f"/api/gym/{test_gym.id}",
        headers={"Authorization": f"Bearer {test_token}"},
        json=data,
    )
    assert res.status_code == 200
    assert test_gym.title == "Custom Test"


def test_delete_gym(setup_database, client, test_gym, test_token):
    db.commit()
    id_ = test_gym.id
    res = client.delete(
        f"/api/gym/{id_}",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    assert res.status_code == 200
    assert res.json == {"success": True}
    assert db.Gym.query.get(id_) is None


def test_comment_crud(setup_database, client, test_gym, test_token):
    db.commit()
    res = client.post(
        f"/api/gym/comment/{test_gym.id}",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"text": "TEXT!!!"},
    )

    assert res.status_code == 200
    comment = db.Comment.query.filter(db.Comment.object_id == test_gym.id).one()
    assert res.json == comment.to_json()
    assert test_gym.comments == [comment]

    res = client.get(
        f"/api/gym/comment/{test_gym.id}",
        headers={"Authorization": f"Bearer {test_token}"},
    )

    assert res.status_code == 200
    assert res.json == [comment.to_json()]
