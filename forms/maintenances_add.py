from customtkinter import *
from tkinter import messagebox

class AddMaintenancesForm(CTkFrame):
    def __init__(self, master, customer_options, vehicle_options, mechanic_options, back_command=None):
        super().__init__(master, fg_color="transparent")
        self.back_conmmand = back_command

        CTKLabel(self, text="Set Maintenance", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pday=(29,0), padx=27)

        form_frame = CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=27, pady=(10,0))

        # Customer selection (ComboBox)
        CTkLabel(form_frame, text="Owner (Customer ID)", font=("Arial Bold", 17), text_color="#fff").grid(row=0, column=0, sticky="w", pady=(0,2))
        self.customer_combo = CTkComboBox(form_frame, values=customer_options, width=300)
        self.customer_combo.grid(row=1, column=0, ipady=10, pady=(0,10))

        # Vehicle selection (ComboBox)
        CTkLabel(form_frame, text="Owner (Vehicle ID)", font=("Arial Bold", 17), text_color="#fff").grid(row=0, column=0, sticky="w", pady=(0,2))
        self.vehicle_combo = CTkComboBox(form_frame, values=vehicle_options, width=300)
        self.vehicle_combo.grid(row=1, column=0, ipady=10, pady=(0,10))

        # Mechanic selection (ComboBox)
        CTkLabel(form_frame, text="Owner (Vehicle ID)", font=("Arial Bold", 17), text_color="#fff").grid(row=0, column=0, sticky="w", pady=(0,2))
        self.mechanic_combo = CTkComboBox(form_frame, values=mechanic_options, width=300)
        self.mechanic_combo.grid(row=1, column=0, ipady=10, pady=(0,10))