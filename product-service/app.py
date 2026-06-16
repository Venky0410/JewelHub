from flask import Flask, jsonify
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Static info metric
metrics.info('jewelhub_service_info', 
             'JewelHub Service Info', 
             version='1.0.0')
CORS(app)

products = [
    {
        "id": 1,
        "name": "Sia CZ Ring",
        "category": "rings",
        "gender": "her",
        "price": 2499,
        "material": "Sterling Silver",
        "description": "Elegant CZ stone ring for everyday wear",
        "image": "sia-cz-ring.jpg",
        "in_stock": True
    },
    {
        "id": 2,
        "name": "Eagle Ring",
        "category": "rings",
        "gender": "him",
        "price": 5499,
        "material": "Sterling Silver",
        "description": "Bold eagle design ring for men",
        "image": "eagle-ring.jpg",
        "in_stock": True
    },
    {
        "id": 3,
        "name": "Silver Lock Chain",
        "category": "necklaces",
        "gender": "her",
        "price": 3999,
        "material": "Sterling Silver",
        "description": "Delicate lock pendant necklace",
        "image": "silver-lock-chain.jpg",
        "in_stock": True
    },
    {
        "id": 4,
        "name": "Bold Silver Chain",
        "category": "necklaces",
        "gender": "him",
        "price": 4999,
        "material": "Sterling Silver",
        "description": "Heavy Cuban link chain for men",
        "image": "bold-silver-chain.jpg",
        "in_stock": True
    },
    {
        "id": 5,
        "name": "Core Bracelet",
        "category": "bracelets",
        "gender": "him",
        "price": 10999,
        "material": "Sterling Silver",
        "description": "Premium silver kada bracelet",
        "image": "core-bracelet.jpg",
        "in_stock": True
    },
    {
        "id": 6,
        "name": "Iris Silver Bracelet",
        "category": "bracelets",
        "gender": "her",
        "price": 3499,
        "material": "Sterling Silver",
        "description": "Elegant chain bracelet for women",
        "image": "iris-bracelet.jpg",
        "in_stock": True
    },
    {
        "id": 7,
        "name": "Statement Hoops",
        "category": "earrings",
        "gender": "her",
        "price": 2999,
        "material": "Sterling Silver",
        "description": "Bold hoop earrings for special occasions",
        "image": "statement-hoops.jpg",
        "in_stock": True
    },
    {
        "id": 8,
        "name": "Silver Studs",
        "category": "earrings",
        "gender": "him",
        "price": 1999,
        "material": "Sterling Silver",
        "description": "Minimalist silver studs for men",
        "image": "silver-studs.jpg",
        "in_stock": True
    },
    {
        "id": 9,
        "name": "Saraswati Silver Frame",
        "category": "gifts",
        "gender": "unisex",
        "price": 2749,
        "material": "999 Pure Silver",
        "description": "Pure silver Saraswati box frame",
        "image": "saraswati-frame.jpg",
        "in_stock": True
    },
    {
        "id": 10,
        "name": "Volt Kada",
        "category": "bracelets",
        "gender": "him",
        "price": 14299,
        "material": "Sterling Silver",
        "description": "Bold silver kada for men",
        "image": "volt-kada.jpg",
        "in_stock": True
    }
]

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "product-service",
        "version": "1.0.0"
    })

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({
        "success": True,
        "count": len(products),
        "products": products
    })

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify({"success": True, "product": product})
    return jsonify({"success": False, "error": "Product not found"}), 404

@app.route('/products/category/<category>', methods=['GET'])
def get_by_category(category):
    filtered = [p for p in products if p['category'] == category]
    return jsonify({
        "success": True,
        "category": category,
        "count": len(filtered),
        "products": filtered
    })

@app.route('/products/gender/<gender>', methods=['GET'])
def get_by_gender(gender):
    filtered = [p for p in products if p['gender'] == gender]
    return jsonify({
        "success": True,
        "gender": gender,
        "count": len(filtered),
        "products": filtered
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)