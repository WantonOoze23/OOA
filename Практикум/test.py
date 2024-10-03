import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

class EnergyConsumer:
    def __init__(self, currentEnergyUsage: float):
        self.currentEnergyUsage = currentEnergyUsage
        maxLimit = 0.0
        minLimit = 0.0

        self.history = pd.DataFrame(columns = ['Time', 'Consumption'])

        self._add_entry(self.currentEnergyUsage)

    def _add_entry(self, consumption):
        new_entry = pd.DataFrame({
            'Time': [pd.Timestamp.now()],
            'Consumption': [consumption]
        })
        self.history = pd.concat([self.history, new_entry], ignore_index=True)

    def getCurrentEnergyUsage(self):
        return self.currentEnergyUsage

    def setCurrentEnergyUsage(self, currentEnergyUsage):
        self.currentEnergyUsage = currentEnergyUsage

    def changeLimits(self, newLimits):
        self.minLimit = newLimits[0]
        self.maxLimit = newLimits[1]

    def constructChart(self):
        df = pd.DataFrame(self.history, columns=['Energy Consumption'])
        df = df.cumsum()
        plt.figure()
        df.plot()
        plt.show()

    def display(self):
        print()

def main():
    curantEnergy = input("Введіть початкове значення: ")
    limits = [100, 200]

    energy = EnergyConsumer(curantEnergy)
    energy.changeLimits(limits)

    energy.constructChart()


if __name__ == '__main__':
    main()