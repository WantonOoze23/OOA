#"ОЩАДБАНК": створіть класи для транзакцій, бюджетів і категорій, дозволяючи користувачам відстежувати доходи та витрати.

from datetime import datetime
import pandas as pd

class Category:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __str__(self):
        return f"Назва: {self.name}, опис: {self.description}"

class Budget:
    def __init__(self, savings: float):
        self.savings = savings

    def __add__(self, other):
        return Budget(self.savings + other)

    def __sub__(self, other):
        return Budget(self.savings - other)

    def __str__(self):
        return f"{self.savings:.2f} грн"

class Transaction:
    def __init__(self, category: Category, amount: float, date: datetime):
        self.category = category
        self.amount = amount
        self.date = date

    def __str__(self):
        return f"{self.category.name}: {self.amount} грн, дата: {self.date.strftime('%d.%m.%Y, %H:%M')}"

class User:
    def __init__(self, id: int, username: str, budget: Budget):
        self.id = id
        self.username = username
        self.budget = budget
        self.transactions = []

    def addTransaction(self, category: Category, amount: float):
        transaction = Transaction(category, amount, datetime.now())
        self.transactions.append(transaction)

        if category.name == 'Дохід':
            self.budget += abs(amount)
        else:
            if self.budget.savings >= abs(amount):
                self.budget -= abs(amount)
            else:
                print(f'Неможливо виконати транзакцію! Недостатньо коштів. {transaction.date.strftime("%d.%m.%Y, %H:%M")}, сума: {amount} грн')

    def showTransactions(self):
        print(f'\nТранзакції користувача {self.username}:')
        for transaction in self.transactions:
            print(transaction)

    def __str__(self):
        return f"ID: {self.id}, користувач: {self.username}, бюджет: {self.budget}"


def main():
    food = Category('Їжа', 'Оплата їжі в магазині')
    salary = Category('Дохід', 'Заробітна плата за місяць')
    phone = Category('Комунальні послуги', 'Оплата телефонного тарифу')

    categories = [food, salary, phone]
    users = []
    Daniil = User(1, 'Daniil', Budget(10000))
    Anfisa = User(2, 'Anfisa', Budget(15000))

    users.append(Daniil)
    users.append(Anfisa)

    Daniil.addTransaction(categories[0], -100)
    Daniil.addTransaction(categories[1], 10000)
    Daniil.addTransaction(categories[2], -280)

    Anfisa.addTransaction(categories[1], 12300)

    Daniil.showTransactions()
    Anfisa.showTransactions()

    print(Daniil)
    print(Anfisa)

    while True:

        print('\n1. Додати користувача\n2. Додати категорію\n3. Додати транзакцію\n4. Переглянути транзакції\n5. Вивести користувачів\n0. Вийти')
        choice = int(input('Оберіть опцію: '))
        match choice:
            case 1:
                userID = int(len(users) + 1)
                username = str(input('Введіть імʼя користувача: '))
                budget = float(input('Введіть бюджет: '))

                users.append(User(userID, username, Budget(budget)))

            case 2:
                category = str(input('Введіть назву категрії: '))
                description = str(input('Введіть опис: '))

                categories.append(Category(category, description))

            case 3:
                for i, user in enumerate(users):
                    print(f"{i + 1}. {user.username}")

                user_idx = int(input('Оберіть користувача (введіть номер): ')) - 1
                user = users[user_idx]

                for i, category in enumerate(categories):
                    print(f"{i + 1}. {category.name}")

                category_idx = int(input('Оберіть категорію (введіть номер): ')) - 1
                category = categories[category_idx]

                amount = float(input('Введіть суму транзакції (для витрат вкажіть мінус): '))
                user.addTransaction(category, amount)
                print(f'Транзакцію для {user.username} додано.')

            case 4:
                for i, user in enumerate(users):
                    print(f"{i + 1}. {user.username}")

                user_idx = int(input('Оберіть користувача (введіть номер): ')) - 1
                user = users[user_idx]

                if user.transactions:
                    user.showTransactions()
                else:
                    print(f'У користувача {user.username} немає транзакцій.')

            case 5:
                for i, user in enumerate(users):
                    print(f"{i + 1}. {user.username}, {user.budget}")
            case 0:
                print('Вихід із програми.')
                break

            case _:
                print('Помилка!')

if __name__ == '__main__':
    main()
