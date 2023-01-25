from sqlalchemy_utils import database_exists, create_database

import db
from lib.fixtures import gyms, geo, users


def generate():

    if not database_exists(db.engine.url):
        create_database(db.engine.url)
        db.Base.metadata.create_all(db.engine)

    users.generate()
    geo.generate()
    gyms.generate()
