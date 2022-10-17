from expenses import *
import json
import xlsxwriter


class User:
    def __init__(self, username, monthlyIncome):
        self.username = username
        self.expenses = []
        self.monthlyIncome = (monthlyIncome * 4)
        self.values = []
        self.goals = []

    def addExpense(self, category, label, amount, frequency=1, amountPaid=0, percentagePaid=0, paidForTheMonth=False):
        newExpense = Expense(category, label, amount, frequency=1,
                             amountPaid=0, percentagePaid=0, paidForTheMonth=False)
        self.expenses.append(newExpense)
        return newExpense

    def getUserExpenses(self):
        return self.expenses

    def rule_50_30_20(self):
        print(
            f"{self.monthlyIncome * .50} for needs, {self.monthlyIncome * .30} for wants, {self.monthlyIncome * .20} for savings/debt")

    def total_expenses(self):
        total = 0
        for expense in self.expenses:
            total += expense.value
        return total

    def enoughIncomeCheck(self):
        if self.total_expenses() <= self.monthlyIncome:
            print(
                f"You have in access ${self.monthlyIncome - self.total_expenses()}")
            return False
        else:
            print(
                f"You need to make ${self.total_expenses() - self.monthlyIncome} to break even")
            return True

    def addGoal(self, title, value, date=False):
        goal = {"title": title, "value": value}
        goal["date"] = date
        self.goals.append(goal)
        return goal

    def addValue(self, value):
        self.values.append(value)

    def createChart(self):
        workbook = xlsxwriter.Workbook('../output/test.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'Hello world')
        workbook.close()
