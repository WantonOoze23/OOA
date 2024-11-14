import customtkinter as ctk
from tkinter import messagebox


from test8 import *

# Головний екран
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
        self.new_window.geometry("300x200")

        # Вибір типу транспортного засобу
        vehicle_buttons = [
            ("Машина", self.open_car_form),
            ("Мотоцикл", self.open_motorcycle_form),
            ("Вантажівка", self.open_truck_form)
        ]

        for text, command in vehicle_buttons:
            ctk.CTkButton(self.new_window, text=text, command=command).pack(pady=10)

    def open_car_form(self):
        self.vehicle_type = "Car"
        self.create_vehicle_form()

    def open_motorcycle_form(self):
        self.vehicle_type = "Motorcycle"
        self.create_vehicle_form()

    def open_truck_form(self):
        self.vehicle_type = "Truck"
        self.create_vehicle_form()

    def create_vehicle_form(self):
        if hasattr(self, 'new_window'):
            self.new_window.destroy()

        self.new_window = ctk.CTkToplevel(self)
        self.new_window.title("Форма для транспортного засобу")
        self.new_window.geometry("400x400")

        self.name_label = ctk.CTkLabel(self.new_window, text="Назва:")
        self.name_label.pack(pady=5)
        self.name_entry = ctk.CTkEntry(self.new_window)
        self.name_entry.pack(pady=5)

        self.model_label = ctk.CTkLabel(self.new_window, text="Модель:")
        self.model_label.pack(pady=5)
        self.model_entry = ctk.CTkEntry(self.new_window)
        self.model_entry.pack(pady=5)

        self.plate_label = ctk.CTkLabel(self.new_window, text="Номер авто:")
        self.plate_label.pack(pady=5)
        self.plate_entry = ctk.CTkEntry(self.new_window)
        self.plate_entry.pack(pady=5)

        if self.vehicle_type == "Car":
            self.vehicle_class_label = ctk.CTkLabel(self.new_window, text="Клас авто:")
            self.vehicle_class_label.pack(pady=10)

            self.vehicle_class = ctk.StringVar(value="Економ")

            for vehicle_class in ["Економ", "Комфорт", "Бізнес"]:
                ctk.CTkRadioButton(self.new_window, text=vehicle_class, variable=self.vehicle_class,
                                   value=vehicle_class).pack(pady=5)

        self.reserve_button = ctk.CTkButton(self.new_window, text="Забронювати місце", command=self.make_reservation)
        self.reserve_button.pack(pady=20)

    def make_reservation(self):
        name = self.name_entry.get()
        model = self.model_entry.get()
        plate_number = self.plate_entry.get()

        if not name or not model or not plate_number:
            messagebox.showerror("Помилка", "Будь ласка, заповніть усі поля!")
            return

        if self.vehicle_type == "Car":
            vehicle_class = self.vehicle_class.get()
            self.vehicle = Car(plate_number, name, model, vehicle_class)
        elif self.vehicle_type == "Motorcycle":
            self.vehicle = Motorcycle(plate_number, name, model)
        elif self.vehicle_type == "Truck":
            self.vehicle = Truck(plate_number, name, model)

        self.reservation = Reservation(self.vehicle, parking_C, hours=2)
        result = self.reservation.make_reservation()

        if "успішне" in result:
            messagebox.showinfo("Успіх", result)
        else:
            messagebox.showerror("Помилка", result)

        self.new_window.destroy()

    def open_parking_view(self):
        self.new_window = ctk.CTkToplevel(self)
        self.new_window.title("Перегляд паркінгу")

        for spot in parking_C.spots:
            spot_label = ctk.CTkLabel(self.new_window, text=str(spot))
            spot_label.pack()

    def open_cancel_reservation_menu(self):
        self.new_window = ctk.CTkToplevel(self)
        self.new_window.title("Скасування бронювання")
        self.new_window.geometry("400x300")

        self.vehicle_list = ctk.CTkComboBox(self.new_window, values=self.get_reserved_vehicles())
        self.vehicle_list.pack(pady=10)

        self.cancel_button = ctk.CTkButton(self.new_window, text="Скасувати бронювання", command=self.cancel_reservation)
        self.cancel_button.pack(pady=20)

    def get_reserved_vehicles(self):
        return [f"{spot.vehicle.name} {spot.vehicle.model} ({spot.vehicle._plate_number})"
                for spot in parking_C.spots if spot.is_occupied]

    def cancel_reservation(self):
        selected_vehicle = self.vehicle_list.get()

        if not selected_vehicle:
            messagebox.showerror("Помилка", "Будь ласка, оберіть транспортний засіб для скасування!")
            return

        for spot in parking_C.spots:
            if spot.is_occupied and spot.vehicle:
                vehicle_info = f"{spot.vehicle.name} {spot.vehicle.model} ({spot.vehicle._plate_number})"
                if vehicle_info == selected_vehicle:
                    spot.release()
                    messagebox.showinfo("Успіх", f"Бронювання для {vehicle_info} скасовано!")
                    self.vehicle_list.configure(values=self.get_reserved_vehicles())
                    return

        messagebox.showerror("Помилка", "Не вдалося знайти вибраний транспортний засіб!")

if __name__ == "__main__":
    audi = Car('ABC123', 'Audi', 'A4', 'Комфорт')
    harley = Motorcycle('XYZ987', 'Harley', 'Sportster')
    bentley = Car('123123', 'Bentley', 'Continental', 'Бізнес')
    bmw = Car('51QWe1', 'BMW', "I8", "Бізнес")

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

    reservation_bmw = Reservation(bmw, parking_C, 5)
    print(reservation_bmw.make_reservation())
    transaction_bmw = Transaction(reservation_bmw)
    print(transaction_bmw.transaction_output())

    reservation_bentley = Reservation(bentley, parking_C, 5)
    print(reservation_bentley.make_reservation())
    transaction_bentley = Transaction(reservation_bentley)
    print(transaction_bentley.transaction_output())


    # Виведення інформації про всі місця
    print(parking_C)


    app = Application()
    app.mainloop()
