from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory cart storage
# In production this would be Redis
# cart = { user_id: { product_id: {item details} } }
carts = {}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "cart-service",
        "version": "1.0.0"
    })

@app.route('/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    cart = carts.get(user_id, {})
    items = list(cart.values())
    total = sum(item['price'] * item['quantity']
                for item in items)
    return jsonify({
        "success": True,
        "user_id": user_id,
        "items": items,
        "total": total,
        "item_count": len(items)
    })

@app.route('/cart/<user_id>/add', methods=['POST'])
def add_to_cart(user_id):
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400

    product_id = str(data.get('product_id'))
    if not product_id:
        return jsonify({
            "success": False,
            "error": "product_id required"
        }), 400

    if user_id not in carts:
        carts[user_id] = {}

    if product_id in carts[user_id]:
        carts[user_id][product_id]['quantity'] += 1
    else:
        carts[user_id][product_id] = {
            "product_id": product_id,
            "name": data.get('name'),
            "price": data.get('price'),
            "quantity": 1,
            "image": data.get('image')
        }

    return jsonify({
        "success": True,
        "message": "Item added to cart",
        "cart": list(carts[user_id].values())
    })

@app.route('/cart/<user_id>/update', methods=['PUT'])
def update_quantity(user_id):
    data = request.get_json()
    product_id = str(data.get('product_id'))
    quantity = data.get('quantity', 1)

    if user_id not in carts:
        return jsonify({
            "success": False,
            "error": "Cart not found"
        }), 404

    if product_id not in carts[user_id]:
        return jsonify({
            "success": False,
            "error": "Item not in cart"
        }), 404

    if quantity <= 0:
        del carts[user_id][product_id]
        return jsonify({
            "success": True,
            "message": "Item removed from cart"
        })

    carts[user_id][product_id]['quantity'] = quantity
    return jsonify({
        "success": True,
        "message": "Cart updated",
        "cart": list(carts[user_id].values())
    })

@app.route('/cart/<user_id>/remove', methods=['DELETE'])
def remove_from_cart(user_id):
    data = request.get_json()
    product_id = str(data.get('product_id'))

    if user_id in carts and product_id in carts[user_id]:
        del carts[user_id][product_id]
        return jsonify({
            "success": True,
            "message": "Item removed from cart",
            "cart": list(carts[user_id].values())
        })

    return jsonify({
        "success": False,
        "error": "Item not found in cart"
    }), 404

@app.route('/cart/<user_id>/clear', methods=['DELETE'])
def clear_cart(user_id):
    if user_id in carts:
        carts[user_id] = {}
    return jsonify({
        "success": True,
        "message": "Cart cleared"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)