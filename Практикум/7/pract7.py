from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def notify(self, message: str) -> None:
        pass
    @abstractmethod
    def methodname(self):
        pass

class EmailNotifier(Notifier):
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def notify(self, message: str) -> None:
        print(f"{self.name}, {message}")

    def methodname(self):
        return 'EMAIL'

class SMSNotifier(Notifier):
    def __init__(self, name: str, number: str):
        self.name = name
        self.number = number

    def notify(self, message: str) -> None:
        print(f"{self.name}, {message}")

    def methodname(self):
        return 'SMS'

class NotificationManager():
    def __init__(self):
        self.notifiers = []

    def add_notifier(self, notifier: Notifier):
        self.notifiers.append(notifier)

    def notify_all(self, message: str) -> None:
        for notifier in self.notifiers:
            notifier.notify(message)

    def remove_notifier(self, notifier: Notifier):
        self.notifiers.remove(notifier)

    def __str__(self):
        return ''.join([f'\n{notifier.name} - {notifier.methodname()}' for notifier in self.notifiers])

def display_menu():
    print("\nМеню:")
    print("1. Додати Email отримувача")
    print("2. Додати SMS отримувача")
    print("3. Відправити повідомлення всім отримувачам")
    print("4. Видалити отримувача")
    print("5. Показати наявних отримувачів")
    print("6. Додати повідомлення ")
    print("0. Вихід")

def main():
    Daniil = EmailNotifier("Daniil","example@gmail.com")
    Alex = SMSNotifier("Alex","+380951234567")

    manager = NotificationManager()

    manager.add_notifier(Daniil)
    manager.add_notifier(Alex)

    manager.notify_all("Test message")

    Daniil.notify('hello world')

    print('Наявні отримувачі:', manager)

    while True:
        try:
            display_menu()
            choice = int(input("Оберіть опцію: "))

            match choice:
                case 1:
                    name = input("Введіть ім'я отримувача: ")
                    email = input("Введіть email: ")
                    notifier = EmailNotifier(name, email)
                    manager.add_notifier(notifier)
                    print(f"Email отримувач {name} доданий.")

                case 2:
                    name = input("Введіть ім'я отримувача: ")
                    number = input("Введіть номер телефону: ")
                    notifier = SMSNotifier(name, number)
                    manager.add_notifier(notifier)
                    print(f"SMS отримувач {name} доданий.")
                case 3:
                    message = input("Введіть повідомлення: ")
                    manager.notify_all(message)
                case 4:
                    name = input("Оберіть отримувача для видалення: ")
                    notifier_to_remove = None
                    for notifier in manager.notifiers:
                        if notifier.name == name:
                            notifier_to_remove = notifier
                            break
                    if notifier_to_remove:
                        manager.remove_notifier(notifier_to_remove)
                        print(f"Отримувач {name} видалений.")
                    else:
                        print(f"Отримувач з ім'ям {name} не знайдений.")

                case 5:
                    print("Наявні отримувачі:")
                    print(manager)

                case 6:
                    print("Наявні отримувачі:")
                    for i, notifier in enumerate(manager.notifiers, start=1):
                        print(
                            f"{i}. {notifier.name} ({notifier.methodname()})")

                    try:
                        choice = int(input("Введіть номер отримувача для відправлення повідомлення: "))
                        if 1 <= choice <= len(manager.notifiers):
                            selected_notifier = manager.notifiers[choice - 1]

                            message = input("Введіть повідомлення: ")
                            selected_notifier.notify(message)
                            print(f"Повідомлення відправлено {selected_notifier.name}: {message}")
                        else:
                            print("Невірний номер отримувача.")
                    except ValueError:
                        print("Будь ласка, введіть коректний номер.")


                case 0:
                    print("Вихід з програми.")
                    break

                case _:
                    print("Невірний вибір. Спробуйте знову.")
        except ValueError:
            print('Некоректний вибір. Спробуйте ще раз.')


if __name__ == '__main__':
    main()