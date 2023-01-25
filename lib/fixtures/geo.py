import db
from lib.fixtures.data.geo_objs import COUNTRIES


def generate():
    for i in COUNTRIES:
        cities = i.pop("cities")
        country = db.GeoObject(**i).add()
        db.flush()
        for c in cities:
            db.GeoObject(obj_type="city", parent_id=country.id, **c).add()
    db.commit()
