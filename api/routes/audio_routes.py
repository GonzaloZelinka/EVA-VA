from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os

from api.services.audio_service import AudioService

audio_bp = Blueprint("audio", __name__)


# @audio_bp.route("/upload", methods=["POST"])
# def upload_audio():
#     if "file" not in request.files:
#         return jsonify({"error": "No file part"}), 400
#     file = request.files["file"]
#     if file.filename == "":
#         return jsonify({"error": "No selected file"}), 400

#     filename = secure_filename(file.filename)
#     file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))

#     return jsonify({"message": "File uploaded successfully", "filename": filename}), 200


@audio_bp.route("/transcribe", methods=["POST"])
def transcribe_audio():
    # Check for the file in the request
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Access the pre-initialized AudioService from app config
    audio_service = current_app.config["audio_service"]
    transcription = audio_service.transcribe_audio_file(filepath)

    # Optionally, remove the audio file after processing
    # os.remove(filepath)

    return jsonify({"transcription": transcription}), 200
