import db

usernames = [
    "Master Climbing",
    "Rock and Roll",
    "Professional",
    "Maybe Yes Maybe Climb",
    "Dev and Climber",
]


def generate():
    users = [
        db.User(
            username=u.replace(" ", "_"),
            email=f"{u.replace(' ', '_').lower()}@example.com",
            password="secretsecret",
        ).add()
        for u in usernames
    ]
    db.commit()
    return users
