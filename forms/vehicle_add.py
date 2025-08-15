from socket import if_indextoname
from customtkinter import *
from tkinter import messagebox

class AddVehicleForm(CTkFrame):
    def __init__(self, master, customer_options, transmission_type_options, back_command=None, vehicle_id=None):
        super().__init__(master, fg_color="transparent")
        self.back_command = back_command
        self.vehicle_id = vehicle_id

        # Title
        CTkLabel(self, text="Add Vehicle", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pady=(29,0), padx=27)

        form_frame = CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=27, pady=(10,0))

        # Customer selection (ComboBox)
        CTkLabel(form_frame, text="Owner (Customer ID)", font=("Arial Bold", 17), text_color="#fff").grid(row=0, column=0, sticky="w", pady=(0,2))
        self.customer_combo = CTkComboBox(form_frame, values=customer_options, width=300)
        self.customer_combo.grid(row=1, column=0, ipady=0, pady=(0,10))

        # Registration Number
        CTkLabel(form_frame, text="Registration Number", font=("Arial Bold", 17), text_color="#fff").grid(row=0, column=1, sticky="w", padx=(25,0), pady=(0,2))
        self.reg_entry = CTkEntry(form_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.reg_entry.grid(row=1, column=1, ipady=0, padx=(24,0), pady=(0,10))

        # Make
        CTkLabel(form_frame, text="Make", font=("Arial Bold", 17), text_color="#fff").grid(row=2, column=0, sticky="w", pady=(0,2))
        self.make_entry = CTkEntry(form_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.make_entry.grid(row=3, column=0, ipady=0, pady=(0,10))

        # Model
        CTkLabel(form_frame, text="Model", font=("Arial Bold", 17), text_color="#fff").grid(row=2, column=1, sticky="w", padx=(25,0), pady=(0,2))
        self.model_entry = CTkEntry(form_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.model_entry.grid(row=3, column=1, ipady=0, padx=(24,0), pady=(0,10))

        # Year
        CTkLabel(form_frame, text="Year", font=("Arial Bold", 17), text_color="#fff").grid(row=4, column=0, sticky="w", pady=(0,2))
        self.year_entry = CTkEntry(form_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.year_entry.grid(row=5, column=0, ipady=0, pady=(0,10))

        # Transmission
        CTkLabel(form_frame, text="Transmission", font=("Arial Bold", 17), text_color="#fff").grid(row=4, column=1, sticky="w", padx=(25,0), pady=(0,2))
        self.transmission_combo = CTkComboBox(form_frame, values=transmission_type_options, width=300)
        self.transmission_combo.grid(row=5, column=1, ipady=0, padx=(24,0), pady=(0,10))

        # Color
        CTkLabel(form_frame, text="Color", font=("Arial Bold", 17), text_color="#fff").grid(row=6, column=0, sticky="w", pady=(0,2))
        self.color_entry = CTkEntry(form_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.color_entry.grid(row=7, column=0, ipady=0, pady=(0,10))

        # VIN Number (optional)
        CTkLabel(form_frame, text="VIN Number (optional)", font=("Arial Bold", 17), text_color="#fff").grid(row=6, column=1, sticky="w", padx=(25,0), pady=(0,2))
        self.vin_entry = CTkEntry(form_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.vin_entry.grid(row=7, column=1, ipady=0, padx=(24,0), pady=(0,10))

        # Actions
        actions = CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", pady=(10, 20), padx=27)

        CTkButton(actions, text="Back", width=150, height=40, fg_color="transparent", font=("Arial Bold", 17), border_color="#601E88", hover_color="#601E88", border_width=2, text_color="#fff", command=self.back_command).pack(side="left", padx=(0,12))
        CTkButton(actions, text="Apply", width=150, height=40, font=("Arial Bold", 17), hover_color="#9569AF", fg_color="#601E88", text_color="#fff", command=self.add_vehicle).pack(side="left", padx=(12,0))

        if self.vehicle_id:
            import connection
            db = connection
            dbcon_func = db.dbcon
            class DummyDB: pass
            db_obj = DummyDB()
            dbcon_func(db_obj)

            if db_obj.con:
                try:
                    db_obj.cur.execute(
                        "SELECT make, year, color, model, reg_number, vin_number, transmission, customer_id FROM vehicles WHERE id = %s", 
                        (self.vehicle_id,)
                    )
                    record = db_obj.cur.fetchone()
                    if record:
                        self.make_entry.insert(0, record[0])
                        self.year_entry.insert(0, record[1])
                        self.color_entry.insert(0, record[2])
                        self.model_entry.insert(0, record[3])
                        self.reg_entry.insert(0, record[4])
                        self.vin_entry.insert(0, record[5])
                        self.transmission_combo.set(str (record[6]))
                        self.customer_combo.set(str(record[7]))
                finally:
                    db_obj.con.close() 

    def add_vehicle(self):
        customer_id = self.customer_combo.get().strip()
        reg_number = self.reg_entry.get().strip()
        make = self.make_entry.get().strip()
        model = self.model_entry.get().strip()
        year = self.year_entry.get().strip()
        transmission = self.transmission_combo.get().strip()
        color = self.color_entry.get().strip()
        vin_number = self.vin_entry.get().strip()

        if not customer_id or not reg_number or not make or not model or not year or not transmission or not color:
            messagebox.showerror("Error", "All fields except VIN Number are required.")
            return

        import connection
        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        if db_obj.con:
            try:
                if self.vehicle_id:
                    # UPDATE existing record
                    db_obj.cur.execute(
                        """
                        UPDATE vehicles
                        SET customer_id = %s, make = %s, year = %s, model = %s,
                            reg_number = %s, vin_number = %s, color = %s, transmission = %s
                        WHERE id = %s
                        """,
                        (customer_id, make, year, model, reg_number, vin_number, color, transmission, self.vehicle_id)
                    )
                    messagebox.showinfo("Success", "Vehicle details updated successfully!")
                else:
                    # ADD a vehicle
                    db_obj.cur.execute(
                        "INSERT INTO vehicles (customer_id, reg_number, make, model, year, transmission, color, vin_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (customer_id, reg_number, make, model, year, transmission, color, vin_number)
                    )
                    messagebox.showinfo("Success", "Vehicle added successfully!")

                db_obj.con.commit()
                
                if self.back_command:
                    self.back_command()
            except Exception as e:
                messagebox.showerror("Database Error", f"Could not add vehicle: {e}")
            finally:
                db_obj.con.close()