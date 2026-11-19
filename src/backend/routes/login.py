
from flask import Flask, request, jsonify
from src.backend.services.accounts.login.login import LoginVerification
app = Flask(__name__)



@app.route("/login", methods=['POST'])
def transactions_report():
    data = request.get_json()

    user = LoginVerification(data["username"], data["password"])
    if user.verification():
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"error": "Invalid username or password"}), 401
