import logging

from flask import Blueprint, request
from sqlalchemy import true

import db
from lib.auth import auth

LOG = logging.getLogger("search")

search_router = Blueprint("search", __name__, url_prefix="/search")


@search_router.route("/geo", methods=["GET"])
@auth.login_required
def search_geo() -> list:
    args: dict = request.args
    query = db.Session.query(db.GeoObject)
    filter_by = true()
    if q := args.get("q"):
        filter_by &= db.GeoObject.name_en.ilike(f"%{q}%")
    if types := args.get("adminLevel", ""):
        filter_by &= db.GeoObject.admin_level.in_(types.split(","))
    res = query.filter(filter_by).order_by(db.GeoObject.name_en)
    return [i.to_json() for i in res.all()]


@search_router.route("/gyms", methods=["GET"])
@auth.login_required
def search_gyms() -> list:
    args: dict = request.args
    query = db.Session.query(db.Gym)
    filter_by = true()
    if q := args.get("q"):
        filter_by &= db.Gym.title.ilike(f"%{q}%")
    if city_id := args.get("cityId"):
        filter_by &= db.Gym.city_id == int(city_id)
    res = query.filter(filter_by).order_by(db.Gym.title)
    return [i.to_json() for i in res.all()]
