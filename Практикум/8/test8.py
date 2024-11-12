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
        return f"Місце {self.number}: {f'Зайнято {self.vehicle.name} {self.vehicle.model} {self.vehicle._plate_number}' if self.is_occupied else 'Вільне'}"


class Parking:
    def __init__(self, floor: str, amount: int):
        self.floor = floor
        self.spots = [ParkingSpot(i + 1) for i in range(amount)]

    def find_free_spot(self):
        for spot in self.spots:
            if not spot.is_occupied:
                return spot
        return None

    def find_spot_by_number(self, spot_number):
        if 0 < spot_number <= len(self.spots):
            return self.spots[spot_number - 1]
        return None

    def __str__(self):
        return "\n".join([str(spot) for spot in self.spots])


class Reservation:
    def __init__(self, vehicle: Union[Car, Motorcycle, Truck], parking: Parking, hours: int, spot_number = None):
        self.vehicle = vehicle
        self.parking = parking
        self.hours = hours
        self.spot_number = spot_number

    def make_reservation(self):
        if self.spot_number:  # Якщо користувач вказав місце
            spot = self.parking.find_spot_by_number(self.spot_number)
            if spot and not spot.is_occupied:
                spot.occupy(self.vehicle)
                return f"Бронювання успішне для {self.vehicle.name} {self.vehicle.model} на місце {spot.number}"
            else:
                return f"Місце {self.spot_number} недоступне"
        else:  # Автоматичний вибір вільного місця
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

    def transaction_output(self):
        vehicle = self.reservation.vehicle
        payment = self.process_payment()
        return f"Транзакція для {vehicle.name} {vehicle.model}: Сума: {payment} грн"


def main():
    # Створення прикладів транспортних засобів
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


if __name__ == '__main__':
    main()
