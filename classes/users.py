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
        # bold = workbook.add_format({'bold': 1})
        # headings = []
        expenseLabels = []
        expenseData = []
        worksheet = workbook.add_worksheet()
        for expense in self.expenses:
            expenseLabels.append(expense.label)
            expenseData.append(expense.value)

        # I have to keep track of the data myself in the sheet
        # Or figure something out with the worksheet.table attribute
        worksheet.write_column('A1', expenseLabels)
        worksheet.write_column('B1', expenseData)
        print(len(worksheet.table.values()))
        pieChart = workbook.add_chart({"type": "pie"})
        pieChart.set_style(10)
        pieChart.add_series(
            {'name': 'Expenses', 'categories': f'=Sheet1!A1:A{len(worksheet.table.values())}', 'values': f'=Sheet1!B1:B{len(worksheet.table.values())}', 'points': [
                {'fill': {'color': '#5ABA10'}},
                {'fill': {'color': '#FE110E'}},
                {'fill': {'color': '#CA5C05'}},
            ]})
        worksheet.insert_chart("E3", pieChart)
        # row = 1
        # col = 1

        # def writeFromExpense():
        #     # create row and col variables
        #     row = 0
        #     col = 0
        #     # fill out spreadsheet titles
        #     # iterate through expenses labels
        #     for expense in self.expenses:
        #         # write label
        #         worksheet.write(row, col, expense.label)
        #         # increase row + 1
        #         row += 1
        #     # reset row and increase col by 1
        #     worksheet.write(row, col, "total")
        #     row = 0
        #     col += 1
        #     # iterate through expenses values
        #     for expense in self.expenses:
        #         # write expense
        #         worksheet.write(row, col, expense.value)
        #         row += 1
        #         # increase row
        #     worksheet.write(row, col, self.total_expenses())
        #     print(self.expenses)

        # writeFromExpense()

        workbook.close()
