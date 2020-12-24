from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_alchemydumps import AlchemyDumps
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

SPOTIFY_BASE_URL = "https://api.spotify.com"

load_dotenv()
db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate(directory="spotify_opus/migrations")
ad = AlchemyDumps()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(
        "spotify_opus.config.app_config")

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    ad.init_app(app, db)

    from spotify_opus.models import Album

    from spotify_opus.manage import manage_commands
    app.register_blueprint(manage_commands)

    from spotify_opus.controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    @app.errorhandler(ValidationError)
    def handle_bad_request(error):
        return jsonify(error=error.messages), 400

    return app
