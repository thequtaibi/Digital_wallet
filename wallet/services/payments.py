import uuid
import time
from datetime import datetime
from wallet.repositories.transactions import RecordedTransactions
from wallet.repositories import users
from wallet.validators import Validations




class TransferService:

    def __init__(self, transactionInfo):
        self.transaction_id = str(uuid.uuid4().int)
        self.transaction_type = transactionInfo.transaction_type
        self.debtor = transactionInfo.debtor
        self.creditor = transactionInfo.creditor
        self.amount = transactionInfo.amount
        self.status = None
        self.created_at = time.time()
        self.idempotency_key = transactionInfo.idempotency_key



    def transfer_process(self):

        if self.amount <= 0:
            raise ValueError("Amount must be positive")

        if self.debtor == self.creditor:
            raise ValueError("Cannot transfer to the same account")

        users.move_balance(self.debtor, self.creditor, self.amount)

        return True

    def validate_transfer(self):
        if self.debtor == self.creditor:
            return "Cannot transfer to the same account."

        if not Validations.valid_users(self.debtor):
            return "Sender account not found."

        if not Validations.valid_users(self.creditor):
                    return "Recipient account not found."

        if not Validations.validate_account(self.debtor, self.amount):
            return "Sender account has insufficient funds or is inactive."


        if self.amount < 1:
            return "Invalid transfer amount."

        return None

    def transfer(self):
        recorded_transactions = RecordedTransactions(
            self.transaction_id,
            self.transaction_type,
            self.debtor,
            self.creditor,
            self.amount,
            self.created_at,
            self.idempotency_key
        )

        message = self.validate_transfer()

        if message is not None:
            self.status = "failed"
            recorded_transactions.record(status=self.status, note=message)
            return message

        if self.transfer_process():
            self.status = "completed"
            recorded_transactions.record(status=self.status, note="Transfer completed successfully.")
            return f"{"Transfer completed successfully."}"

        self.status = "failed"
        return "Transfer failed"



    def print_report(self, note):
        report = {
            "report_name" : "Transfer Receipt",
            "date" : datetime.fromtimestamp(self.created_at),
            "transaction_id" : self.transaction_id,
            "amount" : self.amount,
            "from": self.debtor,
            "to": self.creditor,
            "status": self.status,
            "note": note
        }

        return report





class Deposit:
    def __init__(self, TransferInfo):
        self.transaction_id = str(uuid.uuid4().int)
        self.debtor = TransferInfo.debtor
        self.creditor = TransferInfo.creditor
        self.transaction_type = "deposit"
        self.amount = TransferInfo.amount
        self.status = None
        self.created_at = time.time()
        self.idempotency_key = TransferInfo.idempotency_key



    def _transfer_process(self):

        if self.amount <= 0:
                    raise ValueError("Amount must be positive")

        if self.debtor == self.creditor:
                    raise ValueError("Cannot transfer to the same account")


        return users.add_to_balance(self.creditor, self.amount)

    def _validate_transfer(self):
        if self.debtor == self.creditor:
            return False

        if not Validations.valid_users(self.creditor):
            return False

        if self.amount < 1:
            return False

        return None

    def deposit(self):

        if not Validations.valid_idempotency_key(self.idempotency_key):
            raise ValueError("Erorr")


        recorded_transactions = RecordedTransactions(
                    transaction_id=self.transaction_id,
                    transaction_type=self.transaction_type,
                    debtor=self.debtor,
                    creditor=self.creditor,
                    amount=self.amount,
                    created_at=self.created_at,
                    idempotency_key=self.idempotency_key
                )


        message = self._validate_transfer()



        if message is not None:
            self.status = "failed"
            recorded_transactions.record(status=self.status, note=message)
            return False

        if self._transfer_process():
            self.status = "completed"
            recorded_transactions.record(status=self.status, note=message)
            return True

        self.status = "failed"
        return False

    def report(self, note):
        report = {
            "report_name" : "Deposit Receipt",
            "date" : datetime.fromtimestamp(self.created_at),
            "transaction_id" : self.transaction_id,
            "amount" : self.amount,
            "from": self.debtor,
            "to": self.creditor,
            "status": self.status,
            "note": note
        }

        return report


class Withdraw:
    pass
