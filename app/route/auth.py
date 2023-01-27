import logging.config
import secrets
import string

from flask import Blueprint, g, request
from sqlalchemy import exc, or_
from validate_email import validate_email
from werkzeug import exceptions

import db
from lib.auth import auth

LOG = logging.getLogger("auth")

auth_router = Blueprint("auth", __name__, url_prefix="api/auth")


@auth_router.route("/sign-in", methods=["POST"])
def sign_in():
    try:
        data: dict = request.get_json()
        username: str = data["username"]
        password: str = data["password"]
        user: db.User = db.User.query.filter(
            or_(db.User.username == username, db.User.email == username)
        ).one()
        if not user.check_password(password):
            raise ValueError
    except (exc.SQLAlchemyError, ValueError):
        raise exceptions.Unauthorized("Incorrect password or user")
    return {
        "user": user.to_json(),
        "success": True,
        "token": user.generate_token(),
        "expired": "",
    }


@auth_router.route("/token/validate", methods=["GET"])
@auth.login_required
def validate_token():
    return {
        "success": True,
    }


@auth_router.route("/sign-up", methods=["POST"])
def sign_up():
    data = request.get_json()
    email: str = data["email"].lower().strip()
    username: str = data["username"].strip()
    password: str = data["password"]
    if not all([validate_email(email), username, password]):
        raise exceptions.BadRequest("Please fill in all fields!")
    if db.User.query.filter_by(email=email).one_or_none():
        raise exceptions.BadRequest(f"User {email} is already registered.")
    user: db.User = db.User(
        email=email,
        password=password,
        username=username,
    ).add()
    db.commit()
    return {
        "user": user.to_json(),
        "success": True,
        "token": user.generate_token(),
        "expired": "",
    }


@auth_router.route("/pwd/reset", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data["email"].lower().strip()
    user: db.User = db.User.query.filter(
        db.User.email == email,
    ).one_or_none()
    if user:
        chars = string.ascii_letters + string.digits
        new_password: str = "".join(secrets.choice(chars) for _ in range(8))
        user.set_password(new_password)
        user.is_password_temporary = True
        db.commit()
        return {
            "success": True,
            "notification": "Please check your mailbox. "
            "Don't forget to check spam folders.",
        }
    raise exceptions.BadRequest(f"No user was found with email {email}")


@auth_router.route("/pwd/update", methods=["POST"])
@auth.login_required
def auth_password_update():
    data: dict = request.get_json()
    g.account.is_password_temporary = False
    g.account.hash_password(data["password"])
    db.commit()
    return {
        "success": True,
        "notification": "Success.",
    }
