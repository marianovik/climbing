import logging
from time import sleep

from sqlalchemy_utils import database_exists, drop_database

import db

LOG = logging.getLogger("lib.utils.confest")


def recreate_db():
    from lib.fixtures import generate

    if database_exists(db.engine.url):
        LOG.warning("DROPPING TEST DB -->")
        drop_database(db.engine.url)
        LOG.warning("DROPPING TEST DB --> READY")
        sleep(5)
    LOG.warning("FIXTURES GENERATE -->")
    generate()
    LOG.warning("FIXTURES GENERATE --> READY")
