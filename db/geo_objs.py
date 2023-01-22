import logging

from sqlalchemy import Column, String, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from .core import Base

LOG = logging.getLogger("db.geography")


class GeoObject(
    Base,
):
    obj_type = Column(
        String,
        nullable=False,
        comment="'country', 'province', 'city', 'settlement', 'district', etc.",
    )
    admin_level = Column(String, nullable=True)
    name_en = Column(String, nullable=False)
    parent_id = Column(
        Integer,
        ForeignKey("geo_objs.id", ondelete="RESTRICT", name="geo_objs_parent_id_fkey"),
        nullable=True,
        index=True,
    )
    parent = relationship("GeoObject")
    properties = Column(JSONB, comment="Key-value pairs: property code -> value")
    __tablename__ = "geo_objs"
