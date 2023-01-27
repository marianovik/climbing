import datetime
import logging

from sqlalchemy import Column, String, Integer, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship

import db
from db.core import Base

LOG = logging.getLogger("db.competition")


class Competition(
    Base,
):
    title = Column(
        String,
        nullable=False,
    )
    description = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    logo_id = Column(
        Integer,
        ForeignKey("images.id", ondelete="SET NULL"),
        nullable=True,
    )
    gym_id = Column(
        Integer,
        ForeignKey("gyms.id", ondelete="CASCADE"),
        nullable=False,
    )
    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )
    count = Column(Integer, default=0, server_default="0")
    owner = relationship("User", back_populates="competitions")
    logo = relationship("Image")
    gym = relationship("Gym")
    participants = relationship("Participant")
    users = relationship(
        "User",
        secondary="participants",
        primaryjoin="Participant.competition_id == Competition.id",
        secondaryjoin="User.id == Participant.user_id",
    )

    __tablename__ = "competitions"

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "gym": self.gym.to_json(),
            "available_spots": self.count,
            "registered": len(self.participants),
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

    @property
    def ended(self) -> bool:
        return self.end <= datetime.datetime.now()


class Participant(
    Base,
):
    competition_id = Column(
        Integer,
        ForeignKey("competitions.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    user = relationship("User")
    competition = relationship("Competition")

    __tablename__ = "participants"
