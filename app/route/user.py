import logging.config

from flask import Blueprint, g

LOG = logging.getLogger("auth")

user_router = Blueprint("user", __name__, url_prefix="/user")


@user_router.route("/", methods=["GET"])
def get_user() -> dict:
    return g.user.to_json()
