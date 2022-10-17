from datetime import date
import json


class Expense:
    def __init__(self, category, label, value, frequency, amountPaid, percentagePaid, paidForTheMonth):
        self.category = category
        self.value = value
        self.label = label
        self.frequency = frequency
        self.amountPaid = amountPaid
        self.percentagePaid = (self.amountPaid / self.value)
        self.paidForTheMonth = False
        self.amountPaid = amountPaid
        self.percentagePaid = percentagePaid
        self.paidForTheMonth = paidForTheMonth
        # self.dueDate = type(date) # Default for the current date

    def increaseAmountPaid(self, value):
        self.amountPaid = value + self.amountPaid
        self.percentagePaid = (self.amountPaid / self.value)
        if self.percentagePaid >= 1:
            self.paidForTheMonth = True
        return self.amountPaid

    def getPercentagePaid(self):
        return self.percentagePaid

    def getExpense(self):
        expense = {}
        expense['category'] = self.category
        expense['value'] = self.value
        expense['label'] = self.label
        expense['frequency'] = self.frequency
        expense['amountPaid'] = self.amountPaid
        expense['percentagePaid'] = self.percentagePaid
        expense['paidForTheMonth'] = self.paidForTheMonth
        return json.dumps(self.__dict__)

# Import into user
# create extention for temp expense

    # def addTempExpense(self, title, value, timesAMonth):
    #     tempExepense = {"title": title, "value": value,
    #                     "timesAMonth": {timesAMonth}}
