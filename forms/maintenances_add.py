from customtkinter import *
from tkinter import messagebox

class AddMaintenancesForm(CTkFrame):
    def __init__(self, master, customer_options, vehicle_options, mechanic_options, service_type_options, back_command=None):
        super().__init__(master, fg_color="transparent")
        self.back_command = back_command

        CTkLabel(self, text="Set Maintenance", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pady=(29,0), padx=27)

        form_frame = CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=27, pady=(10,0))

        # 1. Customer selection (ComboBox)
        CTkLabel(form_frame, text="Owner (Customer ID)", font=("Arial Bold", 17), text_color="#fff").grid(row=0, column=0, sticky="w", pady=(0,2))
        self.customer_combo = CTkComboBox(form_frame, values=customer_options, width=300)
        self.customer_combo.grid(row=1, column=0, ipady=0, pady=(0,10))

        # 2. Vehicle selection (ComboBox)
        CTkLabel(form_frame, text="Owner (Vehicle ID)", font=("Arial Bold", 17), text_color="#fff").grid(row=0, column=1, sticky="w", padx=(25,0), pady=(0,2))
        self.vehicle_combo = CTkComboBox(form_frame, values=vehicle_options, width=300)
        self.vehicle_combo.grid(row=1, column=1, ipady=0, padx=(24,0), pady=(0,10))

        # 3. Mechanic selection (ComboBox)
        CTkLabel(form_frame, text="Mechanic ID", font=("Arial Bold", 17), text_color="#fff").grid(row=2, column=0, sticky="w", pady=(0,2))
        self.mechanic_combo = CTkComboBox(form_frame, values=mechanic_options, width=300)
        self.mechanic_combo.grid(row=3, column=0, ipady=0, pady=(0,10))

        # 4. Mileage
        CTkLabel(form_frame, text="Vehicle Mileage", font=("Arial Bold", 17), text_color="#fff").grid(row=2, column=1, sticky="w", padx=(25,0), pady=(0,2))
        self.mileage_entry = CTkEntry(form_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.mileage_entry.grid(row=3, column=1, ipady=0, padx=(24,0), pady=(0,10))

        # 5. Service type selection (ComboBox)
        CTkLabel(form_frame, text="Service Type", font=("Arial Bold", 17), text_color="#fff").grid(row=4, column=0, sticky="w", pady=(0,2))
        self.service_type_combo = CTkComboBox(form_frame, values=service_type_options, width=300)
        self.service_type_combo.grid(row=5, column=0, ipady=0, pady=(0,10))

        # 6. Description
        CTkLabel(form_frame, text="Problem Description", font=("Arial Bold", 17), text_color="#fff").grid(row=4, column=1, sticky="w", padx=(25,0), pady=(0,2))
        self.description_entry = CTkEntry(form_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.description_entry.grid(row=5, column=1, ipady=0, padx=(24,0), pady=(0,10))

        # 7. Labor hours
        CTkLabel(form_frame, text="Labor Hours (Optional)", font=("Arial Bold", 17), text_color="#fff").grid(row=6, column=0, sticky="w", pady=(0,2))
        self.labor_hours_entry = CTkEntry(form_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.labor_hours_entry.grid(row=7, column=0, ipady=0, pady=(0,10))

        # 8. Cost
        CTkLabel(form_frame, text="Cost", font=("Arial Bold", 17), text_color="#fff").grid(row=6, column=1, sticky="w", padx=(25,0), pady=(0,2))
        self.cost_entry = CTkEntry(form_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.cost_entry.grid(row=7, column=1, ipady=0, padx=(24,0), pady=(0,10))

        # Actions
        actions = CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", pady=(10, 20), padx=27)

        CTkButton(
            actions, text="Back", width=150, height=40, fg_color="transparent",
            font=("Arial Bold", 17), border_color="#601E88", hover_color="#601E88",
            border_width=2, text_color="#fff", command=self.back_command
        ).pack(side="left", padx=(0,12))

        CTkButton(
            actions, text="Set", width=150, height=40, font=("Arial Bold", 17),
            hover_color="#9569AF", fg_color="#601E88", text_color="#fff",
            command=self.set_maintenance
        ).pack(side="left", padx=(12,0))

    def set_maintenance(self):
        import connection
        customer_id = self.customer_combo.get().strip()
        vehicle_id = self.vehicle_combo.get().strip()
        mechanic_id = self.mechanic_combo.get().strip()
        mileage = self.mileage_entry.get().strip()
        service_type = self.service_type_combo.get().strip()
        description = self.description_entry.get().strip()
        labor_hours = self.labor_hours_entry.get().strip()
        cost = self.cost_entry.get().strip()

        if not customer_id or not vehicle_id or not mechanic_id or not service_type:
            messagebox.showerror("Error", "All fields except mileage, cost, labor hours and description are required.")
            return
        
        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        if db_obj.con:
            try:
                db_obj.execute(
                    "INSERT INTO maintenances (customer_id, vehicle_id, mechanic_id, mileage, service_type, description, labor_hours, cost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (customer_id, vehicle_id, mechanic_id, mileage, service_type, description, labor_hours, cost)
                )
                db_obj.con.commit()
                messagebox.showinfo("Success", "Maintenance set successfully!")
                if self.back_conmmand:
                    self.back_conmmand()
            except Exception as e:
                messagebox.showerror("Database Error", f"Could not add maintenance: {e}")
            finally:
                db_obj.con.close()