from flask import Flask
from flask_cors import CORS
from routes.auth import auth
from routes.products import products
from routes.cart import cart
from routes.image import image
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

CORS(app)  

app.register_blueprint(auth)
app.register_blueprint(image)
app.register_blueprint(products, url_prefix="/products")
# app.register_blueprint(cart, url_prefix="/cart")

if __name__ == "__main__":
    app.run(debug=True)
