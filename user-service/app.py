from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import uuid
import hashlib
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Static info metric
metrics.info('jewelhub_service_info', 
             'JewelHub Service Info', 
             version='1.0.0')
CORS(app)

# In-memory user storage
# In production this would be MySQL
users = {}

def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "user-service",
        "version": "1.0.0"
    })

@app.route('/users/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')

    if not name or not email or not password:
        return jsonify({
            "success": False,
            "error": "name, email and password required"
        }), 400

    # Check if email already exists
    existing = [u for u in users.values()
                if u['email'] == email]
    if existing:
        return jsonify({
            "success": False,
            "error": "Email already registered"
        }), 409

    # Create user
    user_id = str(uuid.uuid4())[:8].upper()
    user = {
        "user_id": user_id,
        "name": name,
        "email": email,
        "password": hash_password(password),
        "phone": phone,
        "created_at": datetime.now().isoformat(),
        "addresses": []
    }

    users[user_id] = user

    # Return user without password
    safe_user = {k: v for k, v in user.items()
                 if k != 'password'}

    return jsonify({
        "success": True,
        "message": "Registration successful",
        "user": safe_user
    }), 201

@app.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({
            "success": False,
            "error": "email and password required"
        }), 400

    # Find user by email
    user = next((u for u in users.values()
                 if u['email'] == email), None)

    if not user:
        return jsonify({
            "success": False,
            "error": "Invalid email or password"
        }), 401

    # Check password
    if user['password'] != hash_password(password):
        return jsonify({
            "success": False,
            "error": "Invalid email or password"
        }), 401

    # Return user without password
    safe_user = {k: v for k, v in user.items()
                 if k != 'password'}

    return jsonify({
        "success": True,
        "message": "Login successful",
        "user": safe_user
    })

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404

    safe_user = {k: v for k, v in user.items()
                 if k != 'password'}

    return jsonify({
        "success": True,
        "user": safe_user
    })

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = users.get(user_id)

    if not user:
        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404

    # Update allowed fields only
    allowed_fields = ['name', 'phone', 'addresses']
    for field in allowed_fields:
        if field in data:
            users[user_id][field] = data[field]

    users[user_id]['updated_at'] = datetime.now().isoformat()

    safe_user = {k: v for k, v in
                 users[user_id].items()
                 if k != 'password'}

    return jsonify({
        "success": True,
        "message": "Profile updated",
        "user": safe_user
    })

@app.route('/users/<user_id>/address',
           methods=['POST'])
def add_address(user_id):
    data = request.get_json()
    user = users.get(user_id)

    if not user:
        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404

    address = {
        "address_id": str(uuid.uuid4())[:8].upper(),
        "line1": data.get('line1'),
        "city": data.get('city'),
        "state": data.get('state'),
        "pincode": data.get('pincode'),
        "country": data.get('country', 'India'),
        "is_default": data.get('is_default', False)
    }

    users[user_id]['addresses'].append(address)

    return jsonify({
        "success": True,
        "message": "Address added",
        "address": address
    }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)