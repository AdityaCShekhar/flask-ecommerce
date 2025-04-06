from flask import Blueprint, request, jsonify
from services.auth_service import register_user, validate_user
from ..utils import token_required

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    return jsonify(register_user(data))

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    result = validate_user(data["email"], data["password"])
    
    if "error" in result:
        return jsonify(result), 401
    
    return jsonify(result)

@auth.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logged out successfully!"})

@auth.route("/protected", methods=["GET"])
@token_required
def protected_route(current_user):
    return jsonify({"message": f"Hello, {current_user}!"})
