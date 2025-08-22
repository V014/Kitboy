from customtkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry


class AddRemindersForm(CTkFrame):
    def __init__(self, master, customer_options, vehicle_options, reminder_type_options, back_command=None, reminder_id=None, reminder_data=None):
        super().__init__(master, fg_color="transparent")
        self.back_command = back_command
        self.reminder_id = reminder_id

        # Title
        CTkLabel(self, text="Set Reminder", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pady=(29,0), padx=27)

        form_frame = CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=27, pady=(10,0))

        # 1. --- Customer ID ---
        CTkLabel(form_frame, text="Customer ID", font=("Arial Bold", 17), text_color="#fff").grid(row=0, column=0, sticky="w", pady=(0,2))
        self.customer_combo = CTkComboBox(form_frame, values=customer_options, width=300)
        self.customer_combo.grid(row=1, column=0, ipady=0, pady=(0,10))

        # 2. --- Vehicle ID ---
        CTkLabel(form_frame, text="Vehicle ID", font=("Arial Bold", 17), text_color="#fff").grid(row=0, column=1, sticky="w", padx=(25,0), pady=(0,6))
        self.vehicle_combo = CTkComboBox(form_frame, values=vehicle_options, width=300)
        self.vehicle_combo.grid(row=1, column=1, sticky="w", padx=(24,0), pady=(0,12))

        # 3. --- Reminder Type ---
        CTkLabel(form_frame, text="Reminder Type", font=("Arial Bold", 17), text_color="#fff").grid(row=2, column=0, sticky="w", pady=(0,2))
        self.reminder_type_combo = CTkComboBox(form_frame, values=reminder_type_options, width=300)
        self.reminder_type_combo.grid(row=3, column=0, ipady=0, pady=(0,10))

        # 4. --- Date Due ---
        CTkLabel(form_frame, text="Date Due (YYYY-MM-DD)", font=("Arial Bold", 17), text_color="#fff").grid(row=2, column=1, sticky="w", padx=(25,0), pady=(0,2))
        self.date_due_entry = DateEntry(form_frame, fg_color="#F0F0F0", border_width=0, width=46, date_pattern='yyyy-mm-dd', background='#601E88')
        self.date_due_entry.grid(row=3, column=1, ipady=0, padx=(24,0), pady=(0,10))

        # 5. --- Description ---
        CTkLabel(form_frame, text="Description", font=("Arial Bold", 17), text_color="#fff").grid(row=4, column=0, sticky="w", pady=(0,2))
        self.description_entry = CTkEntry(form_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.description_entry.grid(row=5, column=0, ipady=0, pady=(0,10))

        # Actions
        actions = CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", pady=(10, 20), padx=27)

        CTkButton(actions, text="Back", width=150, height=40, fg_color="transparent", font=("Arial Bold", 17), border_color="#601E88", hover_color="#601E88", border_width=2, text_color="#fff", command=self.back_command).pack(side="left", padx=(0,12))
        CTkButton(actions, text="Apply", width=150, height=40, font=("Arial Bold", 17), hover_color="#9569AF", fg_color="#601E88", text_color="#fff", command=self.set_reminder).pack(side="left", padx=(12,0))

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
