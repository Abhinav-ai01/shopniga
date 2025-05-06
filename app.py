from flask import Flask, render_template, request, redirect, url_for, session
import boto3, os
from config import S3_BUCKET, S3_KEY, S3_SECRET, S3_REGION
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secret-key'

# AWS S3 Config
s3 = boto3.client('s3', aws_access_key_id=S3_KEY,
                  aws_secret_access_key=S3_SECRET,
                  region_name=S3_REGION)

# Dummy product list
PRODUCTS = [
    {"id": 1, "name": "Sneakers", "price": 59.99, "image": "https://via.placeholder.com/150"},
    {"id": 2, "name": "T-Shirt", "price": 19.99, "image": "https://via.placeholder.com/150"},
    {"id": 3, "name": "Watch", "price": 99.99, "image": "https://via.placeholder.com/150"},
]

@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS)

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if product:
        cart = session.get('cart', [])
        cart.append(product)
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join("uploads", filename))
    s3.upload_file(f"uploads/{filename}", S3_BUCKET, filename)
    return "Uploaded to S3"

if __name__ == '__main__':
    app.run(debug=True)
