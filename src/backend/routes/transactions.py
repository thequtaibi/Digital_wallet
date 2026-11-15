from flask import Flask, request, jsonify
app = Flask(__name__)
from src.backend.services.transactions.transfer import TransferInfo, TransferService


def view_transaction_history():
    pass



def deposits():
    pass

def withdrawals():
    pass



@app.route("/transactions/transfers" ,methods=['POST'])
def transfers():
    data = request.get_json()

    user = TransferInfo(
        from_account_id=data["from_account_id"],
        to_account_id=data["to_account_id"],
        amount=data["amount"]
    )

    service = TransferService(user)
    result = service.transfer()

    if result:
        return jsonify({
            "message": "Transfer completed successfully"
        }), 200

    return jsonify({
        "error": "Transfer failed"
    }), 400




if __name__ == "__main__":
	app.run(debug=True)

