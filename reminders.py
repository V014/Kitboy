import connection
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image

class Reminders(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.all_reminders_data = [] # To store data including IDs
        self.current_view = "list" # To manage view state: "list" or "detail"

        self.show_reminders_list_view()

    def clear_frame(self):
        """Clears all widgets from this frame."""
        for widget in self.winfo_children():
            widget.destroy()

    def show_reminders_list_view(self):
        self.clear_frame()
        self.current_view = "list"

        # Title
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Reminders", font=("Arial Black", 25), text_color="#ffffff").pack(anchor="nw", side="left")
        CTkButton(master=title_frame, text="+ New Reminder", font=("Arial Black", 15), text_color="#fff", fg_color="#601E88", hover_color="#9569AF").pack(anchor="ne", side="right")
        # Add command for new reminder form, e.g., command=self.open_reminder_form

        self.create_search_container()
        self._load_and_display_reminders_table()

    def create_search_container(self):
        search_container = CTkFrame(master=self, height=50, fg_color="#040C15")
        search_container.pack(fill="x", pady=(45, 0), padx=27)
        CTkEntry(master=search_container, width=305, placeholder_text="Search (Customer, Vehicle, Type)", border_color="#601E88", border_width=2).pack(side="left", padx=(13, 0), pady=15)
        CTkComboBox(master=search_container, width=125, values=["All Types", "Payment Due", "Service Reminder"], button_color="#601E88", border_color="#601E88", border_width=2, button_hover_color="#9569AF",dropdown_hover_color="#9569AF" , dropdown_fg_color="#030712", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)
        CTkComboBox(master=search_container, width=125, values=["All Status", "Pending", "Completed", "Overdue"], button_color="#601E88", border_color="#601E88", border_width=2, button_hover_color="#9569AF",dropdown_hover_color="#9569AF" , dropdown_fg_color="#030712", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)

    def _load_and_display_reminders_table(self):
        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        self.all_reminders_data = []
        if db_obj.con:
            try:
                # Query to get reminder info, customer's name, and vehicle's reg_number
                query = """
                    SELECT r.id, c.firstname, c.lastname, v.reg_number, 
                           r.description, r.due_date, r.status
                    FROM reminders r
                    JOIN customers c ON r.customer_id = c.id
                    LEFT JOIN vehicles v ON r.vehicle_id = v.id
                    ORDER BY r.due_date ASC
                """
                db_obj.cur.execute(query)
                self.all_reminders_data = db_obj.cur.fetchall()
            except Exception as e:
                print(f"Database error: {e}") # Basic error logging
                # Optionally, display an error message in the UI
            finally:
                db_obj.con.close()

        table_display_values = [["Customer", "Vehicle", "Description", "Due Date", "Status", "Action"]]
        for row_data in self.all_reminders_data:
            # row_data: (r.id, c.firstname, c.lastname, v.reg_number, r.description, r.due_date, r.status)
            customer_name = f"{row_data[1]} {row_data[2]}"
            vehicle_reg = row_data[3] if row_data[3] else "N/A"
            description = row_data[4] # Consider truncating if too long
            due_date = str(row_data[5]) if row_data[6] else "N/A"
            status = row_data[6]
            display_row = [customer_name, vehicle_reg, description, due_date, status, "View Details"]
            table_display_values.append(display_row)

        if hasattr(self, "reminders_table"):
            self.reminders_table.destroy()

        self.reminders_table = CTkTable(
            master=self,
            values=table_display_values,
            colors=["#030712", "#040C15"],
            header_color="#030712",
            hover_color="#9569AF",
            text_color="#ffffff",
            command=self.handle_table_action
        )
        self.reminders_table.edit_row(0, text_color="#ffffff", hover_color="#601E88")
        self.reminders_table.pack(fill="both", expand=True, padx=27, pady=(10, 0))

    def handle_table_action(self, event_data):
        row_index = event_data["row"]    # 0 is header, 1 is first data row
        col_index = event_data["column"]
        
        if not self.reminders_table.values or row_index >= len(self.reminders_table.values):
            return # Clicked on empty table or out of bounds

        action_column_index = len(self.reminders_table.values[0]) - 1

        if col_index == action_column_index and row_index > 0: # Clicked on "Action" cell in a data row
            actual_data_index = row_index - 1 # Adjust for header row
            if 0 <= actual_data_index < len(self.all_reminders_data):
                reminder_id = self.all_reminders_data[actual_data_index][0] # Get the reminder ID
                self.show_reminder_detail_view(reminder_id)

    def show_reminder_detail_view(self, reminder_id):
        self.clear_frame()
        self.current_view = "detail"

        CTkLabel(self, text=f"Reminder Details (ID: {reminder_id})", font=("Arial Black", 20), text_color="#ffffff").pack(pady=20, padx=27, anchor="w")

        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        details_text = "Reminder details not found."
        if db_obj.con:
            try:
                query = """
                    SELECT 
                        r.description, r.due_date, r.status, r.notes,
                        c.firstname, c.lastname, c.contact AS customer_contact,
                        v.reg_number, v.make AS vehicle_make, v.model AS vehicle_model
                    FROM reminders r
                    JOIN customers c ON r.customer_id = c.id
                    LEFT JOIN vehicles v ON r.vehicle_id = v.id
                    WHERE r.id = %s
                """
                db_obj.cur.execute(query, (reminder_id,))
                record = db_obj.cur.fetchone()
                if record:
                    # record: (desc, due_date, status, notes, c.fn, c.ln, c.contact, v.reg, v.make, v.model)
                    details_text = (
                        f"Description: {record[1]}\n"
                        f"Due Date: {record[2] if record[2] else 'N/A'}\n"
                        f"Status: {record[3]}\n"
                        f"Notes: {record[4] if record[4] else 'N/A'}\n\n"
                        f"Customer: {record[5]} {record[6]}\n"
                        f"Customer Contact: {record[7] if record[7] else 'N/A'}\n\n"
                    )
                    if record[8]: # If vehicle details exist
                        details_text += (
                            f"Vehicle Registration: {record[8]}\n"
                            f"Vehicle Make: {record[9] if record[9] else 'N/A'}\n"
                            f"Vehicle Model: {record[10] if record[10] else 'N/A'}\n"
                        )
                    else:
                        details_text += "No associated vehicle.\n"

            except Exception as e:
                details_text = f"Error fetching reminder details: {e}"
            finally:
                db_obj.con.close()
        
        CTkLabel(self, text=details_text, font=("Arial", 14), text_color="#ffffff", justify="left", anchor="w").pack(pady=10, padx=27, anchor="w")

        CTkButton(self, text="Back to List", command=self.show_reminders_list_view, fg_color="#601E88", hover_color="#9569AF").pack(pady=20, padx=27)


# Example of a hypothetical reminders table schema for your database:
# CREATE TABLE reminders (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     customer_id INT NOT NULL,
#     vehicle_id INT NULL,
#     reminder_type VARCHAR(255) NOT NULL, -- e.g., 'Payment Due', 'Service Reminder'
#     description TEXT,
#     due_date DATE,
#     status VARCHAR(50) NOT NULL DEFAULT 'Pending', -- e.g., 'Pending', 'Completed', 'Overdue', 'Dismissed'
#     notes TEXT NULL, -- For more detailed information in the detail view
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#     FOREIGN KEY (customer_id) REFERENCES customers(id),
#     FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE SET NULL
# );