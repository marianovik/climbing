import logging

from flask import Blueprint, request, g, Response
from werkzeug import exceptions
from werkzeug.utils import secure_filename

import db
from lib.auth import auth

LOG = logging.getLogger("gym")

comp_router = Blueprint("competition", __name__, url_prefix="/api/comp")


@comp_router.route("/", methods=["POST"])
@auth.login_required
def create_comp() -> dict:
    data: dict = request.json
    gym: db.Gym = db.Gym.query.filter(db.Gym.id == data["gym_id"]).one()
    if data["owner_id"] != g.user.id or gym.owner_id != g.user.id:
        raise exceptions.Forbidden("Cannot create competition for this gym!")
    comp: db.Competition = db.Competition(**data).add()
    db.commit()
    return comp.to_json()


@comp_router.route("/<int:comp_id>", methods=["GET"])
def get_comp(comp_id: int) -> dict:
    return db.Competition.query.filter(db.Competition.id == comp_id).one().to_json()


@comp_router.route("/<int:comp_id>", methods=["PUT"])
@auth.login_required
def update_comp(comp_id: int) -> dict:
    comp: db.Competition = db.Competition.query.filter(
        db.Competition.id == comp_id
    ).one()
    if g.user.id != comp.owner_id:
        raise exceptions.Forbidden("Only owner can update a competition!")
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
        setattr(comp, k, v)
    db.commit()
    return comp.to_json()


@comp_router.route("/<int:comp_id>", methods=["DELETE"])
@auth.login_required
def delete_comp(comp_id: int) -> dict:
    comp: db.Competition = db.Competition.query.filter(
        db.Competition.id == comp_id
    ).one()
    if g.user.id != comp.owner_id:
        raise exceptions.Forbidden("Only owner can delete a gym!")
    db.delete(comp)
    db.commit()
    return {"success": True}


@comp_router.route("/comment/<int:comp_id>", methods=["POST"])
@auth.login_required
def create_comment(comp_id: int) -> dict:
    comp: db.Competition = db.Competition.query.filter(
        db.Competition.id == comp_id
    ).one()
    comment: db.Comment = db.Comment(text=request.json["text"]).add()
    if user := getattr(g, "user", None):
        comment.owner_id = user.id
    comment.object = comp
    db.commit()
    return comment.to_json()


@comp_router.route("/comment/<int:comp_id>", methods=["GET"])
def get_comments(comp_id: int) -> list:
    comp: db.Competition = db.Competition.query.filter(
        db.Competition.id == comp_id
    ).one()
    return [comment.to_json() for comment in comp.comments]


@comp_router.route("/logo/<int:comp_id>", methods=["GET"])
def get_logo(comp_id: int):
    comp: db.Competition = db.Competition.query.filter(
        db.Competition.id == comp_id
    ).one()
    return Response(
        comp.logo.img,
        mimetype=comp.logo.mimetype,
    )


@comp_router.route("/logo/<int:comp_id>", methods=["POST"])
@auth.login_required
def upload_logo(comp_id: int) -> dict:
    comp: db.Competition = db.Competition.query.filter(
        db.Competition.id == comp_id
    ).one()
    if g.user.id != comp.owner_id:
        raise exceptions.Forbidden("Only owner can update a gym!")
    f = request.files["image"]
    secure_filename(f.filename)
    comp.logo = db.Image(name=f.filename, mimetype=f.mimetype, img=f.read()).add()
    db.commit()
    return {"success": True}


@comp_router.route("/<int:comp_id>", methods=["POST"])
@auth.login_required
def register(comp_id: int) -> dict:
    comp: db.Competition = db.Competition.query.filter(
        db.Competition.id == comp_id
    ).one()
    if comp.ended:
        return "Competition is already ended!", 400

    if comp.count < 1:
        return "Registration is over!", 400
    comp.count = comp.count - 1
    db.Participant = db.Participant(competition_id=comp_id, user_id=g.user.id).add()
    db.commit()
    return {"success": True}
