import random

import db

name = [
    "Boulder Room",
    "Bouldering Club",
    "Bouldering",
    "Climb Up",
    "Boulderingowa Akademia",
    "Level Up",
    "Cool and climb",
]
description = [
    "Indoor bouldering gym with a wide variety of courses",
    " Indoor bouldering gym with a variety of walls and challenges",
    "Climbing World is an indoor bouldering gym with a wide range of challenging walls.",
]
address = ["Karmelicka 12", "Glogowska 47", "Grodzka 5", "Wita Stwosza 38/3"]

comments = [
    "Nice!",
    "Cool!",
    "Never again!",
    "You need to check it out!!! 10/10",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
    "Aenean ex lorem, tincidunt ut ex id, bibendum tempor urna. "
    "Pellentesque ornare, erat ut molestie mattis, tellus magna "
    "ultrices massa, et suscipit erat massa sit amet tortor. Vestibulum "
    "ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; "
    "Curabitur iaculis malesuada varius. Ut id mattis sapien. Nulla aliquam mi risus, "
    "interdum varius sem sollicitudin nec.",
]


def generate(imgs: list, users: list):
    cities: list[db.User] = (
        db.Session.query(db.GeoObject).filter(db.GeoObject.obj_type == "city").all()
    )
    for c in cities:
        for i in range(0, random.choice([1, 3, 6, 10])):
            user = random.choice(users) if random.random() < 0.9 else None
            gym = db.Gym(
                address=random.choice(address),
                description=random.choice(description),
                title=f"{random.choice(name)} owned by {user.username}"
                if user
                else random.choice(name),
                city_id=c.id,
                logo=db.Image(**random.choice(imgs)).add(),
                owner=user,
            ).add()
            db.flush()
            [
                db.Comment(
                    text=random.choice(comments), owner=random.choice(users), object=gym
                ).add()
                for i in range(0, int(random.random() * 10))
            ]
        db.commit()
