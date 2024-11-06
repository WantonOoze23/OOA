from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def notify(self, message: str) -> None:
        pass

class EmailNotifier(Notifier):
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def notify(self, message: str) -> None:
        print(f"{self.name}, {message}")

class SMSNotifier(Notifier):
    def __init__(self, name: str, number: str):
        self.name = name
        self.number = number

    def notify(self, message: str) -> None:
        print(f"{self.name}, {message}")

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
        return ', '.join([notifier.name for notifier in self.notifiers])

def main():
    Daniil = EmailNotifier("Daniil","example@gmail.com")
    Alex = SMSNotifier("Alex","+380951234567")

    manager = NotificationManager()

    manager.add_notifier(Daniil)
    manager.add_notifier(Alex)

    manager.notify_all("Test message")

    Daniil.notify('hello world')

    print('Наявні отримувачі:', manager)
if __name__ == '__main__':
    main()