from flask import Flask
from src.backend.routes.apis.accounts import account_bp
from src.backend.routes.apis.transactions import transactions_bp
from src.backend.routes.apis.login import login_bp

app = Flask(__name__)
app.register_blueprint(account_bp)
app.register_blueprint(transactions_bp)
app.register_blueprint(login_bp)

if __name__ == "__main__":
    app.run(debug=True)