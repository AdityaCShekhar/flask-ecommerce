import os
from flask import Blueprint, request, jsonify, send_from_directory
from utils import allowed_file, save_file, UPLOAD_FOLDER

image = Blueprint("image", __name__)

@image.route("/upload", methods=["POST"])
def upload_file():
    """Handle image upload."""
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        file_url = save_file(file)
        return jsonify({"image_url": file_url}), 200

    return jsonify({"error": "Invalid file type"}), 400

@image.route("/uploads/<filename>")
def get_uploaded_file(filename):
    """Serve uploaded images."""
    return send_from_directory(UPLOAD_FOLDER, filename)
