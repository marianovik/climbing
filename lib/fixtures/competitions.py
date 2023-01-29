import datetime
import random

import db

name = [
    "Boulder Starts",
    "Climb Up!",
    "Bouldering Challenges",
    "Boulderingowa Akademia Starts",
]
description = [
    "Indoor bouldering gym with a wide variety of courses",
    "Indoor bouldering gym with a variety of walls and challenges",
    "Climbing World is an indoor bouldering gym with a wide range of challenging walls.",
]

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
    gyms: list[db.Gym] = db.Gym.query.filter(db.Gym.owner_id.is_not(None)).all()
    for g in gyms:
        comp_1 = db.Competition(
            title=f"{random.choice(name)} {g.title}",
            description=random.choice(description),
            gym_id=g.id,
            logo=db.Image(**random.choice(imgs)).add(),
            owner=g.owner,
            start=datetime.datetime.now() - datetime.timedelta(days=60),
            end=datetime.datetime.now() - datetime.timedelta(days=57),
            count=0,
            users=users,
        ).add()
        db.flush()
        [
            db.Comment(
                text=random.choice(comments), owner=random.choice(users), object=comp_1
            ).add()
            for i in range(0, int(random.random() * 10))
        ]
        comp_2 = db.Competition(
            title=f"{random.choice(name)} {g.title}",
            description=random.choice(description),
            gym_id=g.id,
            logo=db.Image(**random.choice(imgs)).add(),
            owner=g.owner,
            start=datetime.datetime.now() - datetime.timedelta(days=3),
            end=datetime.datetime.now() + datetime.timedelta(days=2),
            count=345,
            users=users,
        ).add()
        db.flush()
        [
            db.Comment(
                text=random.choice(comments), owner=random.choice(users), object=comp_2
            ).add()
            for i in range(0, int(random.random() * 10))
        ]
        comp_3 = db.Competition(
            title=f"{random.choice(name)} {g.title}",
            description=random.choice(description),
            gym_id=g.id,
            logo=db.Image(**random.choice(imgs)).add(),
            owner=g.owner,
            start=datetime.datetime.now() + datetime.timedelta(days=15),
            end=datetime.datetime.now() + datetime.timedelta(days=18),
            count=674,
        ).add()
        db.flush()
        [
            db.Comment(
                text=random.choice(comments), owner=random.choice(users), object=comp_3
            ).add()
            for i in range(0, int(random.random() * 10))
        ]
        db.commit()
