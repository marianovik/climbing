import logging.config

from flask import Blueprint, g, request

import db
from lib.auth import auth

LOG = logging.getLogger("auth")

user_router = Blueprint("user", __name__, url_prefix="/api/user")


@user_router.route("/", methods=["GET"])
@auth.login_required
def get_user() -> dict:
    return g.user.to_json()


@user_router.route("/", methods=["PUT"])
@auth.login_required
def update_user() -> dict:
    data: dict = request.json
    for k, v in data.items():
        setattr(g.user, k, v)
    db.commit()
    return g.user.to_json()
