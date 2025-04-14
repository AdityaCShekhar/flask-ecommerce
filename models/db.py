from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]

users_col = db["users"]
products_col = db["products"]
categories_col = db["categories"]
cart_col = db["cart"]
orders_col = db["orders"]
