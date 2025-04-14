from flask import Blueprint, jsonify, request
from datetime import datetime
from utils import token_required
from services.order_service import get_orders_by_email, get_all_orders

order = Blueprint("order", __name__)

@order.route("/user", methods=["GET"])
@token_required
def user_orders(current_user):
    return jsonify(get_orders_by_email(current_user)), 200

@order.route("/all", methods=["GET"])
@token_required
def admin_orders(current_user):
    return jsonify(get_all_orders()), 200