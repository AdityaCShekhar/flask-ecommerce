from bson import ObjectId
from models.db import cart_col, users_col, products_col

def add_to_cart(user_email, product_id):
    user = users_col.find_one({"email": user_email})
    if not user:
        return {"message": "User not found"}, 404

    cart_col.insert_one({
        "userId": user["_id"],
        "productId": ObjectId(product_id)  # store as ObjectId
    })

    return {"message": "Product added to cart!"}, 200

def get_cart(user_email):
    user = users_col.find_one({"email": user_email})
    if not user:
        return {"message": "User not found"}, 404

    cart_items = list(cart_col.find({"userId": user["_id"]}))
    products = []

    for item in cart_items:
        product = products_col.find_one({"_id": item["productId"]})
        if product:
            products.append({
                "_id": str(product["_id"]),
                "name": product["name"],
                "price": float(product['price']),
                "description": product['description'],
                "image": product['image'],  
                "category": product['category'],
                "ratings": float(product.get('ratings', 0.0))
            })

    return {"cart": products}

def remove_from_cart(user_email, product_id):
    user = users_col.find_one({"email": user_email})
    if not user:
        return {"message": "User not found"}, 404

    result = cart_col.delete_one({
        "userId": user["_id"],
        "productId": ObjectId(product_id)
    })

    if result.deleted_count == 0:
        return {"message": "Product not found in cart"}, 404

    return {"message": "Product removed from cart"}, 200