import logging

from sqlalchemy import Column, String, Integer
from sqlalchemy import ForeignKey

from .core import Base

LOG = logging.getLogger("db.gyms")


class Gym(
    Base,
):
    title = Column(
        String,
        nullable=False,
    )
    city_id = Column(
        Integer,
        ForeignKey("geo_objs.id", ondelete="CASCADE"),
        nullable=False,
    )
    address = Column(String, nullable=False)

    __tablename__ = "gyms"
