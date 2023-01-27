from time import time, sleep

from sqlalchemy_utils import database_exists, drop_database

import db
from lib.fixtures.data.links import IMAGES
import requests as r

import datetime
import logging

from sqlalchemy import Column, String, Integer, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship

import db
from db.core import Base


def load_imgs():
    b_images = []
    for i in IMAGES:
        response = r.get(i)
        b_images.append(
            {
                "img": response.content,
                "name": "logo",
                "mimetype": response.headers["content-type"],
            }
        )
    return b_images
