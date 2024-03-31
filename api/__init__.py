from flask import Flask

from api.services.audio_service import AudioService
from api.services.model_service import ModelService
from .routes.audio_routes import audio_bp


def create_app(config_filename="config"):
    app = Flask(__name__)

    # Load Config
    app.config.from_object(config_filename)

    # Initialize AudioService and store it in app config
    app.config["audio_service"] = AudioService(app)
    # Initialize ModelService and store it in app config
    app.config["model_service"] = ModelService()

    # Register Blueprints
    app.register_blueprint(audio_bp, url_prefix="/audio")

    return app
