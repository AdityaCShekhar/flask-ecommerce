import hashlib
import os
from flask import jsonify, request
from functools import wraps
from werkzeug.utils import secure_filename
from models.db import users_col, cart_col
import jwt

SECRET_KEY = os.getenv("SECRET_KEY")


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def is_valid_user(email, password):
    """Check if user credentials are valid."""
    user = users_col.find_one({"email": email})
    return user and user["password"] == hash_password(password)

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Extract token from "Bearer <token>"
        
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data["email"]
            token_version = data["token_version"]
            
            # Check if token version matches the one stored in the database
            user = users_col.find_one({"email": current_user})
            if user and user["token_version"] != token_version:
                return jsonify({"error": "Token is no longer valid!"}), 401
        
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated_function

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if the file has a valid extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    """Save the file and return its URL."""
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    file_url = f"http://127.0.0.1:5000/uploads/{filename}"
    return file_url
