#Створити інформаційно-пошукову систему роботи автостоянки.
from typing import Union

class Vehicle:
    def __init__(self, plate_number, name, model, vehicle_class: str = None):
        self._plate_number = plate_number
        self.name = name
        self.model = model
        self.vehicle_class = vehicle_class

    def __str__(self):
        return f'{self._plate_number} {self.name} {self.model}'


class Car(Vehicle):
    def __init__(self, plate_number, name, model, vehicle_class: str):
        super().__init__(plate_number, name, model, vehicle_class)

    def calculate_fee(self, hours):
        match self.vehicle_class:
            case 'Економ':
                return hours * 25
            case 'Комфорт':
                return hours * 50
            case 'Бізнес':
                return hours * 100
            case _:
                return hours * 25

class Motorcycle(Vehicle):
    def __init__(self, plate_number, name, model):
        super().__init__(plate_number, name, model)

    def calculate_fee(self, hours):
        return hours * 20

class Truck(Vehicle):
    def __init__(self, plate_number, name, model):
        super().__init__(plate_number, name, model)

    def calculate_fee(self, hours):
        return hours * 150


class ParkingSpot:
    def __init__(self, number: int, vehicle: Union[Car, Motorcycle, Truck] = None, is_occupied=False):
        self.number = number
        self.vehicle = vehicle
        self.is_occupied = is_occupied

    def occupy(self, vehicle: Union[Car, Motorcycle, Truck]):
        if self.is_occupied:
            return f"Місце {self.number} вже зайняте"
        self.vehicle = vehicle
        self.is_occupied = True
        return f"Місце {self.number} зайняте для {vehicle.name} {vehicle.model}"

    def release(self):
        if not self.is_occupied:
            return f"Місце {self.number} вже вільне"
        self.is_occupied = False
        self.vehicle = None
        return f"Місце {self.number} звільнено"

    def __str__(self):
        return f"Місце {self.number}: {f'Зайнято {self.vehicle.name} {self.vehicle.model}' if self.is_occupied else 'Вільне'}"


class Parking:
    def __init__(self, floor: str, amount: int):
        self.floor = floor
        self.amount = amount
        self.spots = [ParkingSpot(i + 1) for i in range(amount)]

    def find_free_spot(self):
        for spot in self.spots:
            if not spot.is_occupied:
                return spot
        return None  # Якщо місця немає

    def __str__(self):
        return "\n".join([str(spot) for spot in self.spots])


class Reservation:
    def __init__(self, vehicle: Union[Car, Motorcycle, Truck], parking: Parking, hours: int):
        self.vehicle = vehicle
        self.parking = parking
        self.hours = hours
        self.spot_number = None

    def make_reservation(self):
        free_spot = self.parking.find_free_spot()
        if free_spot is None:
            return "Немає вільних місць"
        self.spot_number = free_spot.number
        free_spot.occupy(self.vehicle)
        return f"Бронювання успішне для {self.vehicle.name} {self.vehicle.model} на місце {self.spot_number}"

    def cancel_reservation(self):
        if self.spot_number is None:
            return "Бронювання не знайдено"
        spot = self.parking.spots[self.spot_number - 1]
        spot.release()
        self.spot_number = None
        return f"Бронювання для {self.vehicle.name} {self.vehicle.model} скасовано"

    def calculate_fee(self):
        return self.vehicle.calculate_fee(self.hours)


class Transaction:
    def __init__(self, reservation: Reservation):
        self.reservation = reservation
        self.amount_to_pay = 0

    def process_payment(self):
        self.amount_to_pay = self.reservation.calculate_fee()
        return self.amount_to_pay

    def get_transaction_info(self):
        return {
            "Vehicle": str(self.reservation.vehicle),
            "Spot Number": self.reservation.spot_number,
            "Amount to Pay": self.amount_to_pay
        }


# Приклад використання:

Audi = Car('ABC123', 'Audi', 'A4', 'Комфорт')
Bentley = Car('123123', 'Bentley', 'Continental', 'Бізнес')
Harley = Motorcycle('XYZ987', 'Harley', 'Sportster')

floor1 = Parking("1", 5)  # Створюємо паркувальний поверх з 5 місцями

# Бронювання місця для Audi
reservation_audi = Reservation(Audi, floor1, 3)  # 3 години
print(reservation_audi.make_reservation())  # Окупація місця для Audi
transaction_audi = Transaction(reservation_audi)
payment_audi = transaction_audi.process_payment()
print(f"Транзакція для {Audi.name} {Audi.model}: Сума: {payment_audi} у.о.")
print(transaction_audi.get_transaction_info())

# Бронювання місця для Harley
reservation_harley = Reservation(Harley, floor1, 2)  # 2 години
print(reservation_harley.make_reservation())  # Окупація місця для Harley
transaction_harley = Transaction(reservation_harley)
payment_harley = transaction_harley.process_payment()
print(f"Транзакція для {Harley.name} {Harley.model}: Сума: {payment_harley} у.о.")
print(transaction_harley.get_transaction_info())

# Виведення інформації про паркувальні місця
print(floor1)

# Скасування бронювання для Audi
print(reservation_audi.cancel_reservation())  # Скасування для Audi
print(floor1)
