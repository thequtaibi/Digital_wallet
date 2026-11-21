# wallet/errors.py
class WalletError(Exception):
    status = 400

class InsufficientFunds(WalletError):
    status = 400

class AccountNotFound(WalletError):
    status = 404