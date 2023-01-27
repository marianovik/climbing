from sqlalchemy_utils import database_exists, create_database

import db
from lib.fixtures import gyms, geo, users, competitions
from lib.fixtures.utils import load_imgs


def generate():
    if not database_exists(db.engine.url):
        create_database(db.engine.url)
        db.Base.metadata.create_all(db.engine)
    imgs: list = load_imgs()
    gen_users = users.generate()
    geo.generate()
    gyms.generate(imgs, gen_users)
    competitions.generate(imgs, gen_users)
    db.commit()
