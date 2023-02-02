import datetime
import logging

import db

LOG = logging.getLogger("tests.competition")


def test_create_comp(
    setup_database,
    client,
    test_user: db.User,
    test_token: str,
    test_gym: db.Gym,
    test_geo,
):
    db.commit()
    data = {
        "title": "Test",
        "start": datetime.datetime.timestamp(datetime.datetime.now()),
        "end": datetime.datetime.timestamp(datetime.datetime.now()),
        "description": "Test Desc",
        "owner_id": test_user.id,
        "gym_id": test_gym.id,
    }
    response = client.post(
        "/api/comp/",
        json=data,
        headers={"Authorization": f"Bearer {test_token}"},
    )
    comp = db.Competition.query.filter(db.Competition.title == "Test").one()
    assert {**comp.to_json(), "is_owner": True, "is_registered": False} == response.json


def test_get_comp(setup_database, client, test_competition):
    db.commit()
    response = client.get(
        f"/api/comp/{test_competition.id}",
    )
    assert {
        **test_competition.to_json(),
        "is_owner": False,
        "is_registered": False,
    } == response.json


def test_update_comp(setup_database, client, test_competition, test_token):
    data = {
        "title": "Custom Test",
    }
    db.commit()
    res = client.put(
        f"/api/comp/{test_competition.id}",
        headers={"Authorization": f"Bearer {test_token}"},
        json=data,
    )
    assert res.status_code == 200
    assert test_competition.title == "Custom Test"


def test_delete_comp(setup_database, client, test_competition, test_token):
    db.commit()
    id_ = test_competition.id
    res = client.delete(
        f"/api/comp/{id_}",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    assert res.status_code == 200
    assert res.json == {"success": True}
    assert db.Competition.query.get(id_) is None


def test_comment_crud(setup_database, client, test_competition, test_token):
    db.commit()
    res = client.post(
        f"/api/comp/comment/{test_competition.id}",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"text": "TEXT!!!"},
    )

    assert res.status_code == 200
    comment = db.Comment.query.filter(db.Comment.object_id == test_competition.id).one()
    assert res.json == comment.to_json()
    assert test_competition.comments == [comment]

    res = client.get(
        f"/api/comp/comment/{test_competition.id}",
        headers={"Authorization": f"Bearer {test_token}"},
    )

    assert res.status_code == 200
    assert res.json == [comment.to_json()]


def test_register(setup_database, client, test_competition, test_token, test_user):
    db.commit()
    res = client.post(
        f"/api/comp/{test_competition.id}",
        headers={"Authorization": f"Bearer {test_token}"},
        json={},
    )

    assert res.status_code == 200
    assert test_competition.count == 9
    assert test_competition.users == [test_user]
