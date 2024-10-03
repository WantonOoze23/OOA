import pandas as pd
import datetime
import matplotlib.pyplot as plt


class EnergyControll:
    def __init__(self, usage, limits: float):
        self.usage = usage
        self.minLimit = limits[0]
        self.maxLimit = limits[1]

        self.history = pd.DataFrame(columns=['Time', 'Usage', 'Min', 'Max'])

    def addNewNote(self, energy):
        new_entry = pd.DataFrame({
            'Time': [datetime.datetime.now()],
            'Usage': [energy],
            'Min': [self.minLimit],
            'Max': [self.maxLimit]
        })

        if not self.history.empty:
            self.history = pd.concat([self.history, new_entry], ignore_index=True)
        else:
            self.history = new_entry

    def changeLimits(self, Limits):
        self.minLimit = Limits[0]
        self.maxLimit = Limits[1]

    def display(self):
        print(self.history)

    def visualisation(self):
        if not self.history.empty:
            plt.figure()
            plt.plot(self.history.Time, self.history.Usage, label='Usage')
            plt.axhline(self.minLimit, color='r', linestyle='--', label='Min')
            plt.axhline(self.maxLimit, color='g', linestyle='--', label='Max')
            plt.legend()
            plt.show()
        else:
            print("Немає даних для візуалізації.")

    def save(self):
        self.history.to_csv("energy.csv", index=False)

    def load(self):
        try:
            self.history = pd.read_csv("energy.csv")
            self.history['Time'] = pd.to_datetime(self.history['Time'])
            print("Дані успішно завантажено.")
        except FileNotFoundError:
            print("Файл не знайдено.")
        except pd.errors.EmptyDataError:
            print("Файл порожній.")


def main():
    limits = [200, 2500]
    energyManager = EnergyControll(usage=0, limits=limits )

    print(energyManager.history)

    while True:
        print("Меню\n1. Додати новий запис\n2. Переглянути дані\n3. Завантажити дані\n0. Вийти")
        try:
            choice = int(input('Оберіть опцію: '))
            match choice:
                case 1:
                    try:
                        print(f"Залишити поточні ліміти min = {limits[0]}, max = {limits[1]}, [y/n]: ")
                        inputChoice = input().lower()
                        match inputChoice:
                            case 'y':
                                try:
                                    addNewUsage = float(input('Введіть нове значення енергії: '))
                                    if limits[0] <= addNewUsage <= limits[1]:
                                        energyManager.addNewNote(addNewUsage)
                                    else:
                                        print(f"Значення енергії має бути в межах {limits[0]} - {limits[1]}")
                                except ValueError:
                                    print("Так не можна")

                            case 'n':
                                minLim = float(input('Введіть мінімальний ліміт: '))
                                maxLim = float(input('Введіть максимальний ліміт: '))
                                if minLim < maxLim:
                                    newLimits = [minLim, maxLim]
                                    energyManager.changeLimits(newLimits)  # Оновлення меж в об'єкті

                                    addNewLimitedUsage = float(input('Введіть нове значення енергії: '))
                                    if newLimits[0] <= addNewLimitedUsage <= newLimits[1]:
                                        energyManager.addNewNote(addNewLimitedUsage)
                                    else:
                                        print(f"Значення енергії має бути в межах {newLimits[0]} - {newLimits[1]}")
                                else:
                                    print("Мінімальний ліміт має бути меншим за максимальний.")
                    except ValueError:
                        print("Спробуйте ще раз")

                case 2:
                    energyManager.display()

                case 3:
                    energyManager.load()

                case 0:
                    energyManager.visualisation()
                    energyManager.save()
                    print('Bye Bye!...')
                    break

            print(energyManager.history)
        except ValueError:
            print('Введіть ціле число!')


if __name__ == '__main__':
    main()

