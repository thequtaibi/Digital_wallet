class TransferInfo:
    def __init__(self, idempotency_key, debtor, creditor, amount, transaction_type):
        self.idempotency_key = idempotency_key
        self.debtor = debtor
        self.creditor = creditor
        if transaction_type in ['deposit', "transfer"]:
            self.transaction_type = transaction_type
        self.amount = amount
