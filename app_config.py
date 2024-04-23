from extensions import db, migrate, cors, login_manager
from flask import Flask
from config import config_object


def create_app(config=config_object["development"]):

    app = Flask(__name__)

    app.config.from_object(config)

    cors.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    return app
