from sqlalchemy import null
import xlsxwriter
from lib.users import *
import json
import os


class Session:
    def __init__(self, id):
        self.id = id
        self.user = null

    def createUser(self, name, income):
        newUser = User(name, income)
        self.user = newUser
        return json.dumps(newUser.__dict__)

    def loadUser(self):
        profileName = 'Test'  # Change to take an input or paramater
        with open(f"users/{profileName}'s-Profile.json") as json_file:
            data = json.load(json_file)
            self.createUser(data['username'], data['monthlyIncome'] / 4)
            # Wrap in loadExpense function because I'll probably need to add more later down the road
            for expense in data['expenses']:
                jsonExpense = json.loads(expense)
                loadedExpense = self.user.addExpense(
                    jsonExpense['category'], jsonExpense['label'], jsonExpense['value'])
                loadedExpense.frequency = jsonExpense['frequency']
                loadedExpense.amountPaid = jsonExpense['amountPaid']
                loadedExpense.percentagePaid = jsonExpense['percentagePaid']
                loadedExpense.frequency = jsonExpense['frequency']
                loadedExpense.paidForTheMonth = jsonExpense['paidForTheMonth']

            for item in data['income']:
                jsonIncome = json.loads(item)
                loadItem = self.user.addIncome(
                    jsonIncome['source'], jsonIncome['amount'], jsonIncome['date'])

    def saveUser(self):
        expensesJSON = []
        incomeJSON = []
        with open(f"users/{self.user.username}'s-Profile.json", 'w') as json_file:
            for expense in self.user.expenses:
                expensesJSON.append(json.dumps(expense.__dict__))
            for income in self.user.income:
                incomeJSON.append(json.dumps(income.__dict__))

            self.user.expenses = expensesJSON
            self.user.income = incomeJSON
            json.dump(self.user.__dict__, json_file)

    def test(self):
        # self.createUser("Test", 571)
        # self.user.addExpense("transportation", "loan", 360)
        # self.user.addExpense("transportation", "gas", 140)
        # self.user.addExpense("food", "groceries", 200)
        # self.user.addExpense("bills", "xfinity", 196)
        # self.user.addExpense("bills", "paypal", 41)
        # self.user.addExpense("bills", "phone", 75)
        # self.user.addExpense("misc_expenses", "fun", 247)
        # self.user.addExpense("misc_expenses", "dates", 140)
        # self.user.addExpense("misc_expenses", "extra car payment", 360)
        # self.user.addExpense("misc_expenses", "personal care", 80)
        # self.user.addExpense("subscriptions", "planet fitness", 20)
        # self.user.addExpense("subscriptions", "youtube", 12)
        # self.user.addExpense("subscriptions", "prime", 9)
        # self.user.addExpense("savings", "general", 400)
        # self.user.addGoal("school loan", 1000, "10/10/22")
        # self.user.addGoal("car loan", 1000)
        # self.user.addValue("Pay bills every month")
        # self.user.addValue("Save 400 dollars every month")
        # self.user.addValue("100 Dollars for dates")
        # self.user.addIncome("Swissport", 571)
        # self.user.addIncome("Swissport", 571)
        # self.user.addIncome("Swissport", 571)
        # self.user.addIncome("Swissport", 571)
        # print(self.user.income)
        # print(self.user.expenses)

        # self.user.enoughIncomeCheck()

        # self.saveUser()

        # self.user.createSpreadsheet()
        self.loadUser()
        self.user.createChart()
        # self.saveUser()
