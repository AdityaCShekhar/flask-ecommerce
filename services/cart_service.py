from flask import request
from services.auth_service import token_required
from models.db import products_col, cart_col, users_col
from bson import ObjectId

@token_required
def add_to_cart(current_user_email, product_id):
    user = users_col.find_one({"email": current_user_email})
    
    try:
        product_obj_id = ObjectId(product_id)
    except:
        return {"error": "Invalid product ID format!"}

    product = products_col.find_one({"_id": product_obj_id})
    if not product:
        return {"error": "Product not found!"}
    
    cart_col.update_one(
        {"user_id": user["_id"]},
        {"$push": {"products": product_obj_id}},
        upsert=True
    )
    return {"message": "Product added to cart!"}


@token_required
def view_cart(current_user_email):
    user = users_col.find_one({"email": current_user_email})
    cart = cart_col.find_one({"user_id": user["_id"]})
    
    if not cart or "products" not in cart:
        return {"cart": []}
    
    products = []
    for product_id in cart["products"]:
        product = products_col.find_one({"_id": product_id})
        if product:
            product["_id"] = str(product["_id"])
            products.append(product)
    
    return {"cart": products}


@token_required
def remove_from_cart(current_user_email, product_id):
    user = users_col.find_one({"email": current_user_email})

    try:
        product_obj_id = ObjectId(product_id)
    except:
        return {"error": "Invalid product ID format!"}

    cart_col.update_one(
        {"user_id": user["_id"]},
        {"$pull": {"products": product_obj_id}}
    )
    
    return {"message": "Product removed from cart!"}
