from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

load_dotenv()
db: SQLAlchemy = SQLAlchemy()
ma: Marshmallow = Marshmallow()
bcrypt: Bcrypt = Bcrypt()
jwt: JWTManager = JWTManager()
migrate: Migrate = Migrate(directory="spotify_opus/migrations")


def create_app() -> Flask:
    app = Flask("spotify_opus")
    app.config.from_object(
        "spotify_opus.config.app_config")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from spotify_opus.commands import db_commands
    app.register_blueprint(db_commands)

    from spotify_opus.controllers import registerable_controllers

    for controller in registerable_controllers:
        app.register_blueprint(controller)

    @app.errorhandler(ValidationError)
    def handle_bad_request(error):
        return (jsonify(error=error.messages), 400)

    return app
