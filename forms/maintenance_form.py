from customtkinter import *
from PIL import Image

class MaintenanceForm(CTkToplevel):
    def __init__(self, master, customers, cars, mechanics, on_submit):
        super().__init__(master)
        self.title("Assign Maintenance Job")
        self.geometry("500x500")
        self.resizable(False, False)

        CTkLabel(self, text="Assign Job", font=("Arial Black", 22)).pack(pady=(20, 10))

        # Customer selection
        CTkLabel(self, text="Customer:", font=("Arial Bold", 14)).pack(anchor="w", padx=30, pady=(10, 0))
        self.customer_cb = CTkComboBox(self, values=customers, width=300)
        self.customer_cb.pack(padx=30, pady=5)

        # Car selection
        CTkLabel(self, text="Car:", font=("Arial Bold", 14)).pack(anchor="w", padx=30, pady=(10, 0))
        self.car_cb = CTkComboBox(self, values=cars, width=300)
        self.car_cb.pack(padx=30, pady=5)

        # Mechanic selection
        CTkLabel(self, text="Mechanic:", font=("Arial Bold", 14)).pack(anchor="w", padx=30, pady=(10, 0))
        self.mechanic_cb = CTkComboBox(self, values=mechanics, width=300)
        self.mechanic_cb.pack(padx=30, pady=5)

        # Job description
        CTkLabel(self, text="Job Description:", font=("Arial Bold", 14)).pack(anchor="w", padx=30, pady=(10, 0))
        self.desc_entry = CTkTextbox(self, width=300, height=80)
        self.desc_entry.pack(padx=30, pady=5)

        # Submit button
        CTkButton(self, text="Assign Job", command=self.submit).pack(pady=20)

        self.on_submit = on_submit

    def submit(self):
        data = {
            "customer": self.customer_cb.get(),
            "car": self.car_cb.get(),
            "mechanic": self.mechanic_cb.get(),
            "description": self.desc_entry.get("1.0", "end").strip()
        }
        self.on_submit(data)
        self.destroy()