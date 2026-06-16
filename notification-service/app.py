from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Static info metric
metrics.info('jewelhub_service_info', 
             'JewelHub Service Info', 
             version='1.0.0')
CORS(app)

# In-memory notification log
notifications = []

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "notification-service",
        "version": "1.0.0"
    })

@app.route('/notify/order-confirmation',
           methods=['POST'])
def order_confirmation():
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400

    user_name = data.get('user_name')
    user_email = data.get('user_email')
    order_id = data.get('order_id')
    items = data.get('items', [])
    total = data.get('total')

    if not all([user_name, user_email,
                order_id, total]):
        return jsonify({
            "success": False,
            "error": "user_name, user_email, order_id and total required"
        }), 400

    # Build notification message
    item_list = "\n".join([
        f"- {item['name']} x{item['quantity']} = ₹{item['price'] * item['quantity']}"
        for item in items
    ])

    message = f"""
    Dear {user_name},

    Thank you for shopping with JewelHub! 💍

    Your order has been confirmed!

    Order ID: #{order_id}
    ─────────────────────
    {item_list}
    ─────────────────────
    Total: ₹{total}

    Estimated Delivery: 5-7 business days

    For any queries contact us at:
    support@jewelhub.com

    Thank you for choosing JewelHub!
    """

    # Log notification
    notification = {
        "id": len(notifications) + 1,
        "type": "order_confirmation",
        "user_email": user_email,
        "user_name": user_name,
        "order_id": order_id,
        "message": message,
        "status": "sent",
        "sent_at": datetime.now().isoformat()
    }

    notifications.append(notification)

    return jsonify({
        "success": True,
        "message": "Order confirmation notification sent",
        "notification": notification
    }), 201

@app.route('/notify/order-status', methods=['POST'])
def order_status_update():
    data = request.get_json()

    user_name = data.get('user_name')
    user_email = data.get('user_email')
    order_id = data.get('order_id')
    new_status = data.get('status')

    status_messages = {
        "processing": "Your order is being processed! 🔄",
        "shipped": "Your order is on its way! 🚚",
        "delivered": "Your order has been delivered! 🎉",
        "cancelled": "Your order has been cancelled. 😔"
    }

    message = f"""
    Dear {user_name},

    Update on your JewelHub order #{order_id}:

    {status_messages.get(new_status, 'Your order status has been updated')}

    Status: {new_status.upper()}

    Thank you for choosing JewelHub! 💍
    """

    notification = {
        "id": len(notifications) + 1,
        "type": "order_status",
        "user_email": user_email,
        "user_name": user_name,
        "order_id": order_id,
        "status": new_status,
        "message": message,
        "sent_at": datetime.now().isoformat()
    }

    notifications.append(notification)

    return jsonify({
        "success": True,
        "message": f"Status update notification sent",
        "notification": notification
    }), 201

@app.route('/notify/welcome', methods=['POST'])
def welcome_notification():
    data = request.get_json()
    user_name = data.get('user_name')
    user_email = data.get('user_email')

    message = f"""
    Dear {user_name},

    Welcome to JewelHub! 💍✨

    Discover our exclusive collection of
    handcrafted sterling silver jewellery!

    Shop by collection:
    → Rings
    → Necklaces
    → Bracelets
    → Earrings
    → Gifts

    Happy Shopping!
    Team JewelHub
    """

    notification = {
        "id": len(notifications) + 1,
        "type": "welcome",
        "user_email": user_email,
        "user_name": user_name,
        "message": message,
        "sent_at": datetime.now().isoformat()
    }

    notifications.append(notification)

    return jsonify({
        "success": True,
        "message": "Welcome notification sent",
        "notification": notification
    })

@app.route('/notifications', methods=['GET'])
def get_notifications():
    return jsonify({
        "success": True,
        "count": len(notifications),
        "notifications": notifications
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)