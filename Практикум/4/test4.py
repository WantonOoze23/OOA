import pandas as pd
import matplotlib.pyplot as plt


class EnergyMonitor:
    def __init__(self, initial_consumption):
        # Ініціалізуємо початкове енергоспоживання (у Ваттах)
        self.consumption = initial_consumption  # Ватти
        # Створюємо порожній DataFrame для зберігання даних
        self.history = pd.DataFrame(columns=['Time', 'Consumption'])
        # Додаємо початкове значення споживання
        self._add_entry(self.consumption)

    def _add_entry(self, consumption):
        """Додає новий запис у історію споживання"""
        new_entry = pd.DataFrame({
            'Time': [pd.Timestamp.now()],
            'Consumption': [consumption]
        })
        self.history = pd.concat([self.history, new_entry], ignore_index=True)

    def update_consumption(self, new_consumption):
        """Оновлює споживання енергії та додає запис у історію"""
        self.consumption = new_consumption
        self._add_entry(new_consumption)

    def adjust_consumption(self, factor):
        """Динамічно регулює споживання енергії за допомогою коефіцієнта"""
        adjusted_consumption = self.consumption * factor
        self.update_consumption(adjusted_consumption)
        print(f"Споживання енергії скориговано на {factor * 100}% від поточного значення.")

    def visualize_consumption(self):
        """Візуалізує споживання енергії за часом"""
        plt.figure(figsize=(10, 5))
        plt.plot(self.history['Time'], self.history['Consumption'], label='Енергоспоживання (Вт)')
        plt.xlabel('Час')
        plt.ylabel('Споживання енергії (Вт)')
        plt.title('Моніторинг енергоспоживання в реальному часі')
        plt.legend()
        plt.show()

    def get_summary(self):
        """Повертає основні статистичні дані про споживання енергії"""
        return self.history.describe()

    def save_data(self, filename='energy_data.csv'):
        """Зберігає дані у CSV файл"""
        self.history.to_csv(filename, index=False)
        print(f"Дані збережено у файл {filename}")

    def load_data(self, filename='energy_data.csv'):
        """Завантажує дані з CSV файлу"""
        self.history = pd.read_csv(filename)
        print(f"Дані завантажено з файлу {filename}")


# Приклад використання класу
monitor = EnergyMonitor(1000)  # Початкове споживання: 1000 Вт
monitor.update_consumption(1200)  # Оновити споживання до 1200 Вт
monitor.adjust_consumption(0.9)  # Зменшити споживання на 10%
monitor.visualize_consumption()  # Візуалізувати споживання
print(monitor.get_summary())  # Отримати статистичні дані

# Збереження даних у CSV файл
monitor.save_data()

# Завантаження даних із CSV файлу
monitor.load_data()
