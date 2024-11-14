from datetime import datetime
import pandas as pd
from typing import Union

from vehicle import Car, Motorcycle, Truck
from parking import Parking

class Manager:
    def __init__(self, vehicle: Union[Car, Motorcycle, Truck], parking: Parking):
        self.vehicle = vehicle
        self.parking = parking
        self.Data = pd.DataFrame(columns=['Name', 'Model', 'Plate Number', 'Phone Number', 'Parking Spot', 'Hours', 'Class', 'Time'])

    def save_data(self, filename: str = "parking_lots.csv"):
        self.Data.to_csv(filename, index=False)

    def load_data(self, filename: str = "parking_lots.csv"):
        self.Data = pd.read_csv(filename)

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

    def find_spot(self):
        spot = self.parking.assign_spot(self.vehicle)
        if spot:
            print(f"Assigned spot {spot} for vehicle {self.vehicle}")
            self.vehicle.parking_spot = spot
            # Додавання інформації у DataFrame
            self.Data = pd.concat([self.Data, pd.DataFrame({
                'Name': [self.vehicle.name],
                'Model': [self.vehicle.model],
                'Plate Number': [self.vehicle.plate_number],
                'Phone Number': [self.vehicle.phone_number],
                'Parking Spot': [spot],
                'Hours': [self.vehicle.hours],
                'Class': [getattr(self.vehicle, 'car_class', 'N/A')],
                'Time': [self.vehicle.time_beginning]
            })], ignore_index=True)
        else:
            print("No available parking spots.")

    def release_spot(self):
        self.parking.release_spot(self.vehicle.parking_spot)
        print(f"Released spot {self.vehicle.parking_spot} for vehicle {self.vehicle}")