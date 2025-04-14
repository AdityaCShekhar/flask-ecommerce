from flask import Blueprint, request, jsonify
import requests
from services.cart_service import add_to_cart, get_cart, remove_from_cart
from services.order_service import create_order_from_cart
from paypal_config import PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, BASE_URL
from utils import token_required

cart = Blueprint("cart", __name__)

BASE_URL = "https://api-m.sandbox.paypal.com"

@cart.route("/add_to_cart", methods=["POST"])
@token_required
def add_to_cart_route(current_user):
    data = request.get_json()
    product_id = data.get("productId")
    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    return jsonify(add_to_cart(current_user, product_id))

@cart.route("/remove_from_cart", methods=["POST"])
@token_required
def remove_from_cart_route(current_user):
    data = request.get_json()
    product_id = data.get("productId")

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    response = remove_from_cart(current_user, product_id)
    return jsonify(response)

@cart.route("/get_cart", methods=["GET"])
@token_required
def get_cart_route(current_user):
    return jsonify(get_cart(current_user))

def get_access_token():
    res = requests.post(
        f"{BASE_URL}/v1/oauth2/token",
        auth=(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET),
        data={"grant_type": "client_credentials"},
        headers={"Accept": "application/json"}
    )
    return res.json()["access_token"]

@cart.route("/create_order", methods=["POST"])
@token_required
def create_order(current_user):
    data = request.get_json()
    price = data.get("price")

    if not price:
        return jsonify({"error": "Price is required"}), 400

    try:
        formatted_price = f"{float(price):.2f}"
    except ValueError:
        return jsonify({"error": "Invalid price format"}), 400

    access_token = get_access_token()

    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": formatted_price
            },
            "description": f"Order by user {str(current_user)}"
        }],
        "application_context": {
            "return_url": "http://localhost:3000/payment-success",
            "cancel_url": "http://localhost:3000/payment-cancel"
        }
    }

    response = requests.post(
        f"{BASE_URL}/v2/checkout/orders",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
        json=order_data
    )

    result = response.json()
    if response.status_code == 201:
        return jsonify({"id": result["id"]})
    else:
        return jsonify({"error": result}), 500



@cart.route("/capture_order", methods=["POST"])
@token_required
def capture_order(current_user):
    data = request.get_json()
    order_id = data.get("orderID")

    if not order_id:
        return jsonify({"error": "Order ID is required"}), 400

    access_token = get_access_token()

    response = requests.post(
        f"{BASE_URL}/v2/checkout/orders/{order_id}/capture",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
    )

    result = response.json()
    if response.status_code == 201:
        # store order in DB and clear cart
        store_result, status = create_order_from_cart(current_user, result)
        if status == 200:
            return jsonify({"message": "Payment successful!", "details": result})
        else:
            return jsonify(store_result), status
    else:
        return jsonify({"error": result}), 500
