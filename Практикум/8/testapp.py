import customtkinter as ctk
from tkinter import messagebox

from Parking import parking as Parking
from Parking import vehicle as Vehicle
from Parking import manager as ParkingManager

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('')
        self.geometry('800x500')

        self.minsize(800,500)


        self.parking1 = Parking(name = 'Cars', )


        self.controllPanen()

        self.mainloop()

    def controllPanen(self):
        self.button_add = ctk.CTkButton(self, text="Додати місце")
        self.button_remove = ctk.CTkButton(self, text="Звільнити місце")
        self.button_add.grid(row=0, column=0, padx=10, pady=10)
        self.button_remove.grid(row=1, column=0, padx=10, pady=10)



if __name__ == '__main__':
    app = App()