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
    description = Column(String)
    logo_id = Column(
        Integer,
        ForeignKey("images.id", ondelete="SET NULL"),
        nullable=True,
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
    logo = relationship("Image")

    __tablename__ = "gyms"

    @property
    def full_address(self):
        return f"{self.address}, {self.city.name_en}, {self.city.parent.name_en}"

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "address": self.address,
            "city": self.city.name_en,
            "country": self.city.parent.name_en,
            "full_address": self.full_address,
        }

    @property
    def comments(self):
        return (
            db.Comment.query.filter(
                db.Comment.object_id == self.id,
                db.Comment.object_type == self.__class__.__name__,
            )
            .order_by(db.Comment.created_on.desc())
            .all()
        )
