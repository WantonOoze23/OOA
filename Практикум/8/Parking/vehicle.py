from datetime import datetime


class Vehicle():
    def __init__(self, name:str, model:str, plate_number:str, phone_number:str, hours, place = None):
        self.name = name
        self.model = model
        self.plate_number = plate_number
        self.phone_number = phone_number
        self.hours = hours
        self.place = place

        self.time_beginning = datetime.now().strftime('%H:%M %Y-%m-%d')

    def __str__(self):
        return f"{self.name} - {self.model} - {self.plate_number}"

class Car(Vehicle):
    def __init__(self, name: str, model: str, plate_number: str, phone_number: str,  hours, place ,car_class: str = None):

        super().__init__(name, model, plate_number, phone_number, hours, place)
        self.car_class = car_class

class Motorcycle(Vehicle):
    def __init__(self, name: str, model: str, plate_number: str, phone_number: str,  hours, place):
        super().__init__(name, model, plate_number, phone_number, hours, place)

class Truck(Vehicle):
    def __init__(self, name: str, model: str, plate_number: str, phone_number: str, hours, place):
        super().__init__(name, model, plate_number, phone_number, hours, place)

