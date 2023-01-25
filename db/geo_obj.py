import logging

from sqlalchemy import Column, String, Integer, Index
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .core import Base

LOG = logging.getLogger("db.geo_obj")


class GeoObject(
    Base,
):
    obj_type = Column(
        String,
        nullable=False,
        comment="'country', 'province', 'city', 'settlement', 'district', etc.",
    )
    code = Column(
        String,
        nullable=False,
        comment=(
            "Our own human-readable identifier, unique in combination with obj_type"
        ),
    )
    name_en = Column(String, nullable=False)
    parent_id = Column(
        Integer,
        ForeignKey("geo_objs.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    parent = relationship("GeoObject", uselist=False)
    __tablename__ = "geo_objs"
    __table_args__ = (
        Index("geo_objs_code_type_uidx", "code", "obj_type", unique=True),
    )

    def to_json(self):
        return {
            "id": self.id,
            "name_en": self.name_en,
            "obj_type": self.obj_type,
            "code": self.code,
        }
