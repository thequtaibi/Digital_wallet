
from flask import Flask, request, jsonify, Blueprint
from src.backend.services.accounts.login.login import LoginVerification
login_bp = Blueprint("login", __name__)



@login_bp.route("/login", methods=['POST'])
def transactions_report():
    data = request.get_json()

    user = LoginVerification(data["username"], data["password"])
    if user.verification():
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"error": "Invalid username or password"}), 401
