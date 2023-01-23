import logging

from flask import Blueprint, request, g
from werkzeug import exceptions

import db
from lib.auth import auth

LOG = logging.getLogger("gym")

gym_router = Blueprint("gym", __name__, url_prefix="/gym")


@gym_router.route("/", methods=["GET"])
def create_gym() -> dict:
    gym: db.Gym = db.Gym(**request.json).add()
    db.commit()
    return gym.to_json()


@gym_router.route("/<gym_id>", methods=["GET"])
def get_gym(gym_id: int) -> dict:
    return db.Gym.query.filter(db.Gym.id == gym_id).one().to_json()


@gym_router.route("/<gym_id>", methods=["PUT"])
@auth.login_required
def update_gym(gym_id: int) -> dict:
    gym: db.Gym = db.Gym.query.filter(db.Gym.id == gym_id).one()
    if g.user.id != gym.id:
        raise exceptions.Forbidden("Only owner can update a gym!")
    for k, v in request.json.items():
        setattr(gym, k, v)
    db.commit()
    return gym.to_json()


@gym_router.route("/<gym_id>", methods=["DELETE"])
@auth.login_required
def delete_gym(gym_id: int) -> dict:
    gym: db.Gym = db.Gym.query.filter(db.Gym.id == gym_id).one()
    if g.user.id != gym.id:
        raise exceptions.Forbidden("Only owner can delete a gym!")
    db.delete(gym)
    db.commit()
    return {"success": True}


@gym_router.route("/<gym_id>", methods=["DELETE"])
@auth.login_required
def delete_gym(gym_id: int) -> dict:
    gym: db.Gym = db.Gym.query.filter(db.Gym.id == gym_id).one()
    if g.user.id != gym.id:
        raise exceptions.Forbidden("Only owner can delete a gym!")
    db.delete(gym)
    db.commit()
    return {"success": True}


@gym_router.route("/<gym_id>/comment", methods=["POST"])
def create_comment(gym_id: int) -> dict:
    gym: db.Gym = db.Gym.query.filter(db.Gym.id == gym_id).one()
    comment: db.Comment = db.Comment(text=request.json["text"])
    comment.object = gym
    db.commit()
    return comment.to_json()


@gym_router.route("/<gym_id>/comment", methods=["GET"])
def get_comments(gym_id: int) -> list:
    gym: db.Gym = db.Gym.query.filter(db.Gym.id == gym_id).one()
    return [comment.to_json() for comment in gym.comments]
