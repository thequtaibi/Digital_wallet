from flask import Flask
from wallet.api.accounts import account_bp
from wallet.api.transactions import transactions_bp
from wallet.api.auth import login_bp


app = Flask(__name__)
app.register_blueprint(account_bp)
app.register_blueprint(transactions_bp)
app.register_blueprint(login_bp)

if __name__ == "__main__":
    app.run(debug=True)