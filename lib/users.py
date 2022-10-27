from contextlib import nullcontext
from sqlalchemy import null
from lib.expenses import *
from lib.income import *

import json
import xlsxwriter


class User:
    def __init__(self, username, monthlyIncome):
        self.username = username
        self.expenses = []
        self.income = []
        self.monthlyIncome = (monthlyIncome * 4)
        self.values = []
        self.goals = []

    def addExpense(self, category, label, amount, frequency=1, amountPaid=0, percentagePaid=0, paidForTheMonth=False):
        newExpense = Expense(category, label, amount, frequency=1,
                             amountPaid=0, percentagePaid=0, paidForTheMonth=False)
        self.expenses.append(newExpense)
        return newExpense

    def addIncome(self, source, amount, date=0):
        incomeItem = Income(source, amount, date)
        self.income.append(incomeItem)
        return incomeItem

    def getUserIncome(self):
        return self.income

    def totalIncome(self):
        total = 0
        for item in self.income:
            total += item.amount
        return total

    def getUserExpenses(self):
        return self.expenses

    def rule_50_30_20(self):
        print(
            f"{self.totalIncome() * .50} for needs, {self.totalIncome() * .30} for wants, {self.totalIncome() * .20} for savings/debt")

    def total_expenses(self):
        total = 0
        for expense in self.expenses:
            total += expense.value
        return total

    def total_expenses_cat(self):
        totalExpenses = {}
        for expense in self.expenses:
            if expense.category not in totalExpenses.keys():
                totalExpenses[expense.category] = expense.value
            else:
                # iftotalExpenses[expense.category]:
                totalExpenses[expense.category] += expense.value
        return totalExpenses

    def enoughIncomeCheck(self):
        if self.total_expenses() <= self.totalIncome():
            print(
                f"You have in access ${self.totalIncome() - self.total_expenses()}")
            return False
        else:
            print(
                f"You need to make ${self.total_expenses() - self.totalIncome()} to break even")
            return True

    def addGoal(self, title, value, date=False):
        goal = {"title": title, "value": value}
        goal["date"] = date
        self.goals.append(goal)
        return goal

    def addValue(self, value):
        self.values.append(value)

    def createChart(self):
        workbook = xlsxwriter.Workbook(
            f"output/{self.username.title()}'s-Budget.xlsx")

        dollarFormat = workbook.add_format(
            {'num_format': '-$#,##0.00'})
        labelFormat = workbook.add_format({'bold': True})

        def createExpenseSheet():
            expenseLabels = []
            expenseData = []
            expenseSheet = workbook.add_worksheet("Expenses")
            for expense in self.expenses:
                expenseLabels.append(expense.label.title())
                expenseData.append(expense.value)

            dollarFormat = workbook.add_format(
                {'num_format': '$#,##0.00'})
            expenseSheet.set_column(1, 1, 10, dollarFormat)
            labelFormat = workbook.add_format({'bold': True})
            expenseSheet.set_column(0, 0, 20, labelFormat)
            expenseSheet.set_column(3, 3, 20, labelFormat)
            expenseSheet.set_column(4, 4, 10, dollarFormat)
            expenseSheet.write_column('A1', expenseLabels)
            expenseSheet.write_column('B1', expenseData)
            expenseLastCell = len(expenseSheet.table.values())
            expenseSheet.write(f'A{expenseLastCell+1}', "Total Expenses")
            expenseSheet.write(f'B{expenseLastCell+1}', self.total_expenses())

            allExpensesPieChart = workbook.add_chart({"type": "pie"})
            allExpensesPieChart.set_style(10)
            allExpensesPieChart.add_series(
                {'name': 'Expenses', 'categories': f'=Expenses!A1:A{expenseLastCell - 1}', 'values': f'=Expenses!B1:B{expenseLastCell - 1}', 'points': [
                    {'fill': {'color': '#5ABA10'}},
                    {'fill': {'color': '#FE110E'}},
                    {'fill': {'color': '#CA5C05'}},
                ]})
            groupedExpensesPieChart = workbook.add_chart({"type": "pie"})
            expenseSheet.insert_chart("G3", allExpensesPieChart)
            groupedExpenseTotals = self.total_expenses_cat()
            expenseSheet.write_column(
                'D1', groupedExpenseTotals.keys(), labelFormat)
            expenseSheet.write_column(
                'E1', groupedExpenseTotals.values(), dollarFormat)
            groupedExpensesPieChart.add_series(
                {'name': 'Expenses', 'categories': f'=Expenses!D1:D{len(groupedExpenseTotals.keys())}', 'values': f'=Expenses!E1:E{len(groupedExpenseTotals.values()    )}', 'points': [
                    {'fill': {'color': '#5ABA10'}},
                    {'fill': {'color': '#FE110E'}},
                    {'fill': {'color': '#CA5C05'}},
                ]})

            groupedExpensesPieChart.set_style(10)
            expenseSheet.insert_chart("G20", groupedExpensesPieChart)

        def createIncomeSheet():
            incomeSheet = workbook.add_worksheet("Income")

            incomeSources = []
            incomeAmounts = []
            for item in self.income:
                incomeSources.append(item.source)
                incomeAmounts.append(item.amount)

            incomeSheet.write_column("A1", incomeSources, labelFormat)
            incomeSheet.write_column("B1", incomeAmounts, dollarFormat)
        self.total_expenses_cat()

        createExpenseSheet()
        createIncomeSheet()

        workbook.close()
