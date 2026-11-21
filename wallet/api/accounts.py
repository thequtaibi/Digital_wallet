from flask import Flask, request, Blueprint, jsonify
from wallet.models import Account
from wallet.services.accounts import AccountService
from wallet.repositories import users
import json
account_bp = Blueprint("accounts", __name__)




@account_bp.route("/accounts", methods=['POST'])
def add_acounts():
	user = Account(
		gov_identification=request.json['gov_identification'],
        first_name=request.json['first_name'], 
        last_name=request.json['last_name'], 
        email=request.json['email'], 
        phone_number=request.json['phone_number'], 
        username=request.json['username'],
        password=request.json['password']
        )
	user_service = AccountService(user)
	response = user_service.save_to_db()
	return {"notes":f"{response}"}


	
@account_bp.route("/accounts/<id_gev>")
def account_informations(id_gev):
    user = users.get_by_gov_id(id_gev)

    if user:
        user_json = json.dumps(user, indent=4)
        return user_json
    else:
          return {"note":"note found"}


def update_account():
      pass

if __name__ == "__main__":
	account_bp.run(debug=True)