from flask import g
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
