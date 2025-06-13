import connection
from customtkinter import *
from CTkTable import CTkTable
from forms.maintenance_form import MaintenanceForm

class Maintenances(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.all_maintenances_data = [] # To store data including IDs
        self.current_view = "list" # To manage view state: "list" or "detail"

        self.show_maintenances_list_view()
    
    def create_search_container(self):
        search_container = CTkFrame(master=self, height=50, fg_color="#040C15")
        search_container.pack(fill="x", pady=(45, 0), padx=27)
        CTkEntry(master=search_container, width=305, placeholder_text="Search Job", border_color="#601E88", border_width=2).pack(side="left", padx=(13, 0), pady=15)
        CTkComboBox(master=search_container, width=125, values=["Date", "Most Recent Order", "Least Recent Order"], button_color="#601E88", border_color="#601E88", border_width=2, button_hover_color="#9569AF",dropdown_hover_color="#9569AF" , dropdown_fg_color="#030712", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)
        CTkComboBox(master=search_container, width=125, values=["Status", "Processing", "Confirmed", "Packing", "Shipping", "Delivered", "Cancelled"], button_color="#601E88", border_color="#601E88", border_width=2, button_hover_color="#9569AF",dropdown_hover_color="#9569AF" , dropdown_fg_color="#030712", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)

    def clear_frame(self):
        """Clears all widgets from this frame."""
        for widget in self.winfo_children():
            widget.destroy()

    def show_maintenances_list_view(self):
        """Clears the frame and displays the list of maintenances."""
        self.clear_frame()
        self.current_view = "list"

        # Title
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Vehicle Maintenances", font=("Arial Black", 25), text_color="#ffffff").pack(anchor="nw", side="left")
        CTkButton(master=title_frame, text="+ New Job", font=("Arial Black", 15), text_color="#fff", fg_color="#601E88", hover_color="#9569AF", command=self.open_form).pack(anchor="ne", side="right")

        self._load_and_display_maintenances_table()

    def open_form(self):
        def on_submit(data):
            # Save to DB or process as needed
            print("Job assigned:", data)
            # Refresh the list view after a new job is submitted
            if self.current_view == "list":
                self.show_maintenances_list_view()
            elif hasattr(self.master, 'show_page'): # If called from main app context
                self.master.show_page("maintenances")

        MaintenanceForm(self, on_submit)
    
    def _load_and_display_maintenances_table(self):
        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        self.all_maintenances_data = []
        if db_obj.con:
            try:
                # Ensure you select the 'id' column
                db_obj.cur.execute("SELECT id, reg_number, mileage, last_service, date FROM maintenances")
                self.all_maintenances_data = db_obj.cur.fetchall()
            finally:
                db_obj.con.close()

        table_display_values = [["Reg number", "Mileage", "Last Service", "Date", "Action"]]
        for row_data in self.all_maintenances_data:
            # row_data is (id, reg_number, mileage, last_service, date)
            # We display all except ID, and add "View Details" for action
            display_row = list(row_data[1:]) + ["View Details"]
            table_display_values.append(display_row)

        if hasattr(self, "maintenances_table"):
            self.maintenances_table.destroy()

        self.maintenances_table = CTkTable(
            master=self,
            values=table_display_values,
            colors=["#030712", "#040C15"],
            header_color="#601E88",
            hover_color="#9569AF",
            text_color="#ffffff",
            command=self.handle_table_action # Add command to handle cell clicks
        )
        self.maintenances_table.edit_row(0, text_color="#ffffff", hover_color="#601E88")
        self.maintenances_table.pack(fill="both", expand=True, padx=27, pady=(10, 0))

    def handle_table_action(self, event_data):
        row_index = event_data["row"]    # 0 is header, 1 is first data row
        col_index = event_data["column"]
        
        # Last column is "Action"
        action_column_index = len(self.maintenances_table.values[0]) - 1

        if col_index == action_column_index and row_index > 0: # Clicked on "Action" cell in a data row
            actual_data_index = row_index - 1 # Adjust for header row to get index in self.all_maintenances_data
            if 0 <= actual_data_index < len(self.all_maintenances_data):
                maintenance_id = self.all_maintenances_data[actual_data_index][0] # Get the ID (first element)
                self.show_maintenance_detail_view(maintenance_id)

    def show_maintenance_detail_view(self, maintenance_id):
        self.clear_frame()
        self.current_view = "detail"

        CTkLabel(self, text=f"Maintenance Details (ID: {maintenance_id})", font=("Arial Black", 20), text_color="#ffffff").pack(pady=20, padx=27, anchor="w")

        # Fetch more comprehensive details from DB
        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        details_text = "Details not found."
        if db_obj.con:
            try:
                # Customize this query to fetch all relevant details for a maintenance item
                db_obj.cur.execute("SELECT reg_number, mileage, last_service, date, description, date, cost FROM maintenances WHERE id = %s", (maintenance_id,))
                record = db_obj.cur.fetchone()
                if record:
                    details_text = (
                        f"Registration Number: {record[0]}\n"
                        f"Mileage: {record[1]}\n"
                        f"Last Service Date: {record[2]}\n"
                        f"Maintenance Date: {record[3]}\n"
                        f"Description: {record[4] if record[4] else 'N/A'}\n"
                        f"Date: {record[5] if record[5] else 'N/A'}\n"
                        f"Cost: ${record[6]:.2f}" if record[6] is not None else "Cost: N/A"
                    )
            except Exception as e:
                details_text = f"Error fetching details: {e}"
            finally:
                db_obj.con.close()
        
        CTkLabel(self, text=details_text, font=("Arial", 14), text_color="#ffffff", justify="left", anchor="w").pack(pady=10, padx=27, anchor="w")

        CTkButton(self, text="Back to List", command=self.show_maintenances_list_view, fg_color="#601E88", hover_color="#9569AF").pack(pady=20, padx=27)