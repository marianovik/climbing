import logging
import time

import pytest
from psycopg2 import OperationalError
from sqlalchemy_utils import create_database

import db
from app.core import create_app
from db.core import engine

TEST_DATABASE_URL = "postgresql://test_user:test_password@test_db:5432/test_db"


@pytest.fixture(scope="session")
def connection():
    if str(db.engine.url) != TEST_DATABASE_URL:
        raise RuntimeError("Test must be run in the test database!!!")

    try:
        db.engine.connect()
    except OperationalError:
        create_database(db.engine.url)

    for _ in range(10):
        try:
            with db.engine.connect() as conn:
                conn.execute(
                    """
                    SELECT 1
                    """
                )
        except Exception:
            logging.warning("Retrying db.engine.connect()")
            time.sleep(1)
        else:
            break
    else:
        raise RuntimeError("Could not connect to test DB")


@pytest.fixture(scope="session")
def create_db(connection):
    if str(db.engine.url) != TEST_DATABASE_URL:
        raise RuntimeError("Test must be run in the test database!!!")
    db.Base.metadata.drop_all(bind=db.engine)
    db.Base.metadata.create_all(bind=db.engine)


@pytest.fixture()
async def setup_database(connection, create_db):
    db.remove()
    if str(db.engine.url) != TEST_DATABASE_URL:
        raise RuntimeError("Test must be run in the test database!!!")

    db.engine.execute(
        "TRUNCATE {} RESTART IDENTITY CASCADE;\n".format(
            ", ".join(
                f'"{table.name}"' for table in reversed(db.Base.metadata.sorted_tables)
            )
        )
    )

    try:
        yield

    finally:
        db.rollback()
        db.remove()
        engine.dispose()


@pytest.fixture()
def test_app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def test_client(test_app):
    return test_app.test_client()


@pytest.fixture()
def test_user() -> db.User:
    return db.User(
        username="test", email="test@example.com", password="testtest1"
    ).add()
