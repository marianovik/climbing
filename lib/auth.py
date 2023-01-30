from flask import g, Request
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer

import db
from lib import const

auth = HTTPTokenAuth(scheme="Bearer")

serializer = TimedJSONWebSignatureSerializer(
    const.SECRET_KEY, const.AUTH_TOKEN_DURATION
)


@auth.verify_token
def verify_token(token):
    user = db.User.parse_token(token)
    g.user = user
    return user


def get_user_from_request(request: Request):
    if "Authorization" in request.headers:
        return db.User.parse_token(request.headers["Authorization"].split()[1])
