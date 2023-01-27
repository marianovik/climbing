import logging

from flask import Blueprint, request
from sqlalchemy import true
from sqlalchemy.orm import aliased

import db

LOG = logging.getLogger("search")

search_router = Blueprint("search", __name__, url_prefix="api/search")


@search_router.route("/geo", methods=["GET"])
def search_geo() -> list:
    args: dict = request.args
    query = db.Session.query(db.GeoObject)
    filter_by = true()
    if q := args.get("q"):
        filter_by &= db.GeoObject.name_en.ilike(f"%{q}%")
    if country := args.get("country"):
        country_model = aliased(db.GeoObject)
        query = query.join(country_model, country_model.id == db.GeoObject.parent_id)
        filter_by &= country_model.name_en == country
    if types := args.get("objType"):
        filter_by &= db.GeoObject.obj_type.in_(types.split(","))
    res = query.filter(filter_by).order_by(db.GeoObject.name_en)
    return [i.to_json() for i in res.all()]


@search_router.route("/gyms", methods=["GET"])
def search_gyms() -> list:
    args: dict = request.args
    query = db.Session.query(db.Gym)
    filter_by = true()
    if q := args.get("q"):
        filter_by &= db.Gym.title.ilike(f"%{q}%")
    if args.get("city") or args.get("country"):
        city_model = aliased(db.GeoObject)
        query = query.join(city_model, city_model.id == db.Gym.city_id)
        if country := args.get("country"):
            country_model = aliased(db.GeoObject)
            query = query.join(country_model, country_model.id == city_model.parent_id)
            filter_by &= country_model.name_en == country
        if city := args.get("city"):
            filter_by &= city_model.name_en == city
    res = query.filter(filter_by).order_by(db.Gym.title)
    return [i.to_json() for i in res.all()]
