from flask import Flask

import app.models
from app.api.v1 import api_v1
from app.config import config_by_name
from app.extensions import bcrypt, cors, db, jwt, migrate


def create_app(config_name: str = "development") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(api_v1, url_prefix="/api/v1")

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    return app
