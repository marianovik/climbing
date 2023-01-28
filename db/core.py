import datetime as dt
import logging

from sqlalchemy import (
    Column,
    Integer,
    orm,
    create_engine,
    inspect,
    text,
    DateTime,
)
from sqlalchemy.ext import declarative

from lib import const

LOG = logging.getLogger("db.core")

engine = create_engine(
    const.DATABASE_URL,
    pool_size=50,
    max_overflow=50,
    echo=False,
)

sessionmaker = orm.sessionmaker(engine)

Session = orm.scoped_session(sessionmaker)


@declarative.as_declarative()
class Base:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = Column(Integer, primary_key=True)

    created_on = Column(
        DateTime,
        nullable=False,
        default=dt.datetime.now(),
        server_default=text("now()"),
    )
    updated_on = Column(
        DateTime,
        nullable=False,
        default=dt.datetime.now(),
        onupdate=dt.datetime.now(),
        server_default=text("now()"),
    )

    @property
    def session(self):
        return inspect(self).session

    query = Session.query_property()

    def add(self, session=None):
        if session:
            session.add(self)
        else:
            Session.add(self)
        return self

    def flush(self):
        Session.add(self)
        Session.flush()
        return self

    def delete(self):
        Session.delete(self)
        return self

    @classmethod
    def resession(cls, s):
        def add(self):
            if s:
                s.add(self)
            else:
                s.add(self)
            return self

        def flush(self):
            s.add(self)
            s.flush()
            return self

        def delete(self):
            s.delete(self)
            return self

        cls.query = s.query_property()
        cls.add = add
        cls.flush = flush
        cls.delete = delete
