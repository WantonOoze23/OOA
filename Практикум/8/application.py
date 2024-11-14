import customtkinter
from manager import *


class Application(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

if __name__ == '__main__':
    if __name__ == "__main__":
        # Створюємо об'єкти
        parking = Parking("Main Parking", 10)
        car = Car("Toyota", "Camry", "AA1234BB", "+380501234567", 1,2, "Бізнес")

        # Менеджер паркування
        manager = Manager(vehicle=car, parking=parking)

        # Пошук місця
        manager.find_spot()

        # Підрахунок оплати
        print(f"Payment: {manager.payment()} UAH")

        # Збереження даних
        manager.save_data()
        print("Data saved to CSV.")