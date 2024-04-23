from extensions import db, migrate, cors, login_manager
from flask import Flask


def create_app():

    app = Flask(__name__)

    cors.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    return app
