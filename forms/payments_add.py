from customtkinter import *
from tkinter import messagebox
import connection

class AddPaymentsForm(CTkFrame):
    def __init__(self, master, customer_options, vehicle_options, maintenance_options, payment_type_options, back_command=None):
        super().__init__(master, fg_color="transparent")
        self.back_command = back_command

        CTkLabel(self, text="Record Payment", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pady=(29,0), padx=27)

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

        # 3. Maintenance selection (ComboBox)
        CTkLabel(form_frame, text="Maintenanace ID", font=("Arial Bold", 17), text_color="#fff").grid(row=2, column=0, sticky="w", pady=(0,2))
        self.maintenance_combo = CTkComboBox(form_frame, values=maintenance_options, width=300)
        self.maintenance_combo.grid(row=3, column=0, ipady=0, pady=(0,10))

        # 4. Amount
        CTkLabel(form_frame, text="Amount", font=("Arial Bold", 17), text_color="#fff").grid(row=2, column=1, sticky="w", padx=(25,0), pady=(0,2))
        self.amount_entry = CTkEntry(form_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.amount_entry.grid(row=3, column=1, ipady=0, padx=(24,0), pady=(0,10))

        # 5. Payment type selection (ComboBox)
        CTkLabel(form_frame, text="Payment Type", font=("Arial Bold", 17), text_color="#fff").grid(row=4, column=0, sticky="w", pady=(0,2))
        self.payment_type_combo = CTkComboBox(form_frame, values=payment_type_options, width=300)
        self.payment_type_combo.grid(row=5, column=0, ipady=0, pady=(0,10))

        # 6. Recipt Number
        CTkLabel(form_frame, text="Recipt Number", font=("Arial Bold", 17), text_color="#fff").grid(row=4, column=1, sticky="w", padx=(25,0), pady=(0,2))
        self.recipt_number_entry = CTkEntry(form_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.recipt_number_entry.grid(row=5, column=1, ipady=0, padx=(24,0), pady=(0,10))

        # Actions
        actions = CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", pady=(10, 20), padx=27)

        CTkButton(
            actions, text="Back", width=150, height=40, fg_color="transparent",
            font=("Arial Bold", 17), border_color="#601E88", hover_color="#601E88",
            border_width=2, text_color="#fff", command=self.back_command
        ).pack(side="left", padx=(0,12))

        CTkButton(
            actions, text="Record", width=150, height=40, font=("Arial Bold", 17),
            hover_color="#9569AF", fg_color="#601E88", text_color="#fff",
            command=self.record_payment
        ).pack(side="left", padx=(12,0))

    def record_payment(self):
        customer_id = self.customer_combo.get().strip()
        vehicle_id = self.vehicle_combo.get().strip()
        maintenance_id = self.maintenance_combo.get().strip()
        amount = self.amount_entry.get().strip()
        payment_type = self.payment_type_combo.get().strip()
        recipt_number = self.recipt_number_entry.get().strip()

        if not customer_id or not vehicle_id or not maintenance_id or not payment_type or not amount or not recipt_number:
            messagebox.showerror("Error", "All fields are required.")
            return
        
        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        if db_obj.con:
            try:
                db_obj.cur.execute(
                    "INSERT INTO customer_payments (customer_id, vehicle_id, maintenance_id, amount, payment_type, recipt_number) VALUES (%s, %s, %s, %s, %s, %s)",
                    (customer_id, vehicle_id, maintenance_id, amount, payment_type, recipt_number)
                )
                db_obj.con.commit()
                messagebox.showinfo("Success", "Payment recorded successfully!")
                if self.back_command:
                    self.back_command()
            except Exception as e:
                messagebox.showerror("Database Error", f"Could not record payment: {e}")
            finally:
                db_obj.con.close()