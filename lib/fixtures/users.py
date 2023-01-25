import db

usernames = [
    "Master Climbing",
    "Rock and Roll",
    "Professional",
    "Maybe Yes Maybe Climb",
    "Dev and Climber",
]


def generate():
    for u in usernames:
        db.User(
            username=u,
            email=f"{u.replace(' ', '_').lower()}@example.com",
            password="secretsecret",
        ).add()
    db.commit()
