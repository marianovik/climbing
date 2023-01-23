import datetime as dt
import logging

from itsdangerous import SignatureExpired, BadSignature
from sqlalchemy import Column, DateTime, String, text, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

import db
from db.core import Base
from lib.auth import serializer

LOG = logging.getLogger("db.user")


class User(Base):
    updated_on = Column(
        DateTime,
        nullable=False,
        default=dt.datetime.now(),
        onupdate=dt.datetime.now(),
        server_default=text("now()"),
    )
    username = Column(String)
    password_hash = Column(String)
    email = Column(String, unique=True)
    is_password_temporary = Column(
        Boolean, nullable=False, default=True, server_default="true"
    )

    gyms = relationship("Gym", back_populates="owner")

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
        return {"id": self.id, "username": self.username, "email": self.email}

    @classmethod
    def parse_token(cls, token):
        try:
            loaded = serializer.loads(token)
        except (TypeError, SignatureExpired, BadSignature):
            loaded = None
        user: db.User | None = loaded and db.User.query.get(loaded["user_id"])
        return user
