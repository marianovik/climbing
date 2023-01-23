from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy.exc import NoResultFound

from app import route
from lib import const
from lib.auth import auth

app = Flask("climbing")


@app.route("/")
def hello_world():
    return "Hello World!"


def create_app():
    app.register_blueprint(route.search_router)
    app.register_blueprint(route.auth_router)
    app.register_blueprint(route.gym_router)
    auth.error_handler(lambda: {"error": "Unauthorized"})
    app.register_error_handler(
        NoResultFound, lambda e: (jsonify({"error": "Not found"}), 404)
    )
    app.register_error_handler(400, lambda e: (jsonify({"error": e.description}), 400))
    app.register_error_handler(404, lambda e: (jsonify({"error": e.description}), 404))
    app.register_error_handler(401, lambda e: (jsonify({"error": e.description}), 401))
    app.register_error_handler(403, lambda e: (jsonify({"error": e.description}), 403))
    app.register_error_handler(500, lambda e: (jsonify({"error": e.description}), 500))
    CORS(
        app=app,
        supports_credentials=True,
        origins=const.CORS_ORIGINS,
    )
    return app