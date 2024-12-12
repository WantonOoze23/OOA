import customtkinter as ctk
from tkinter import ttk, messagebox
import pandas as pd

from Parking.manager import Manager
from Parking.parking import Parking
from Parking.vehicle import Car, Truck, Motorcycle

# Головне вікно програми
class ParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parking Management System")
        self.root.geometry("1100x700")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize the Parking object
        self.parking = Parking("Main Parking", capacity=20)

        # Initialize the Data DataFrame
        self.Data = pd.DataFrame(
            columns=['Name', 'Model', 'Plate Number', 'Phone Number', 'Parking Spot', 'Hours', 'Class', 'Vehicle Type',
                     'Time', 'Total Payment'])

        # Create the tabs
        self.tabs = ctk.CTkTabview(root, width=1100, height=700)
        self.tabs.pack(fill="both", expand=True)

        # Create the "Add Vehicle" tab
        self.add_vehicle_tab = self.tabs.add("Add Vehicle")
        self.create_add_vehicle_tab()

        # Create the "Manage Parking" tab
        self.manage_tab = self.tabs.add("Manage Parking")
        self.create_manage_tab()

        # Ідентифікатор для скасування after-викликів
        self.after_id = None

    def create_add_vehicle_tab(self):
        frame = self.add_vehicle_tab

        ctk.CTkLabel(frame, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = ctk.CTkEntry(frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Model:").grid(row=1, column=0, padx=10, pady=5)
        self.model_entry = ctk.CTkEntry(frame)
        self.model_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Plate Number:").grid(row=2, column=0, padx=10, pady=5)
        self.plate_entry = ctk.CTkEntry(frame)
        self.plate_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Phone Number:").grid(row=3, column=0, padx=10, pady=5)
        self.phone_entry = ctk.CTkEntry(frame)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Hours:").grid(row=4, column=0, padx=10, pady=5)
        self.hours_entry = ctk.CTkEntry(frame)
        self.hours_entry.grid(row=4, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Class:").grid(row=5, column=0, padx=10, pady=5)
        self.class_combobox = ctk.CTkComboBox(frame, values=["Економ", "Стандарт", "Комфорт", "Бізнес", "N/A"])
        self.class_combobox.grid(row=5, column=1, padx=10, pady=5)
        self.class_combobox.set("N/A")

        ctk.CTkLabel(frame, text="Vehicle Type:").grid(row=6, column=0, padx=10, pady=5)
        self.type_combobox = ctk.CTkComboBox(frame, values=["Car", "Truck", "Motorcycle"])
        self.type_combobox.grid(row=6, column=1, padx=10, pady=5)
        self.type_combobox.set("Car")

        ctk.CTkButton(frame, text="Add Vehicle", command=self.add_vehicle).grid(row=7, column=0, columnspan=2, pady=10)

    def add_vehicle(self):
        name = self.name_entry.get()
        model = self.model_entry.get()
        plate = self.plate_entry.get()
        phone = self.phone_entry.get()
        hours = self.hours_entry.get()
        car_class = self.class_combobox.get()
        vehicle_type = self.type_combobox.get()

        try:
            hours = int(hours)
        except ValueError:
            messagebox.showinfo(title="Input Error", message="Hours must be an integer.", icon="error")
            return

        if vehicle_type == "Car":
            vehicle = Car(name, model, plate, phone, hours, None, car_class)
        elif vehicle_type == "Truck":
            vehicle = Truck(name, model, plate, phone, hours, None)
        elif vehicle_type == "Motorcycle":
            vehicle = Motorcycle(name, model, plate, phone, hours, None)
        else:
            messagebox.showinfo(title="Success", message=f"Vehicle added: {name}\nSpot assigned.")
            return

        manager = Manager(vehicle, self.parking)
        manager.find_spot()

        messagebox.showinfo(title="Success", message=f"Vehicle added: {vehicle.name}\nSpot assigned.", icon="info")
        self.refresh_table()  # Оновлюємо таблицю після додавання

    def create_manage_tab(self):
        frame = self.manage_tab

        # Використання ttk.Treeview для таблиці
        self.tree = ttk.Treeview(frame, columns=("Name", "Model", "Plate", "Spot", "Total Payment"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Model", text="Model")
        self.tree.heading("Plate", text="Plate")
        self.tree.heading("Spot", text="Spot")
        self.tree.heading("Total Payment", text="Total Payment")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkButton(frame, text="Refresh", command=self.refresh_table).pack(pady=5)

        # Додаємо кнопку "Save"
        ctk.CTkButton(frame, text="Save Data", command=self.save_data).pack(pady=5)

        # Додаємо кнопку "Delete"
        ctk.CTkButton(frame, text="Delete Selected", command=self.delete_selected_vehicle).pack(pady=5)

    def refresh_table(self):
        # Очищаємо таблицю перед оновленням
        for row in self.tree.get_children():
            self.tree.delete(row)

        for spot, vehicle in self.parking.occupied_spots.items():
            # Створення менеджера для кожного транспортного засобу
            manager = Manager(vehicle, self.parking)
            # Отримуємо розраховану ціну
            price = manager.TMCPayment()

            # Додаємо дані в таблицю (ім'я, модель, номер та ціна)
            self.tree.insert("", "end", values=(vehicle.name, vehicle.model, vehicle.plate_number, spot, price))

    def delete_selected_vehicle(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo(title="Delete Error", message="No item selected.")
            return

        # Obtain the spot number from the selected row
        spot = self.tree.item(selected_item[0], "values")[3]

        # Remove the vehicle from the parking using the spot number
        message = self.parking.remove_vehicle(spot)

        # Update the table after deletion
        self.refresh_table()
        messagebox.showinfo(title="Delete Success", message=message)

    def save_data(self):
        new_data = []
        for spot, vehicle in self.parking.occupied_spots.items():
            manager = Manager(vehicle, self.parking)
            total_payment = manager.TMCPayment()

            # Add vehicle type to the data dictionary
            vehicle_type = type(vehicle).__name__  # Get the class name of the vehicle (Car, Truck, Motorcycle)

            new_data.append({
                "Name": vehicle.name,
                "Model": vehicle.model,
                "Plate Number": vehicle.plate_number,
                "Phone Number": vehicle.phone_number,
                "Parking Spot": spot,
                "Hours": vehicle.hours,
                "Class": getattr(vehicle, 'car_class', 'N/A'),  # Use 'car_class' if available, otherwise 'N/A'
                "Time": vehicle.time_beginning,
                "Total Payment": total_payment,
                "Vehicle Type": vehicle_type  # Save the vehicle type (Car, Truck, Motorcycle)
            })

        new_df = pd.DataFrame(new_data)
        self.Data = pd.concat([self.Data, new_df], ignore_index=True)
        self.Data.to_csv("parking_lots.csv", index=False)
        messagebox.showinfo(title="Save Data", message="Data has been saved successfully!")

    def load_data(self):
        try:
            df = pd.read_csv("parking_lots.csv")
            for _, row in df.iterrows():
                # Визначаємо тип транспортного засобу
                vehicle_type = row["Vehicle Type"]
                if vehicle_type == "Car":
                    vehicle = Car(
                        row["Name"], row["Model"], row["Plate Number"], row["Phone Number"],
                        row["Hours"], None, row["Class"]
                    )
                elif vehicle_type == "Truck":
                    vehicle = Truck(
                        row["Name"], row["Model"], row["Plate Number"], row["Phone Number"],
                        row["Hours"], None
                    )
                elif vehicle_type == "Motorcycle":
                    vehicle = Motorcycle(
                        row["Name"], row["Model"], row["Plate Number"], row["Phone Number"],
                        row["Hours"], None
                    )
                else:
                    continue  # Пропускаємо, якщо тип транспортного засобу невідомий

                # Призначаємо місце для транспортного засобу
                spot_assigned = self.parking.assign_spot(vehicle)

                if spot_assigned:
                    # Використовуємо менеджер для розрахунку оплати
                    manager = Manager(vehicle, self.parking)
                    vehicle.total_payment = manager.TMCPayment()
        except FileNotFoundError:
            print("File not found. Starting with an empty parking lot.")

    def on_closing(self):
        """Метод для завершення програми коректно."""
        if self.after_id:
            self.root.after_cancel(self.after_id)  # Скасування викликів after
        self.save_data()  # Збереження даних
        self.root.destroy()  # Закриття програми


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = ParkingApp(root)

    app.load_data()

    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()