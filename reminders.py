from tkinter import messagebox
from tkcalendar import DateEntry
from customtkinter import *
from CTkTable import CTkTable
from forms.reminders_add import AddRemindersForm
from enum import Enum
from utils import Utils

class ReminderType(Enum):
    TYPE1 = "Payment"
    TYPE2 = "Service"
    TYPE3 = "Retrieval"
    TYPE4 = "Recovery"

class Reminders(CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.all_reminders_data = []  # To store data including IDs
        self.current_view = "list"  # To manage view state: "list" or "detail"

        self.show_reminders_list_view()

    def clear_frame(self):
        # Clears all widgets from this frame.
        for widget in self.winfo_children():
            widget.destroy()

    def show_reminders_list_view(self):
        self.clear_frame()
        self.current_view = "list"

        # Title
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Reminders", font=("Arial", 25), text_color="#ffffff").pack(anchor="nw", side="left")
        CTkButton(master=title_frame, text="Set Reminder", font=("Arial", 15), text_color="#fff", fg_color="#601E88", hover_color="#9569AF", command=self._show_add_form).pack(anchor="ne", side="right")

        self._load_and_display_reminders_table()

    def _load_and_display_reminders_table(self):
        import connection
        db = connection
        dbcon_func = db.dbcon  # Get the function itself
        class DummyDB: pass
        db_obj = DummyDB() # Create an object to act as 'self'
        dbcon_func(db_obj)  # Call dbcon with the dummy object

        if db_obj.con: # Check if connection was successful
            try:
                # Ensure you select the 'id' column first
                # Query to get reminder's info
                query = """
                    SELECT r.id, c.firstname, c.lastname, r.reminder_type, v.reg_number, r.due_date, r.date
                    FROM reminders r
                    JOIN customers c ON r.customer_id = c.id
                    JOIN vehicles v ON r.vehicle_id = v.id
                """
                db_obj.cur.execute(query)
                self.all_reminders_data = db_obj.cur.fetchall()
            finally:
                db_obj.con.close()

        table_display_values = [["Customer", "Type", "Vehicle", "Date Due", "Action"]]
        for row_data in self.all_reminders_data:
            reminders_name = f"{row_data[1]} {row_data[2]}" # Combile firstname and lastname
            display_row = [reminders_name, row_data[3], row_data[4], row_data[5], "View Details"]
            table_display_values.append(display_row)

        if hasattr(self, "reminders_table"):
            self.reminders_table.destroy()

        self.reminders_table = CTkTable(
            master=self,
            values=table_display_values,
            colors=["#030712", "#040C15"],
            header_color="#601E88",
            hover_color="#9569AF",
            text_color="#ffffff",
            command=self.handle_table_action  # <-- Respond to event
        )
        self.reminders_table.edit_row(0, text_color="#ffffff", hover_color="#601E88")
        self.reminders_table.pack(fill="both", expand=True, padx=27, pady=(10, 0))

    def handle_table_action(self, event_data):
        row_index = event_data["row"]    # 0 is header, 1 is first data row
        col_index = event_data["column"]
        action_column_index = len(self.reminders_table.values[0]) - 1

        if col_index == action_column_index and row_index > 0: # Clicked on "Action" cell in a data row
            actual_data_index = row_index - 1 # Adjust for header row
            if 0 <= actual_data_index < len(self.all_reminders_data):
                reminder_id = self.all_reminders_data[actual_data_index][0] # Get the reminders ID (first element)
                self.show_reminder_details_view(reminder_id)

    def show_reminder_details_view(self, reminder_id):
        self.clear_frame()
        self.current_view = "details"

        # Navigation and action buttons
        button_frame = CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20, padx=27, fill="x")
        CTkButton(button_frame, text="Back", command=self.show_reminders_list_view, fg_color="#601E88", hover_color="#9569AF").pack(side="left")
        CTkButton(button_frame, text="Delete", command=lambda: Utils.delete_record("reminders", reminder_id, self.show_reminders_list_view), fg_color="#601E88", hover_color="#DD4055").pack(padx=10, side="right")
        CTkButton(button_frame, text="Update", command=lambda: self._show_add_form(reminder_id),fg_color="#601E88", hover_color="#9569AF").pack(side="right")

        # Title
        CTkLabel(self, text=f"reminder Details (ID: {reminder_id})", font=("Arial Black", 20), text_color="#ffffff").pack(pady=20, padx=27, anchor="w")

        # Fetch more comprehensice details from DB
        import connection
        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        details_text = "Reminders details not found."
        if db_obj.con:
            try:
                # Query to get detailed reminder info
                query = """
                    SELECT c.firstname, c.lastname, r.reminder_type, r.description, v.reg_number, r.due_date, r.status,  DATE_FORMAT(r.date, '%Y-%m-%d')
                    FROM reminders r
                    JOIN customers c ON r.customer_id = c.id
                    JOIN vehicles v ON r.vehicle_id = v.id
                    WHERE r.id = %s
                """
                db_obj.cur.execute(query, (reminder_id,))
                record = db_obj.cur.fetchone()
                if record:
                    details_text = (
                        f"Firstname: {record[0]}\n\n"
                        f"Lastname: {record[1]}\n\n"
                        f"Type: {record[2]}\n\n"
                        f"Description: {record[3]}\n\n"
                        f"Vehicle Registration Number: {record[4]}\n\n"
                        f"Due Date: {record[5]}\n\n"
                        f"Status: {record[6]}\n\n"
                        f"Date: {record[7]}"
                    )
            except Exception as e:
                details_text = f"Error fetching details: {e}"
            finally:
                db_obj.con.close()
        
        CTkLabel(self, text=details_text, font=("Arial", 14), text_color="#ffffff", justify="left", anchor="w", wraplength=600).pack(pady=10, padx=27, anchor="w")

    # show the add form
    def _show_add_form(self, reminder_id=None):
        self.clear_frame()
        customer_options = Utils.get_options("customers", "id")
        vehicle_options = Utils.get_options("vehicles", "id")
        reminder_type_options = [reminder.value for reminder in ReminderType]

        reminder_data = None
        if reminder_id:
            import connection
            db = connection
            dbcon_func = db.dbcon
            class DummyDB: pass
            db_obj = DummyDB()
            dbcon_func(db_obj)
            if db_obj.con:
                try:
                    db_obj.cur.execute(
                        "SELECT customer_id, vehicle_id, reminder_type, description, due_date FROM reminders WHERE id = %s",
                        (reminder_id,)
                    )
                    reminder_data = db_obj.cur.fetchone()
                finally:
                    db_obj.con.close()

        add_form = AddRemindersForm(
            self,
            customer_options,
            vehicle_options,
            reminder_type_options,
            back_command=self.show_reminders_list_view,
            reminder_id=reminder_id,
            reminder_data=reminder_data
        )
        add_form.pack(expand=True, fill="both")

class AddRemindersForm(CTkFrame):
    def __init__(self, master, customer_options, vehicle_options, reminder_type_options, back_command=None, reminder_id=None, reminder_data=None):
        super().__init__(master, fg_color="transparent")
        self.back_command = back_command
        self.reminder_id = reminder_id

        # Customer ID
        CTkLabel(self, text="Customer ID:", text_color="#ffffff", font=("Arial", 14)).pack(pady=(20, 5), padx=27, anchor="w")
        self.customer_combo = CTkComboBox(self, values=customer_options, font=("Arial", 14), fg_color="#2B2B2B", text_color="#ffffff", dropdown_fg_color="#601E88")
        self.customer_combo.pack(fill="x", padx=27, pady=(0, 10))
        
        # Vehicle ID
        CTkLabel(self, text="Vehicle ID:", text_color="#ffffff", font=("Arial", 14)).pack(pady=(10, 5), padx=27, anchor="w")
        self.vehicle_combo = CTkComboBox(self, values=vehicle_options, font=("Arial", 14), fg_color="#2B2B2B", text_color="#ffffff", dropdown_fg_color="#601E88")
        self.vehicle_combo.pack(fill="x", padx=27, pady=(0, 10))

        # Reminder Type
        CTkLabel(self, text="Reminder Type:", text_color="#ffffff", font=("Arial", 14)).pack(pady=(10, 5), padx=27, anchor="w")
        self.reminder_type_combo = CTkComboBox(self, values=reminder_type_options, font=("Arial", 14), fg_color="#2B2B2B", text_color="#ffffff", dropdown_fg_color="#601E88")
        self.reminder_type_combo.pack(fill="x", padx=27, pady=(0, 10))

        # Description
        CTkLabel(self, text="Description:", text_color="#ffffff", font=("Arial", 14)).pack(pady=(10, 5), padx=27, anchor="w")
        self.description_entry = CTkEntry(self, font=("Arial", 14), fg_color="#2B2B2B", text_color="#ffffff")
        self.description_entry.pack(fill="x", padx=27, pady=(0, 10))

        # Date Due
        CTkLabel(self, text="Date Due:", text_color="#ffffff", font=("Arial", 14)).pack(pady=(10, 5), padx=27, anchor="w")
        self.date_due_entry = DateEntry(self, font=("Arial", 14), fg_color="#2B2B2B", text_color="#ffffff", width=17)
        self.date_due_entry.pack(fill="x", padx=27, pady=(0, 10))

        # Action buttons frame
        actions = CTkFrame(self, fg_color="transparent")
        actions.pack(pady=20, padx=27, fill="x")

        # Back button
        CTkButton(
            actions, text="Back", width=150, height=40, font=("Arial Bold", 17),
            hover_color="#9569AF", fg_color="#601E88", text_color="#fff",
            command=self.back_command
        ).pack(side="left", padx=(0, 12))

        # Pre-fill fields if editing
        if reminder_data:
            self.customer_combo.set(str(reminder_data[0]))
            self.vehicle_combo.set(str(reminder_data[1]))
            self.reminder_type_combo.set(str(reminder_data[2]))
            self.description_entry.insert(0, reminder_data[3] if reminder_data[3] else "")
            self.date_due_entry.set_date(reminder_data[4])

        # Change button text if editing
        action_text = "Update Reminder" if reminder_id else "Set Reminder"
        CTkButton(actions, text=action_text, width=150, height=40, font=("Arial Bold", 17), hover_color="#9569AF", fg_color="#601E88", text_color="#fff", command=self.set_reminder).pack(side="left", padx=(12,0))

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
                    # Update existing reminder
                    db_obj.cur.execute(
                        "UPDATE reminders SET customer_id=%s, vehicle_id=%s, reminder_type=%s, description=%s, due_date=%s WHERE id=%s",
                        (customer_id, vehicle_id, reminder_type, description, due_date, self.reminder_id)
                    )
                    db_obj.con.commit()
                    messagebox.showinfo("Success", "Reminder updated successfully!")
                else:
                    # Add new reminder
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

