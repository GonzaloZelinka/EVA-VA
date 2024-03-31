from flask import Blueprint, request, jsonify, current_app


model_bp = Blueprint("model", __name__)


@model_bp.route("/completition", methods=["POST"])
def completition():
    data = request.json
    if "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"]
    response = current_app.config["model_service"].execute(text)

    return jsonify({"response": response}), 200
