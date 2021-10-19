class Mempool:
    def __init__(self):

        self.transactions = []

    def add_transactions(self, txn):

        self.transactions.append(txn)

    def get_transactions(self):

        element = self.transactions.pop(0)
        return element
