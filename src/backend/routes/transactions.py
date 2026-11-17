from flask import Flask, request, jsonify
from src.backend.services.Transactions.transfer.transfer import TransferService
# from src.backend.services.Transactions.depositing.depositing import Deposit
from src.backend.services.Transactions.transfer_info import TransferInfo
app = Flask(__name__)


def view_transaction_history():
    pass



@app.route("/transactions/transfers" ,methods=['POST'])
def transfers():
    data = request.get_json()

    user = TransferInfo(
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
         result = service.transfer()

    app.json.sort_keys = False
    return jsonify(report), 200

    





if __name__ == "__main__":
	app.run(debug=True)

