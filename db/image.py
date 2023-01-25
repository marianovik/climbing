from sqlalchemy import Column, Integer, String, LargeBinary

from db import Base


class Image(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    img = Column(LargeBinary)
    mimetype = Column(String(50))

    __tablename__ = "images"
