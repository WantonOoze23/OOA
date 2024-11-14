from typing import Union
import pandas as pd

class Vehicle:
    def __init__(self, plate_number: str, name: str, model: str, vehicle_class: str = None):
        self.plate_number = plate_number
        self.name = name
        self.model = model
        self.vehicle_class = vehicle_class

    def __str__(self):
        return f'{self.plate_number} {self.name} {self.model}'

    def calculate_fee(self, hours: int) -> float:
        """Base fee calculation"""
        return hours * 30  # Default base fee for unknown vehicles


class Car(Vehicle):
    def __init__(self, plate_number: str, name: str, model: str, vehicle_class: str):
        super().__init__(plate_number, name, model, vehicle_class)

    def calculate_fee(self, hours: int) -> float:
        """Override for specific class-based fee"""
        fee_mapping = {
            'Економ': 25,
            'Комфорт': 50,
            'Бізнес': 100
        }
        return hours * fee_mapping.get(self.vehicle_class, 30)  # Default to 30 if class not found


class Motorcycle(Vehicle):
    def __init__(self, plate_number: str, name: str, model: str):
        super().__init__(plate_number, name, model)

    def calculate_fee(self, hours: int) -> float:
        return hours * 20


class Truck(Vehicle):
    def __init__(self, plate_number: str, name: str, model: str):
        super().__init__(plate_number, name, model)

    def calculate_fee(self, hours: int) -> float:
        return hours * 150


class ParkingSpot:
    def __init__(self, number: int, vehicle: Union[Car, Motorcycle, Truck] = None, is_occupied: bool = False):
        self.number = number
        self.vehicle = vehicle
        self.is_occupied = is_occupied

    def occupy(self, vehicle: Union[Car, Motorcycle, Truck]) -> str:
        if self.is_occupied:
            return f"Місце {self.number} вже зайняте"
        self.vehicle = vehicle
        self.is_occupied = True
        return f"Місце {self.number} зайняте для {vehicle.name} {vehicle.model}"

    def release(self) -> str:
        if not self.is_occupied:
            return f"Місце {self.number} вже вільне"
        self.is_occupied = False
        self.vehicle = None
        return f"Місце {self.number} звільнено"

    def save_parking_spot(self, filename: str = "parking_spot.csv") -> None:
        data = {
            "Plate Number": [self.vehicle.plate_number if self.vehicle else None],
            "Vehicle": [self.vehicle.name if self.vehicle else None],
            "Model": [self.vehicle.model if self.vehicle else None],
            "Spot Number": [self.number],
            "Is Occupied": [self.is_occupied]
        }
        df = pd.DataFrame(data)
        df.to_csv(filename, mode='a', header=False, index=False)

    def load_parking_spot(self, filename: str = "parking_spot.csv") -> None:
        try:
            data = pd.read_csv(filename)
            spot_data = data.loc[data["Spot Number"] == self.number]
            if not spot_data.empty:
                self.is_occupied = spot_data["Is Occupied"].iloc[0]
        except FileNotFoundError:
            pass

    def __str__(self) -> str:
        return f"Місце {self.number}: {'Зайнято' if self.is_occupied else 'Вільне'}"


class Parking:
    def __init__(self, floor: str, amount: int):
        self.floor = floor
        self.spots = [ParkingSpot(i + 1) for i in range(amount)]

    def find_free_spot(self) -> Union[ParkingSpot, None]:
        return next((spot for spot in self.spots if not spot.is_occupied), None)

    def find_spot_by_number(self, spot_number: int) -> Union[ParkingSpot, None]:
        return self.spots[spot_number - 1] if 0 < spot_number <= len(self.spots) else None

    def __str__(self) -> str:
        return "\n".join([str(spot) for spot in self.spots])


class Reservation:
    def __init__(self, vehicle: Union[Car, Motorcycle, Truck], parking: Parking, hours: int, spot_number: int = None):
        self.vehicle = vehicle
        self.parking = parking
        self.hours = hours
        self.spot_number = spot_number

    def make_reservation(self) -> str:
        if self.spot_number:
            spot = self.parking.find_spot_by_number(self.spot_number)
            if spot and not spot.is_occupied:
                spot.occupy(self.vehicle)
                return f"Бронювання успішне для {self.vehicle.name} {self.vehicle.model} на місце {spot.number}"
            else:
                return f"Місце {self.spot_number} недоступне"
        else:
            free_spot = self.parking.find_free_spot()
            if free_spot is None:
                return "Немає вільних місць"
            self.spot_number = free_spot.number
            free_spot.occupy(self.vehicle)
            return f"Бронювання успішне для {self.vehicle.name} {self.vehicle.model} на місце {self.spot_number}"

    def cancel_reservation(self) -> str:
        if self.spot_number is None:
            return "Бронювання не знайдено"
        spot = self.parking.find_spot_by_number(self.spot_number)
        spot.release()
        self.spot_number = None
        return f"Бронювання для {self.vehicle.name} {self.vehicle.model} скасовано"

    def calculate_fee(self) -> float:
        return self.vehicle.calculate_fee(self.hours)


class Transaction:
    def __init__(self, reservation: Reservation):
        self.reservation = reservation
        self.amount_to_pay = 0

    def process_payment(self) -> float:
        self.amount_to_pay = self.reservation.calculate_fee()
        return self.amount_to_pay

    def get_transaction_info(self) -> dict:
        return {
            "Vehicle": str(self.reservation.vehicle),
            "Spot Number": self.reservation.spot_number,
            "Amount to Pay": self.amount_to_pay
        }

    def transaction_output(self, filename: str = "transactions.csv") -> str:
        self.process_payment()
        data = {
            "Vehicle": [str(self.reservation.vehicle)],
            "Class": [str(self.reservation.vehicle.vehicle_class)],
            "Spot Number": [self.reservation.spot_number],
            "Hours": [self.reservation.hours],
            "Amount to Pay": [self.amount_to_pay]
        }
        df = pd.DataFrame(data)
        df.to_csv(filename, mode='a', header=False, index=False)
        return f"Транзакція для {self.reservation.vehicle.name}: Сума до сплати {self.amount_to_pay} грн"
