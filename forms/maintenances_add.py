from customtkinter import *
from tkinter import messagebox

class AddMaintenancesForm(CTkFrame):
    def __init__(self, master, customer_options, back_command=None):
        super().__init__(master, fg_color="transparent")
        self.back_conmmand = back_command

        CTKLabel(self, text="Set Maintenance", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pday=(29,0), padx=27)