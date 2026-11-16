class TransferInfo:
    def __init__(self, debtor, creditor, amount, transaction_type):
        self.debtor = debtor
        self.creditor = creditor
        if transaction_type in ['deposit', "transfer"]:
            self.transaction_type = transaction_type
        self.amount = amount
