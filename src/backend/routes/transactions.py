from flask import Flask, request, jsonify
from src.backend.services.transactions.transfer.transfer import TransferService
from src.backend.services.transactions.depositing.depositing import Deposit
from src.backend.services.transactions.transactions_operations.transfer_info import TransferInfo
from src.backend.services.transactions.transactions_operations.transations_report import TransationsReport
app = Flask(__name__)



@app.route("/transactions/report", methods=['POST'])
def transactions_report():
    data = request.get_json()

    transations_report = TransationsReport(user_id=data['user_id'])
    transactions = transations_report.report()

    return jsonify({
        "status": "success",
        "count": len(transactions),
        "transactions": transactions
    }), 200



@app.route("/transactions/transfers" ,methods=['POST'])
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
         report = service.deposit()

    app.json.sort_keys = False
    return jsonify(report), 200



if __name__ == "__main__":
	app.run(debug=True)

