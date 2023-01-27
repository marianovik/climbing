import logging

from flask import Blueprint, request, g, Response
from werkzeug import exceptions
from werkzeug.utils import secure_filename

import db
from lib.auth import auth

LOG = logging.getLogger("gym")

gym_router = Blueprint("gym", __name__, url_prefix="api/gym")


@gym_router.route("/", methods=["POST"])
@auth.login_required
def create_gym() -> dict:
    data: dict = request.json
    city_name = data.pop("city")
    data["city_id"] = (
        db.Session.query(db.GeoObject.id)
        .filter(db.GeoObject.name_en == city_name)
        .one()
        .id
    )
    data["owner_id"] = g.user.id
    gym: db.Gym = db.Gym(**data).add()
    db.commit()
    return gym.to_json()


@gym_router.route("/<int:gym_id>", methods=["GET"])
def get_gym(gym_id: int) -> dict:
    return db.Gym.query.filter(db.Gym.id == gym_id).one().to_json()


@gym_router.route("/<int:gym_id>", methods=["PUT"])
@auth.login_required
def update_gym(gym_id: int) -> dict:
    gym: db.Gym = db.Gym.query.filter(db.Gym.id == gym_id).one()
    if g.user.id != gym.owner_id:
        raise exceptions.Forbidden("Only owner can update a gym!")
    data: dict = request.json
    if "city" in data:
        city_name = data.pop("city")
        data["city_id"] = (
            db.Session.query(db.GeoObject.id)
            .filter(db.GeoObject.name_en == city_name)
            .one()
            .id
        )
    for k, v in data.items():
        setattr(gym, k, v)
    db.commit()
    return gym.to_json()


@gym_router.route("/<int:gym_id>", methods=["DELETE"])
@auth.login_required
def delete_gym(gym_id: int) -> dict:
    gym: db.Gym = db.Gym.query.filter(db.Gym.id == gym_id).one()
    if g.user.id != gym.owner_id:
        raise exceptions.Forbidden("Only owner can delete a gym!")
    db.delete(gym)
    db.commit()
    return {"success": True}


@gym_router.route("comment/<int:gym_id>", methods=["POST"])
@auth.login_required
def create_comment(gym_id: int) -> dict:
    gym: db.Gym = db.Gym.query.filter(db.Gym.id == gym_id).one()
    comment: db.Comment = db.Comment(text=request.json["text"]).add()
    if user := getattr(g, "user", None):
        comment.owner_id = user.id
    comment.object = gym
    db.commit()
    return comment.to_json()


@gym_router.route("comment/<int:gym_id>", methods=["GET"])
def get_comments(gym_id: int) -> list:
    gym: db.Gym = db.Gym.query.filter(db.Gym.id == gym_id).one()
    return [comment.to_json() for comment in gym.comments]


@gym_router.route("logo/<int:gym_id>", methods=["GET"])
def get_logo(gym_id: int):
    gym: db.Gym = db.Gym.query.filter(db.Gym.id == gym_id).one()
    return Response(
        gym.logo.img,
        mimetype=gym.logo.mimetype,
    )


@gym_router.route("logo/<int:gym_id>", methods=["POST"])
@auth.login_required
def upload_logo(gym_id: int) -> dict:
    gym: db.Gym = db.Gym.query.filter(db.Gym.id == gym_id).one()
    if g.user.id != gym.owner_id:
        raise exceptions.Forbidden("Only owner can update a gym!")
    f = request.files["image"]
    secure_filename(f.filename)
    gym.logo = db.Image(name=f.filename, mimetype=f.mimetype, img=f.read()).add()
    db.commit()
    return {"success": True}
