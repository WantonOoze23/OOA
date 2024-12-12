import pandas as pd
from typing import Union

from .vehicle import Car, Motorcycle, Truck
from .parking import Parking

class Manager:
    def __init__(self, vehicle: Union[Car, Motorcycle, Truck], parking: Parking):
        self.vehicle = vehicle
        self.parking = parking
        self.Data = pd.DataFrame(columns=['Name', 'Model', 'Plate Number', 'Phone Number', 'Parking Spot', 'Hours', 'Class', 'Time', 'Total Payment'])

    # Зберігання даних в CSV файл
    def save_to_csv(self, filename: str = "parking_lots.csv"):
        self.Data.to_csv(filename, index=False)

    # Завантаження даних з CSV файлу
    def load_from_csv(self, filename: str = "parking_lots.csv"):
        try:
            self.Data = pd.read_csv(filename)
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with empty data.")
            self.Data = pd.DataFrame(columns=['Name', 'Model', 'Plate Number', 'Phone Number', 'Parking Spot', 'Hours', 'Class', 'Time', 'Total Payment'])

    # Метод для розрахунку вартості
    def payment(self):
        match self.vehicle.car_class:
            case "Економ":
                return self.vehicle.hours * 100
            case "Стандарт":
                return self.vehicle.hours * 120
            case "Комфорт":
                return self.vehicle.hours * 150
            case "Бізнес":
                return self.vehicle.hours * 200
            case _:
                return self.vehicle.hours * 120

    # Спеціальний розрахунок вартості для мотоциклів і траків
    def TMCPayment(self):
        if isinstance(self.vehicle, Motorcycle):
            return self.vehicle.hours * 100  # ціна для мотоциклів
        elif isinstance(self.vehicle, Truck):
            return self.vehicle.hours * 200  # ціна для траків
        else:
            return self.payment()

    # Знаходження місця для транспортного засобу
    def find_spot(self):
        spot = self.parking.assign_spot(self.vehicle)
        if spot:
            print(f"Assigned spot {spot} for vehicle {self.vehicle}")
            self.vehicle.parking_spot = spot
            # Розраховуємо суму оплати
            total_payment = self.TMCPayment()

            # Додавання інформації у DataFrame
            self.Data = pd.concat([self.Data, pd.DataFrame({
                'Name': [self.vehicle.name],
                'Model': [self.vehicle.model],
                'Plate Number': [self.vehicle.plate_number],
                'Phone Number': [self.vehicle.phone_number],
                'Parking Spot': [spot],
                'Hours': [self.vehicle.hours],
                'Class': [getattr(self.vehicle, 'car_class', 'N/A')],
                'Time': [self.vehicle.time_beginning],
                'Total Payment': [total_payment]  # Додаємо суму оплати
            })], ignore_index=True)
        else:
            print("No available parking spots.")

    # Вивільнення місця на парковці
    def release_spot(self):
        self.parking.release_spot(self.vehicle.parking_spot)
        print(f"Released spot {self.vehicle.parking_spot} for vehicle {self.vehicle}")
