from flask import Flask
from routes.auth import auth
from routes.products import products
from routes.cart import cart
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

app.register_blueprint(auth)
app.register_blueprint(products, url_prefix="/products")
app.register_blueprint(cart, url_prefix="/cart")

@app.route("/")
def home():
    return "Welcome to the Flask E-commerce API!"

if __name__ == "__main__":
    app.run(debug=True)
