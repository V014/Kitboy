from customtkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry


class AddRemindersForm(CTkFrame):
    def __init__(self, master, customer_options, vehicle_options, reminder_type_options,
                 back_command=None, reminder_id=None, reminder_data=None):
        super().__init__(master, fg_color="transparent")
        self.back_command = back_command
        self.reminder_id = reminder_id

        # --- Configure grid for self (the main frame) ---
        self.grid_columnconfigure(0, weight=1)   # left column
        self.grid_columnconfigure(1, weight=1)   # right column

        # Title
        CTkLabel(
            self, text="Set Reminder",
            font=("Arial Black", 25), text_color="#fff"
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=27, pady=(29, 10))

        # --- Customer ID ---
        CTkLabel(self, text="Customer ID", font=("Arial Bold", 17), text_color="#fff").grid(
            row=1, column=0, sticky="w", padx=27, pady=(0, 2))
        self.customer_combo = CTkComboBox(self, values=customer_options, width=300)
        self.customer_combo.grid(row=2, column=0, sticky="w", padx=27, pady=(0, 10))

        # --- Vehicle ID ---
        CTkLabel(self, text="Vehicle ID", font=("Arial Bold", 17), text_color="#fff").grid(
            row=1, column=1, sticky="w", padx=27, pady=(0, 2))
        self.vehicle_combo = CTkComboBox(self, values=vehicle_options, width=300)
        self.vehicle_combo.grid(row=2, column=1, sticky="w", padx=27, pady=(0, 10))

        # --- Reminder Type ---
        CTkLabel(self, text="Reminder Type", font=("Arial Bold", 17), text_color="#fff").grid(
            row=3, column=0, sticky="w", padx=27, pady=(0, 2))
        self.reminder_type_combo = CTkComboBox(self, values=reminder_type_options, width=300)
        self.reminder_type_combo.grid(row=4, column=0, sticky="w", padx=27, pady=(0, 10))

        # --- Date Due ---
        CTkLabel(self, text="Date Due", font=("Arial Bold", 17), text_color="#fff").grid(
            row=3, column=1, sticky="w", padx=27, pady=(0, 2))
        self.date_due_entry = DateEntry(self, width=18)
        self.date_due_entry.grid(row=4, column=1, sticky="w", padx=27, pady=(0, 10))

        # --- Description (span both columns) ---
        CTkLabel(self, text="Description", font=("Arial Bold", 17), text_color="#fff").grid(
            row=5, column=0, columnspan=2, sticky="w", padx=27, pady=(0, 2))
        self.description_entry = CTkEntry(self, fg_color="#F0F0F0", border_width=0, width=624)
        self.description_entry.grid(row=6, column=0, columnspan=2, sticky="ew", padx=27, pady=(0, 10))

        # --- Action Buttons (span both columns, align left/right) ---
        self.grid_rowconfigure(7, weight=1)  # push buttons to the bottom

        back_btn = CTkButton(
            self, text="Back", width=150, height=40, fg_color="transparent",
            font=("Arial Bold", 17), border_color="#601E88",
            hover_color="#601E88", border_width=2, text_color="#fff",
            command=self.back_command
        )
        back_btn.grid(row=8, column=0, sticky="w", padx=27, pady=(20, 20))

        action_text = "Update Reminder" if reminder_id else "Set Reminder"
        submit_btn = CTkButton(
            self, text=action_text, width=150, height=40,
            font=("Arial Bold", 17), hover_color="#9569AF",
            fg_color="#601E88", text_color="#fff",
            command=self.set_reminder
        )
        submit_btn.grid(row=8, column=1, sticky="e", padx=27, pady=(20, 20))

        # --- Pre-fill fields if editing ---
        if reminder_data:
            try:
                self.customer_combo.set(str(reminder_data[0]))
                self.vehicle_combo.set(str(reminder_data[1]))
                self.reminder_type_combo.set(str(reminder_data[2]))
                if reminder_data[3]:
                    self.description_entry.insert(0, reminder_data[3])
                if reminder_data[4]:
                    try:
                        self.date_due_entry.set_date(reminder_data[4])
                    except Exception:
                        pass
            except Exception:
                pass

    def set_reminder(self):
        customer_id = self.customer_combo.get().strip()
        vehicle_id = self.vehicle_combo.get().strip()
        reminder_type = self.reminder_type_combo.get().strip()
        description = self.description_entry.get().strip()
        due_date = self.date_due_entry.get_date()

        if not customer_id or not vehicle_id or not reminder_type or not due_date:
            messagebox.showerror("Error", "All fields except description are required.")
            return

        import connection
        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        if db_obj.con:
            try:
                if self.reminder_id:
                    db_obj.cur.execute(
                        "UPDATE reminders SET customer_id=%s, vehicle_id=%s, reminder_type=%s, description=%s, due_date=%s WHERE id=%s",
                        (customer_id, vehicle_id, reminder_type, description, due_date, self.reminder_id)
                    )
                    db_obj.con.commit()
                    messagebox.showinfo("Success", "Reminder updated successfully!")
                else:
                    db_obj.cur.execute(
                        "INSERT INTO reminders (customer_id, vehicle_id, reminder_type, description, due_date) VALUES (%s, %s, %s, %s, %s)",
                        (customer_id, vehicle_id, reminder_type, description, due_date)
                    )
                    db_obj.con.commit()
                    messagebox.showinfo("Success", "Reminder set successfully!")
                if self.back_command:
                    self.back_command()
            except Exception as e:
                messagebox.showerror("Database Error", f"Could not save reminder: {e}")
            finally:
                db_obj.con.close()
