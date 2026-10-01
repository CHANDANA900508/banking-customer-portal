from flask import Flask, request, jsonify
app = Flask(__name__)
customers = {}
@app.route("/")
def home():
    return "Banking Customer Portal is running"
@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "application": "customer-portal"
    })
@app.route("/customers", methods=["POST"])
def register_customer():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({
            "error": "Name and email are required"
        }), 400
    customer_id = len(customers) + 1
    customer = {
        "id": customer_id,
        "name": data["name"],
        "email": data["email"]
    }
    customers[customer_id] = customer
    return jsonify(customer), 201
@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = customers.get(customer_id)
    if not customer:
        return jsonify({
            "error": "Customer not found"
        }), 404
    return jsonify(customer)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)