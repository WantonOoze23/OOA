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
        self.transactions = pd.DataFrame(columns=['category', 'amount', 'date'])

    def addTransaction(self, category: Category, amount: float, users):
        transaction = Transaction(category, amount, datetime.now())

        # Створюємо новий рядок як DataFrame для додавання
        new_transaction = pd.DataFrame([{
            'category': category.name,
            'amount': amount,
            'date': transaction.date.strftime('%d.%m.%Y, %H:%M')
        }])

        # Додаємо перевірку, щоб уникнути попередження
        if not new_transaction.empty:
            self.transactions = pd.concat([self.transactions, new_transaction], ignore_index=True)

        if category.name == 'Дохід' or amount > 0:
            self.budget += abs(amount)

        elif category.name == 'Переказ':
            for i, user in enumerate(users):
                print(f"{i + 1}. {user.username}")
            try:
                recipientID = int(input('Введіть ID отримувача: '))
            except ValueError:
                print("Будь ласка, введіть дійсний ID.")
                return

            if recipientID == self.id:
                print('Неможливо вибрати самого себе')
                return
            else:
                recipient = next((user for user in users if user.id == recipientID), None)

                if recipient:
                    if self.budget.savings >= abs(amount):
                        self.budget -= abs(amount)
                        recipient.budget += abs(amount)

                        # Додаємо транзакцію переказу до обох користувачів без рекурсивного виклику
                        self.transactions = pd.concat([self.transactions, pd.DataFrame([{
                            'category': "Переказ",
                            'amount': -abs(amount),
                            'date': transaction.date.strftime('%d.%m.%Y, %H:%M')
                        }])], ignore_index=True)

                        recipient.transactions = pd.concat([recipient.transactions, pd.DataFrame([{
                            'category': "Переказ",
                            'amount': abs(amount),
                            'date': transaction.date.strftime('%d.%m.%Y, %H:%M')
                        }])], ignore_index=True)

                        print(f'Пересилання {amount} грн користувачу {recipient.username} успішно виконано.')
                    else:
                        print(f'Недостатньо коштів для переказу {amount} грн.')
                else:
                    print(f'Користувач з імʼям {recipientID} не знайдений.')

        else:
            if self.budget.savings >= abs(amount):
                self.budget -= abs(amount)
            else:
                print(
                    f'Неможливо виконати транзакцію! Недостатньо коштів. {transaction.date.strftime("%d.%m.%Y, %H:%M")}, сума: {amount} грн')

    def showTransactions(self):
        print(f'\nТранзакції користувача {self.username}:')
        print(self.transactions)

    def saveTransactions(self):
        self.transactions.to_csv(f'transactions_{self.username}.csv', index=False)

    def loadTransactions(self):
        try:
            self.transactions = pd.read_csv(f'transactions_{self.username}.csv')
            return self.transactions
        except FileNotFoundError:
            print('Файл не знайдено')

    def __str__(self):
        return f"ID: {self.id}, користувач: {self.username}, бюджет: {self.budget}"

def saveUsers(users):
    usersData = pd.DataFrame({
        'id': [user.id for user in users],
        'username': [user.username for user in users],
        'budget': [user.budget.savings for user in users]
    })

    usersData.to_csv('users.csv', index=False)
    print("Дані користувачів збережено у файл.")

def loadUsers():
    usersData = pd.read_csv('users.csv')
    users = []
    for index, row in usersData.iterrows():
        users.append(User(int(row['id']), row['username'], Budget(float(row['budget']))))
    return users

def saveCategories(categories):
    categoriesData = pd.DataFrame({
        'Name': [category.name for category in categories],
        'Description': [category.description for category in categories],
    })
    categoriesData.to_csv('categories.csv', index=False)
    print("Категорії збережено у файл.")

def loadCategories():
    try:
        categoriesData = pd.read_csv('categories.csv')
        categories = []
        for index, row in categoriesData.iterrows():
            categories.append(Category(row['Name'], row['Description']))
        return categories
    except FileNotFoundError:
        print("Файл категорій не знайдено. Створюємо новий список категорій.")
        return []

def addCategory(categories):
    categoryName = input('Введіть назву категорії: ')
    if any(category.name == categoryName for category in categories):
        print(f'Категорія \"{categoryName}\" вже існує.')
    else:
        description = input('Введіть опис: ')
        newCategory = Category(categoryName, description)
        categories.append(newCategory)
        print(f"Категорія \"{categoryName}\" додана.")
        saveCategories(categories)


def main():
    users = []
    categories = loadCategories()

    try:
        users = loadUsers()
        print("Користувачі завантажені.")
    except FileNotFoundError:
        print("Файл користувачів не знайдено. Створюємо новий список.")

    for user in users:
        user.loadTransactions()


    while True:
        print(
            '\n1. Додати користувача\n2. Додати категорію\n3. Додати транзакцію\n4. Переглянути транзакції\n5. Вивести користувачів\n0. Вийти')
        try:
            choice = int(input('Оберіть опцію: '))
        except ValueError:
            print('Повторіть спробу ще раз!')
            continue

        match choice:
            case 1:
                userID = len(users) + 1
                username = str(input('Введіть імʼя користувача: '))
                if username == 'cancel':
                    continue
                try:
                    budget = float(input('Введіть бюджет: '))
                except ValueError:
                    print('Невірно введений бюджет')

                users.append(User(userID, username, Budget(budget)))

            case 2:
                addCategory(categories)

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
                user.addTransaction(category, amount, users)
                print(f'Транзакцію для {user.username} додано.')

            case 4:
                for i, user in enumerate(users):
                    print(f"{i + 1}. {user.username}")

                user_idx = int(input('Оберіть користувача (введіть номер): ')) - 1
                user = users[user_idx]

                if not user.transactions.empty:
                    user.showTransactions()
                else:
                    print(f'У користувача {user.username} немає транзакцій.')

            case 5:
                for user in users:
                    print(f"{user.username}, бюджет: {user.budget}")

            case 0:
                print('Вихід із програми.')
                saveUsers(users)
                for user in users:
                    user.saveTransactions()
                print("Транзакції збережено у файл.")
                break

            case _:
                print('Помилка! Невірна опція.')


if __name__ == '__main__':
    main()
