from sqlalchemy import null


class Income:
    def __init__(self, source, amount, date):
        self.source = source
        self.amount = amount
        self.date = date
