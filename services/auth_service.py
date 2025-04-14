import jwt
import datetime
from models.db import users_col
import utils
import os

SECRET_KEY = os.getenv("SECRET_KEY")

def register_user(data):
    if users_col.find_one({"email": data['email']}):
        return {"error": "Email already exists!"}
    
    users_col.insert_one({
        "name" : data['name'],
        "email": data['email'],
        "password": utils.hash_password(data['password']),
        # "firstName": data['firstName'],
        # "lastName": data['lastName'],
        # "phone": data['phone'],
        "token_version": 0  # Initially set token version to 0
    })
    return {"message": "User registered successfully!"}


def validate_user(email, password):
    user = users_col.find_one({"email": email})
    
    if user and user["password"] == utils.hash_password(password):
        # Increment token version
        new_token_version = user["token_version"] + 1
        users_col.update_one({"email": email}, {"$set": {"token_version": new_token_version}})
        
        # Create JWT token with the token version included
        payload = {
            "email": user["email"],
            "name": user["name"],
            # "firstName": user["firstName"],
            # "lastName": user["lastName"],
            "token_version": new_token_version,  # Include token version in the payload
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        
        return {
            "message": "Login successful!",
            "token": token,
            "user": {
                "email": user["email"],
                "name": user["name"]
            }
        }

    return {"error": "Invalid credentials!"}

