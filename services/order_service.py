from bson import ObjectId
from models.db import users_col, cart_col, products_col, orders_col
from datetime import datetime

def create_order_from_cart(user_email, paypal_details):
    user = users_col.find_one({"email": user_email})
    if not user:
        return {"message": "User not found"}, 404

    user_id = user["_id"]
    cart_items = list(cart_col.find({"userId": user_id}))

    if not cart_items:
        return {"message": "Cart is empty"}, 400

    order_items = []
    total_amount = 0.0

    for item in cart_items:
        product = products_col.find_one({"_id": item["productId"]})
        if product:
            order_items.append({
                "productId": str(product["_id"]),
                "name": product["name"],
                "price": float(product["price"])
            })
            total_amount += float(product["price"])

    order_data = {
        "userId": str(user_id),
        "email": user_email,
        "items": order_items,
        "total": round(total_amount, 2),
        "paypal": paypal_details,
        "timestamp": datetime.utcnow()
    }

    orders_col.insert_one(order_data)

    # Clear cart
    cart_col.delete_many({"userId": user_id})

    return {"message": "Order placed successfully!"}, 200

def get_orders_by_email(email):
    orders = list(orders_col.find({"email": email}))
    return format_orders(orders)

def get_all_orders():
    orders = list(orders_col.find())
    return format_orders(orders)

def format_orders(orders):
    for order in orders:
        order["_id"] = str(order["_id"])
        order["timestamp"] = order.get("timestamp", datetime.now()).isoformat()
    return orders
