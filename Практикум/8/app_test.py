import customtkinter as ctk
from tkinter import messagebox
from typing import Union
from test8 import *
# Клас для транспорту

# Головний екран за допомогою customtkinter
class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Система паркування")
        self.geometry("600x400")

        # Кнопки на головному екрані
        self.option_button1 = ctk.CTkButton(self, text="Резервація місця", command=self.open_reservation_menu)
        self.option_button1.pack(pady=20)

        self.option_button2 = ctk.CTkButton(self, text="Зняття резервації", command=self.open_cancel_reservation_menu)
        self.option_button2.pack(pady=20)

        self.option_button3 = ctk.CTkButton(self, text="Перегляд паркінгу", command=self.open_parking_view)
        self.option_button3.pack(pady=20)

        self.vehicle = None  # Поточний транспортний засіб
        self.reservation = None  # Поточна бронь

    def open_reservation_menu(self):
        self.new_window = ctk.CTkToplevel(self)
        self.new_window.title("Вибір типу транспортного засобу")

        self.car_button = ctk.CTkButton(self.new_window, text="Машина", command=self.open_car_form)
        self.car_button.pack(pady=10)

        self.motorcycle_button = ctk.CTkButton(self.new_window, text="Мотоцикл", command=self.open_motorcycle_form)
        self.motorcycle_button.pack(pady=10)

        self.truck_button = ctk.CTkButton(self.new_window, text="Вантажівка", command=self.open_truck_form)
        self.truck_button.pack(pady=10)

    def open_car_form(self):
        self.new_window.destroy()  # Закриваємо попереднє вікно
        self.new_window = ctk.CTkToplevel(self)
        self.new_window.title("Резервація для машини")

        self.vehicle_type = "Car"
        self.create_vehicle_form()

    def open_motorcycle_form(self):
        self.new_window.destroy()  # Закриваємо попереднє вікно
        self.new_window = ctk.CTkToplevel(self)
        self.new_window.title("Резервація для мотоцикла")

        self.vehicle_type = "Motorcycle"
        self.create_vehicle_form()

    def open_truck_form(self):
        self.new_window.destroy()  # Закриваємо попереднє вікно
        self.new_window = ctk.CTkToplevel(self)
        self.new_window.title("Резервація для вантажівки")

        self.vehicle_type = "Truck"
        self.create_vehicle_form()

    def create_vehicle_form(self):
        # Створення полів для введення даних транспортного засобу
        self.name_label = ctk.CTkLabel(self.new_window, text="Назва:")
        self.name_label.pack(pady=10)
        self.name_entry = ctk.CTkEntry(self.new_window)
        self.name_entry.pack(pady=10)

        self.model_label = ctk.CTkLabel(self.new_window, text="Модель:")
        self.model_label.pack(pady=10)
        self.model_entry = ctk.CTkEntry(self.new_window)
        self.model_entry.pack(pady=10)

        self.plate_label = ctk.CTkLabel(self.new_window, text="Номер авто:")
        self.plate_label.pack(pady=10)
        self.plate_entry = ctk.CTkEntry(self.new_window)
        self.plate_entry.pack(pady=10)

        # Для машини
        # Для машини, вибір класу транспортного засобу
        if self.vehicle_type == "Car":
            self.vehicle_class_label = ctk.CTkLabel(self.new_window, text="Тип (Економ, Комфорт, Бізнес):")
            self.vehicle_class_label.pack(pady=10)
            self.vehicle_class_entry = ctk.CTkEntry(self.new_window)
            self.vehicle_class_entry.pack(pady=10)

        # Кнопка для бронювання
        self.reserve_button = ctk.CTkButton(self.new_window, text="Забронювати місце", command=self.make_reservation)
        self.reserve_button.pack(pady=20)

    def make_reservation(self):
        name = self.name_entry.get()
        model = self.model_entry.get()
        plate = self.plate_entry.get()

        if self.vehicle_type == "Car":
            vehicle_class = self.vehicle_class_entry.get()
            self.vehicle = Car(plate, name, model, vehicle_class)
        elif self.vehicle_type == "Motorcycle":
            self.vehicle = Motorcycle(plate, name, model)
        elif self.vehicle_type == "Truck":
            self.vehicle = Truck(plate, name, model)

        # Перевірка на вибір місця (автоматично або вручну)
        self.choose_spot_window()

    def choose_spot_window(self):
        self.new_window.destroy()
        self.new_window = ctk.CTkToplevel(self)
        self.new_window.title("Вибір місця для паркування")

        self.automatic_button = ctk.CTkButton(self.new_window, text="Автоматичний вибір місця",
                                              command=self.automatic_reservation)
        self.automatic_button.pack(pady=10)

        self.manual_button = ctk.CTkButton(self.new_window, text="Вибір місця вручну", command=self.manual_reservation)
        self.manual_button.pack(pady=10)

    def automatic_reservation(self):
        # Автоматична бронь
        messagebox.showinfo("Успішно", "Місце заброньовано автоматично!")
        self.reservation = Reservation(self.vehicle, parking_C, 3)  # Автоматичне бронювання на 3 години
        self.reservation.make_reservation()

    def manual_reservation(self):
        # Ручний вибір місця
        self.new_window.destroy()
        self.new_window = ctk.CTkToplevel(self)
        self.new_window.title("Вибір місця")

        self.spot_number_label = ctk.CTkLabel(self.new_window, text="Введіть номер місця:")
        self.spot_number_label.pack(pady=10)
        self.spot_number_entry = ctk.CTkEntry(self.new_window)
        self.spot_number_entry.pack(pady=10)

        self.confirm_button = ctk.CTkButton(self.new_window, text="Підтвердити",
                                            command=self.confirm_manual_reservation)
        self.confirm_button.pack(pady=20)

    def confirm_manual_reservation(self):
        spot_number = int(self.spot_number_entry.get())
        self.reservation = Reservation(self.vehicle, parking_C, 3, spot_number=spot_number)
        self.reservation.make_reservation()

    def open_parking_view(self):
        self.new_window = ctk.CTkToplevel(self)
        self.new_window.title("Перегляд паркінгу")

        # Список паркувальних місць
        for spot in parking_C.spots:
            spot_label = ctk.CTkLabel(self.new_window, text=str(spot))
            spot_label.pack()

    def open_cancel_reservation_menu(self):
        self.new_window = ctk.CTkToplevel(self)
        self.new_window.title("Скасування бронювання")

        # Скасування бронювання для вибраного автомобіля
        self.cancel_button = ctk.CTkButton(self.new_window, text="Скасувати бронювання",
                                           command=self.cancel_reservation)
        self.cancel_button.pack(pady=20)

    def cancel_reservation(self):
        if self.reservation:
            self.reservation.cancel_reservation()
            messagebox.showinfo("Успішно", "Бронювання скасовано!")
        else:
            messagebox.showerror("Помилка", "Немає активного бронювання!")

if __name__ == "__main__":
    audi = Car('ABC123', 'Audi', 'A4', 'Комфорт')
    harley = Motorcycle('XYZ987', 'Harley', 'Sportster')
    bentley = Car('123123', 'Bentley', 'Continental', 'Бізнес')

    parking_C = Parking("1", 10)

    # Бронювання для Audi
    reservation_audi = Reservation(audi, parking_C, 3, 5)
    print(reservation_audi.make_reservation())
    transaction_audi = Transaction(reservation_audi)
    print(transaction_audi.transaction_output())

    # Бронювання для Harley
    reservation_harley = Reservation(harley, parking_C, 3)
    print(reservation_harley.make_reservation())
    transaction_harley = Transaction(reservation_harley)
    print(transaction_harley.transaction_output())

    # Виведення інформації про всі місця
    print(parking_C)

    # Скасування бронювання для Audi
    print(reservation_audi.cancel_reservation())
    print(parking_C)

    app = Application()
    app.mainloop()
