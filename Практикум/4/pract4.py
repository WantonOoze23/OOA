import pandas as pd
import datetime
import matplotlib.pyplot as plt

class EnergyControl:
    def __init__(self, usage, limits: [float]):
        self.usage = usage
        self.minLimit = limits[0]
        self.maxLimit = limits[1]

        self.history = pd.DataFrame(columns=['Time', 'Curent_Usage', 'Min', 'Max'])

    def addNewNote(self, energy):
        new_entry = pd.DataFrame({
            'Time': [datetime.datetime.now().strftime('%Y.%m.%d %H:%M')],
            'Current_Usage': [energy],
            'Min': [self.minLimit],
            'Max': [self.maxLimit]
        })

        self.history = pd.concat([self.history, new_entry], ignore_index=True)

    def changeLimits(self, Limits):
        self.minLimit = Limits[0]
        self.maxLimit = Limits[1]

    def display(self):
        print(self.history)

    def visualisation(self):
        if not self.history.empty:
            plt.figure(figsize=(20, 6))
            plt.plot(self.history.Time, self.history.Current_Usage, label='Usage')

            plt.plot(self.history.Time, self.history.Min, color='r', linestyle='--', label='Min Limit')
            plt.plot(self.history.Time, self.history.Max, color='g', linestyle='--', label='Max Limit')

            plt.xlabel('Time')
            plt.ylabel('Energy Usage Kw/h')
            plt.legend()
            plt.show()
        else:
            print("Немає даних для візуалізації.")

    def save(self):
        self.history.to_csv("energy.csv", index=False)

    def load(self):
        try:
            self.history = pd.read_csv("../5/energy.csv")
            self.history['Time'] = pd.to_datetime(self.history['Time'], format='%Y.%m.%d %H:%M')
            self.history['Current_Usage'] = pd.to_numeric(self.history['Current_Usage'], errors='coerce')
            print("Дані успішно завантажено.")
        except FileNotFoundError:
            print("Файл не знайдено.")
        except pd.errors.EmptyDataError:
            print("Файл порожній.")


def main():
    limits = [200, 2500]
    energyManager = EnergyControl(usage=0, limits=limits)

    while True:
        print("\nМеню\n1. Додати новий запис\n2. Переглянути дані\n3. Завантажити дані\n0. Вийти")
        try:
            choice = int(input('Оберіть опцію: '))
            match choice:
                case 1:
                    print(f"Залишити поточні ліміти min = {energyManager.minLimit}, max = {energyManager.maxLimit}, [y/n]: ")
                    inputChoice = input().lower()
                    if inputChoice == 'y':
                        try:
                            addNewUsage = float(input('Введіть нове значення енергії: '))
                            if energyManager.minLimit <= addNewUsage <= energyManager.maxLimit:
                                energyManager.addNewNote(addNewUsage)
                            else:
                                print(f"Значення енергії має бути в межах {energyManager.minLimit} - {energyManager.maxLimit}")
                        except ValueError:
                            print("Помилка: введено неправильне значення.")
                    elif inputChoice == 'n':
                        try:
                            minLim = float(input('Введіть мінімальний ліміт: '))
                            maxLim = float(input('Введіть максимальний ліміт: '))
                            if minLim < maxLim:
                                energyManager.changeLimits([minLim, maxLim])
                                addNewLimitedUsage = float(input('Введіть нове значення енергії: '))
                                if minLim <= addNewLimitedUsage <= maxLim:
                                    energyManager.addNewNote(addNewLimitedUsage)
                                else:
                                    print(f"Значення енергії має бути в межах {minLim} - {maxLim}")
                            else:
                                print("Мінімальний ліміт має бути меншим за максимальний.")
                        except ValueError:
                            print("Помилка: введено неправильне значення.")
                    else:
                        print("Невірний вибір.")
                case 2:
                    energyManager.display()

                case 3:
                    energyManager.load()

                case 0:
                    energyManager.visualisation()
                    energyManager.save()
                    print('До побачення!')
                    break
                case _:
                    print("Невірний вибір. Спробуйте знову.")

        except ValueError:
            print('Помилка: введіть ціле число!')

if __name__ == '__main__':
    main()
