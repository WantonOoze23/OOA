#"ОЩАДБАНК": створіть класи для транзакцій, бюджетів і категорій, дозволяючи користувачам відстежувати доходи та витрати.
from datetime import datetime
from typing import List

class Category:
    def __init__(self, name):
        self.name = name

class Transaction:
    def __init__(self, amount: float, category: Category, description: str, date: datetime = None):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date if date else datetime.now()

    def __repr__(self):
        return f"{self.date.strftime('%d.%m.%Y')} - {self.description}: {self.amount} UAH in {self.category.name}"

class Budget:
    def __init__(self, name: str, totalBudget: float):
        self.name = name
        self.totalBudget = totalBudget
        self.transactions: List[Transaction] = []

    def addTransaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def totalSpent(self):
        return self.totalBudget * len(self.transactions)

    def remainingBudget(self):
        return self.totalBudget - self.totalSpent()

    def __repr__(self):
        return (f"Budget: {self.name}\n"
                f"Total Budget: {self.totalBudget} UAH\n"
                f"Total Spent: {self.totalSpent()} UAH\n"
                f"Remaining Budget: {self.remainingBudget()} UAH")


def menu():
    print("\n--- ОЩАДБАНК МЕНЮ ---")
    print("1. Додати категорію")
    print("2. Додати транзакцію")
    print("3. Показати всі транзакції")
    print("4. Показати бюджет")
    print("0. Вийти")


def addCategory(categories: List[Category]):
    name = input("Введіть назву категорії: ")
    categories.append(Category(name))
    print(f"Категорію '{name}' додано.")


def addTransaction(budget: Budget, categories: List[Category]):
    if not categories:
        print("Немає категорій. Спочатку додайте категорію.")
        return

    amount = float(input("Введіть суму транзакції (від'ємна для витрат): "))
    description = input("Введіть опис транзакції: ")

    print("Оберіть категорію:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category.name}")
    category_index = int(input("Введіть номер категорії: ")) - 1

    if 0 <= category_index < len(categories):
        category = categories[category_index]
        transaction = Transaction(amount, category, description)
        budget.addTransaction(transaction)
        print("Транзакцію додано.")
    else:
        print("Неправильний вибір категорії.")


def showTransactions(budget: Budget):
    if not budget.transactions:
        print("Транзакцій немає.")
    else:
        for transaction in budget.transactions:
            print(transaction)


def showBudget(budget: Budget):
    print(budget)

def main():
    categories = []
    budget_name = input("Введіть ім'я бюджету: ")
    total_budget = float(input("Введіть загальний бюджет: "))
    budget = Budget(budget_name, total_budget)

    while True:
        menu()
        choice = input("Введіть номер опції: ")

        if choice == '1':
            addCategory(categories)
        elif choice == '2':
            addTransaction(budget, categories)
        elif choice == '3':
            showTransactions(budget)
        elif choice == '4':
            showBudget(budget)
        elif choice == '0':
            print("Вихід з програми.")
            break
        else:
            print("Неправильний вибір. Спробуйте ще раз.")


if __name__ == '__main__':
    main()