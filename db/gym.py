import logging

from sqlalchemy import Column, String, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

import db
from .core import Base

LOG = logging.getLogger("db.gym")


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
    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )
    address = Column(String, nullable=False)
    city = relationship(
        "GeoObject",
        foreign_keys="Gym.city_id",
    )
    owner = relationship("User", back_populates="gyms")

    __tablename__ = "gyms"

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "address": f"{self.address}, "
            f"{self.city.name_en}, "
            f"{self.city.parent.name_en}",
        }

    @property
    def comments(self):
        return (
            db.Comment.query.filter(
                db.Comment.owner_id == self.id, db.Comment.object_type == "Gym"
            )
            .order_by(db.Comment.created_on.desc())
            .all()
        )
