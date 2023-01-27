import logging

from itsdangerous import SignatureExpired, BadSignature
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

import db
from db.core import Base
from lib.auth import serializer

LOG = logging.getLogger("db.user")


class User(Base):
    username = Column(String)
    password_hash = Column(String)
    email = Column(String, unique=True)
    is_password_temporary = Column(
        Boolean, nullable=False, default=False, server_default="True"
    )

    gyms = relationship("Gym", back_populates="owner")
    competitions = relationship(
        "Competition",
        back_populates="owner",
        order_by="desc(Competition.start)",
    )
    registered_on_competitions = relationship(
        "Competition",
        order_by="desc(Competition.start)",
        secondary="participants",
        primaryjoin="User.id == Participant.user_id",
        secondaryjoin="Participant.competition_id == Competition.id",
        overlaps="participants,users",
    )

    __tablename__ = "users"

    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.set_password(kwargs.pop("password"))
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return "<User %r>" % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def generate_token(self) -> str:
        return serializer.dumps({"user_id": self.id}).decode("ascii")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "gyms": [gym.to_json() for gym in self.gyms],
            "owned_competitions": [comp.to_json() for comp in self.competitions],
            "registered_on_competitions": [
                comp.to_json() for comp in self.registered_on_competitions
            ],
        }

    @classmethod
    def parse_token(cls, token):
        try:
            loaded = serializer.loads(token)
        except (TypeError, SignatureExpired, BadSignature):
            loaded = None
        user: db.User | None = loaded and db.User.query.get(loaded["user_id"])
        return user
