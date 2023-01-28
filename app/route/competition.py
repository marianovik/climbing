import logging
from datetime import datetime

from flask import Blueprint, request, g, Response
from werkzeug import exceptions
from werkzeug.utils import secure_filename

import db
from lib.auth import auth, get_user_from_request

LOG = logging.getLogger("gym")

comp_router = Blueprint("competition", __name__, url_prefix="/api/comp")


def with_user_fields(comp: db.Competition, user: db.User):
    return {
        **comp.to_json(),
        "is_owner": bool(user and comp.owner_id == user.id),
        "is_registered": bool(
            user
            and bool(
                db.Participant.query.filter(
                    db.Participant.user_id == user.id,
                    db.Participant.competition_id == comp.id,
                ).first()
            )
        ),
    }


@comp_router.route("/", methods=["POST"])
@auth.login_required
def create_comp() -> dict:
    data: dict = request.json
    gym: db.Gym = db.Gym.query.filter(db.Gym.id == data["gym_id"]).one()
    if gym.owner_id != g.user.id:
        raise exceptions.Forbidden("Cannot create competition for this gym!")
    comp: db.Competition = db.Competition(**data).add()
    comp.end = datetime.fromtimestamp(data["end"])
    comp.start = datetime.fromtimestamp(data["start"])
    if data["end"] < data["start"]:
        return "End date cannot be earlier than start!", 400
    db.commit()
    return with_user_fields(comp, g.user)


@comp_router.route("/<int:comp_id>", methods=["GET"])
def get_comp(comp_id: int) -> dict:
    return with_user_fields(
        db.Competition.query.filter(db.Competition.id == comp_id).one(),
        get_user_from_request(request),
    )


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
    if "end" in data:
        comp.end = datetime.fromtimestamp(data["end"])
    if "end" in data:
        comp.start = datetime.fromtimestamp(data["start"])
    if comp.end < comp.start:
        return "End date cannot be earlier than start!", 400
    db.commit()
    return with_user_fields(comp, g.user)


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
    if comp.is_over:
        return "Competition is already ended!", 400

    if comp.count < 1:
        return "Registration is over!", 400
    comp.count = comp.count - 1
    db.Participant = db.Participant(competition_id=comp_id, user_id=g.user.id).add()
    db.commit()
    return {"success": True}


@comp_router.route("/users/<int:comp_id>", methods=["GET"])
def get_registered_users(comp_id: int) -> dict:
    comp: db.Competition = db.Competition.query.filter(
        db.Competition.id == comp_id
    ).one()

    return [u.to_json() for u in comp.users]
