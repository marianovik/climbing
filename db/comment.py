import logging

from sqlalchemy import Column, Integer, Text, Unicode
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import generic_relationship

from .core import Base

LOG = logging.getLogger("db.comment")


class Comment(
    Base,
):
    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )
    text = Column(
        Text,
        nullable=False,
    )
    # This is used to discriminate between the linked tables.
    object_type = Column(Unicode(255), nullable=True)
    # This is used to point to the primary key of the linked row.
    object_id = Column(Integer, nullable=True)

    owner = relationship(
        "User",
        foreign_keys="Comment.owner_id",
    )

    __tablename__ = "comments"

    object = generic_relationship(object_type, object_id)

    def to_json(self):
        return {
            "id": self.id,
            "owner": getattr(self.owner, "username", "Guest"),
            "text": self.text,
        }
