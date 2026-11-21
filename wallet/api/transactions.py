from flask import Flask, request, jsonify, Blueprint
from wallet.services.payments import TransferService, Deposit
from wallet.models import TransferInfo
from wallet.repositories.transactions import TransationsReport
transactions_bp = Blueprint("transactions", __name__)



@transactions_bp.route("/transactions/report", methods=['POST'])
def transactions_report():
    data = request.get_json()

    transations_report = TransationsReport(user_id=data['user_id'])
    transactions = transations_report.report()

    return jsonify({
        "status": "success",
        "count": len(transactions),
        "transactions": transactions
    }), 200



@transactions_bp.route("/transactions/transfers" ,methods=['POST'])
def transfers():
    data = request.get_json()

    user = TransferInfo(
        idempotency_key=data["idempotency_key"],
        debtor=data["debtor"],
        creditor=data["creditor"],
        transaction_type=data["transaction_type"],
        amount=data["amount"]
    )

    if user.transaction_type == 'transfer':
        service = TransferService(user)
        note = service.transfer()
        report = service.print_report(note)

    if user.transaction_type == 'deposit':
         service = Deposit(user)
         note = service.deposit()
         report = service.report(note)
         

    # transactions_bp.json.sort_keys = False
    return jsonify(report), 200



if __name__ == "__main__":
	transactions_bp.run(debug=True)

