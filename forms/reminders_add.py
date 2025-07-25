from customtkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
import connection

class AddRemindersForm(CTkFrame):
    def __init__(self, master, customer_options, vehicle_options, reminder_type_options, back_command=None):
        super().__init__(master, fg_color="transparent")
        self.back_command = back_command

        CTkLabel(self, text="Set Reminder", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pady=(29,0), padx=27)

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

        # 3. Reminder type selection (ComboBox)
        CTkLabel(form_frame, text="Reminder Type", font=("Arial Bold", 17), text_color="#fff").grid(row=2, column=0, sticky="w", pady=(0,2))
        self.reminder_type_combo = CTkComboBox(form_frame, values=reminder_type_options, width=300)
        self.reminder_type_combo.grid(row=3, column=0, ipady=0, pady=(0,10))

        # 4. Description
        CTkLabel(form_frame, text="Problem Description", font=("Arial Bold", 17), text_color="#fff").grid(row=2, column=1, sticky="w", padx=(25,0), pady=(0,2))
        self.description_entry = CTkEntry(form_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.description_entry.grid(row=3, column=1, ipady=0, padx=(24,0), pady=(0,10))

        # 5. Date due
        CTkLabel(form_frame, text="Due date", font=("Arial Bold", 17), text_color="#fff").grid(row=4, column=0, sticky="w", pady=(0,2))
        self.date_due_entry = CTkEntry(form_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.date_due_entry.grid(row=7, column=0, ipady=0, pady=(0,10))

        # Actions
        actions = CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", pady=(10, 20), padx=27)

        CTkButton(
            actions, text="Back", width=150, height=40, fg_color="transparent",
            font=("Arial Bold", 17), border_color="#601E88", hover_color="#601E88",
            border_width=2, text_color="#fff", command=self.back_command
        ).pack(side="left", padx=(0,12))

        CTkButton(
            actions, text="Set Reminder", width=150, height=40, font=("Arial Bold", 17),
            hover_color="#9569AF", fg_color="#601E88", text_color="#fff",
            command=self.set_reminder
        ).pack(side="left", padx=(12,0))

    def set_reminder(self):
        customer_id = self.customer_combo.get().strip()
        vehicle_id = self.vehicle_combo.get().strip()
        reminder_type = self.reminder_type_combo.get().strip()
        description = self.description_entry.get().strip()
        due_date = self.date_due_entry.get().strip()

        if not customer_id or not vehicle_id or not reminder_type or not due_date:
            messagebox.showerror("Error", "All fields except description are required.")
            return
        
        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        if db_obj.con:
            try:
                db_obj.cur.execute(
                    "INSERT INTO reminders (customer_id, vehicle_id, reminder_type, desciption, due_date) VALUES (%s, %s, %s, %s, %s)",
                    (customer_id, vehicle_id, reminder_type, description, due_date)
                )
                db_obj.con.commit()
                messagebox.showinfo("Success", "reminder set successfully!")
                if self.back_command:
                    self.back_command()
            except Exception as e:
                messagebox.showerror("Database Error", f"Could not add reminder: {e}")
            finally:
                db_obj.con.close()