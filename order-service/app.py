from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import uuid
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Static info metric
metrics.info('jewelhub_service_info', 
             'JewelHub Service Info', 
             version='1.0.0')
CORS(app)

# In-memory order storage
# In production this would be MySQL
orders = {}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "order-service",
        "version": "1.0.0"
    })

@app.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400

    user_id = data.get('user_id')
    items = data.get('items', [])
    address = data.get('address')

    if not user_id or not items or not address:
        return jsonify({
            "success": False,
            "error": "user_id, items and address required"
        }), 400

    # Calculate total
    total = sum(item['price'] * item['quantity']
                for item in items)

    # Generate unique order ID
    order_id = str(uuid.uuid4())[:8].upper()

    # Create order
    order = {
        "order_id": order_id,
        "user_id": user_id,
        "items": items,
        "total": total,
        "address": address,
        "status": "confirmed",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    orders[order_id] = order

    return jsonify({
        "success": True,
        "message": "Order placed successfully",
        "order": order
    }), 201

@app.route('/orders/user/<user_id>', methods=['GET'])
def get_user_orders(user_id):
    user_orders = [o for o in orders.values()
                   if o['user_id'] == user_id]
    user_orders.sort(key=lambda x: x['created_at'],
                     reverse=True)
    return jsonify({
        "success": True,
        "user_id": user_id,
        "count": len(user_orders),
        "orders": user_orders
    })

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = orders.get(order_id)
    if order:
        return jsonify({
            "success": True,
            "order": order
        })
    return jsonify({
        "success": False,
        "error": "Order not found"
    }), 404

@app.route('/orders/<order_id>/status', methods=['PUT'])
def update_status(order_id):
    data = request.get_json()
    new_status = data.get('status')

    valid_statuses = [
        "confirmed",
        "processing",
        "shipped",
        "delivered",
        "cancelled"
    ]

    if new_status not in valid_statuses:
        return jsonify({
            "success": False,
            "error": f"Invalid status. Must be one of {valid_statuses}"
        }), 400

    if order_id not in orders:
        return jsonify({
            "success": False,
            "error": "Order not found"
        }), 404

    orders[order_id]['status'] = new_status
    orders[order_id]['updated_at'] = datetime.now().isoformat()

    return jsonify({
        "success": True,
        "message": f"Order status updated to {new_status}",
        "order": orders[order_id]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)