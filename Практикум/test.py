import matplotlib.pyplot as plt
import pandas as pd

class EnergyConsumer:
    def __init__(self, currentEnergyUsage: float):
        self.currentEnergyUsage = currentEnergyUsage
        maxLimit = 0.0
        minLimit = 0.0

        self.history = pd.DataFrame(['Time'],['Rate'])
        self.addNew(self.currentEnergyUsage)

    def getCurrentEnergyUsage(self):
        return self.currentEnergyUsage

    def setCurrentEnergyUsage(self, currentEnergyUsage):
        self.currentEnergyUsage = currentEnergyUsage

    def changeLimits(self, newLimits):
        self.minLimit = newLimits[0]
        self.maxLimit = newLimits[1]

    def addNew(self, newEnergyUsage):
        newNote = pd.DataFrame({
            'Time': [pd.Timestamp.now()],
            'Consumption': [newEnergyUsage]
        })

        self.history = pd.concat([self.history, newNote], ignore_index=True)


def main():
    curantEnergy = input("Введіть початкове значення: ")
    limits = [100, 200]

    energy = EnergyConsumer(curantEnergy)
    energy.changeLimits(limits)
    print(energy)


if __name__ == '__main__':
    main()