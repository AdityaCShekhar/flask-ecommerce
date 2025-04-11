from flask import Blueprint, request, jsonify
from services.cart_service import add_to_cart, view_cart, remove_from_cart

cart = Blueprint("cart", __name__)

@cart.route("/add_to_cart/<product_id>", methods=["POST"])
def add_to_cart_route(product_id):
    response = add_to_cart(product_id)
    return jsonify(response)

@cart.route("/view_cart", methods=["GET"])
def view_cart_route():
    response = view_cart()
    return jsonify(response)

@cart.route("/remove_from_cart/<product_id>", methods=["DELETE"])
def remove_from_cart_route(product_id):
    response = remove_from_cart(product_id)
    return jsonify(response)
