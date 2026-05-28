from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)
app.secret_key = 'jewelhub-secret-key'

# Service URLs
PRODUCT_SERVICE = os.getenv('PRODUCT_SERVICE_URL', 'http://localhost:5001')
CART_SERVICE = os.getenv('CART_SERVICE_URL', 'http://localhost:5002')
ORDER_SERVICE = os.getenv('ORDER_SERVICE_URL', 'http://localhost:5003')
USER_SERVICE = os.getenv('USER_SERVICE_URL', 'http://localhost:5004')
NOTIFICATION_SERVICE = os.getenv('NOTIFICATION_SERVICE_URL', 'http://localhost:5005')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "frontend",
        "version": "1.0.0"
    })

@app.route('/')
def home():
    try:
        response = requests.get(f'{PRODUCT_SERVICE}/products')
        data = response.json()
        products = data.get('products', [])
        featured = products[:4]
        return render_template('index.html',
                             featured=featured)
    except:
        return render_template('index.html',
                             featured=[])

@app.route('/products')
def products():
    try:
        response = requests.get(
            f'{PRODUCT_SERVICE}/products')
        data = response.json()
        products = data.get('products', [])
        return render_template('products.html',
                             products=products,
                             title="All Products")
    except:
        return render_template('products.html',
                             products=[],
                             title="All Products")

@app.route('/him')
def for_him():
    try:
        response = requests.get(
            f'{PRODUCT_SERVICE}/products/gender/him')
        data = response.json()
        products = data.get('products', [])
        return render_template('products.html',
                             products=products,
                             title="For Him")
    except:
        return render_template('products.html',
                             products=[],
                             title="For Him")

@app.route('/her')
def for_her():
    try:
        response = requests.get(
            f'{PRODUCT_SERVICE}/products/gender/her')
        data = response.json()
        products = data.get('products', [])
        return render_template('products.html',
                             products=products,
                             title="For Her")
    except:
        return render_template('products.html',
                             products=[],
                             title="For Her")

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    try:
        response = requests.get(
            f'{PRODUCT_SERVICE}/products/{product_id}')
        data = response.json()
        product = data.get('product', {})
        return render_template('product_detail.html',
                             product=product)
    except:
        return redirect(url_for('products'))

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        user_id = session.get('user_id', 'guest')
        data = request.get_json()
        try:
            response = requests.post(
                f'{CART_SERVICE}/cart/{user_id}/add',
                json=data)
            return jsonify(response.json())
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

    # GET request
    user_id = session.get('user_id', 'guest')
    try:
        response = requests.get(
            f'{CART_SERVICE}/cart/{user_id}')
        data = response.json()
        return render_template('cart.html',
                             cart=data)
    except:
        return render_template('cart.html',
                             cart={
                                 "items": [],
                                 "total": 0
                             })

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        try:
            response = requests.post(
                f'{USER_SERVICE}/users/login',
                json=data)
            result = response.json()
            if result.get('success'):
                session['user_id'] = result['user']['user_id']
                session['user_name'] = result['user']['name']
            return jsonify(result)
        except:
            return jsonify({
                "success": False,
                "error": "Service unavailable"
            }), 500
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        try:
            response = requests.post(
                f'{USER_SERVICE}/users/register',
                json=data)
            result = response.json()
            if result.get('success'):
                requests.post(
                    f'{NOTIFICATION_SERVICE}/notify/welcome',
                    json={
                        "user_name": data.get('name'),
                        "user_email": data.get('email')
                    })
            return jsonify(result)
        except:
            return jsonify({
                "success": False,
                "error": "Service unavailable"
            }), 500
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/orders')
def orders():
    user_id = session.get('user_id', 'guest')
    try:
        response = requests.get(
            f'{ORDER_SERVICE}/orders/user/{user_id}')
        data = response.json()
        return render_template('orders.html',
                             orders=data.get('orders', []))
    except:
        return render_template('orders.html',
                             orders=[])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)