#Завдання: Реалізувати клас для відстеження споживання енергії в реальному часі з можливістю динамічного регулювання споживання.

import pandas as pn
import matplotlib.pyplot as plt

plt.close('all')

class EnergyConsumer:
    def __init__(self, maxLimit: float, minLimit: float):
        self.currentEnergy = 0.0
        self.maxLimit = maxLimit
        self.minLimit = minLimit
        
    def increaseConsumption(self, amount: float):
        if self.currentEnergy + amount > self.maxLimit:
            print(f"Перевищення максимального ліміту! Споживання енергії не може перевищувати {self.maxLimit}")
            self.currentEnergy = self.maxLimit
        else:
            self.currentEnergy += amount
        return self.currentEnergy

    def decreaseConsumption(self, amount: float):
        if self.currentEnergy - amount < self.minLimit:
            print(f"Зменшення нижче мінімального ліміту! Споживання енергії не може бути меншим за {self.minLimit}")
            self.currentEnergy = self.minLimit
        else:
            self.currentEnergy -= amount
        return self.currentEnergy

    def display(self):
        print(self.currentEnergy)

def  main():
    current = float(input("Введіть поточну енергію: "))
    maxF = float(input("Введіть максимальне значення: "))
    minF = float(input("Введіть мінімальне значення: "))
    
    consumer = EnergyConsumer( maxF, minF)
    consumer.currentEnergy = current
    consumer.display()
    amount = 100.0

    consumer.increaseConsumption(amount)
    consumer.display()

    consumer.decreaseConsumption(amount)
    consumer.display()

if __name__ == "__main__":
    main()