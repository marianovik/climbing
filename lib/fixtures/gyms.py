import random

import requests as r

import db
from lib.fixtures.data.links import IMAGES

name = [
    "Boulder Room",
    "Bouldering Club",
    "Bouldering",
    "Climb Up",
    "Boulderingowa Akademia",
]
description = [
    "Indoor bouldering gym with a wide variety of courses",
    " Indoor bouldering gym with a variety of walls and challenges",
    "Climbing World is an indoor bouldering gym with a wide range of challenging walls.",
]
address = ["Karmelicka 12", "Glogowska 47", "Grodzka 5", "Wita Stwosza 38/3"]


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


def generate():
    imgs = load_imgs()
    cities = (
        db.Session.query(db.GeoObject).filter(db.GeoObject.obj_type == "city").all()
    )
    for c in cities:
        for i in range(0, random.choice([1, 3, 6, 10])):
            image = db.Image(**random.choice(imgs))
            db.Gym(
                address=random.choice(address),
                description=random.choice(description),
                title=random.choice(name),
                city_id=c.id,
                logo=image,
            ).add()
        db.commit()
