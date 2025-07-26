import connection
from customtkinter import *
from CTkTable import CTkTable
from enum import Enum
from forms.maintenances_add import AddMaintenancesForm
from utils import Utils

class ServiceType(Enum):
        TYPE1 = "Breaking system"
        TYPE2 = "Engine service"
        TYPE3 = "General service"
        TYPE4 = "Body service"
        TYPE5 = "Suspension system"

class Maintenances(CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.all_maintenances_data = [] # To store data including IDs
        self.current_view = "list" # To manage view state: "list" or "detail"

        self.show_maintenances_list_view()

    def clear_frame(self):
        """Clears all widgets from this frame."""
        for widget in self.winfo_children():
            widget.destroy()

    def show_maintenances_list_view(self):
        self.clear_frame()
        self.current_view = "list"

        # Title
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Vehicle Maintenances", font=("Arial", 25), text_color="#ffffff").pack(anchor="nw", side="left")
        CTkButton(master=title_frame, text="Set Maintenance", font=("Arial", 15), text_color="#fff", fg_color="#601E88", hover_color="#9569AF", command=self._show_add_form).pack(anchor="ne", side="right")

        self._load_and_display_maintenances_table()
    
    def _load_and_display_maintenances_table(self):
        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        self.all_maintenances_data = []
        if db_obj.con:
            try:
                # Query to get maintenance info, vehicle's reg_number
                # Assumes 'maintenances' table has 'id', 'vehicle_id', 'completion', 'date'
                query = """
                    SELECT m.id, v.reg_number, m.completion, DATE_FORMAT(m.date, '%Y-%m-%d')
                    FROM maintenances m
                    JOIN vehicles v ON m.vehicle_id = v.id
                """
                db_obj.cur.execute(query)
                self.all_maintenances_data = db_obj.cur.fetchall()
            finally:
                db_obj.con.close()

        table_display_values = [["Reg number", "Completion", "Date", "Action"]]
        for row_data in self.all_maintenances_data:
            # row_data is (id, reg_number, completion, last_service, date)
            # We display reg_number, completion, date, and "View Details" for action
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

        # Navigation and action buttons
        CTkButton(self, text="⬅️Back", command=self.show_maintenances_list_view, fg_color="#601E88", hover_color="#9569AF").pack(pady=20, padx=27)
        CTkButton(self, text="Update details", command=self._show_add_form, fg_color="#601E88", hover_color="#9569AF").pack(pady=20, padx=27, anchor="e")

        # Title page labrl
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
                # Query to get detailed maintenance info, vehicle details, and customer details
                query = """
                    SELECT
                        v.reg_number, v.make, v.model,       -- Vehicle details
                        c.firstname, c.lastname,             -- Customer details
                        m.mileage,                           -- Maintenance details
                        DATE_FORMAT(m.last_service, '%Y-%m-%d') AS formatted_last_service,
                        DATE_FORMAT(m.date, '%Y-%m-%d') AS formatted_maintenance_date,
                        m.description,
                        m.cost,
                        m.completion
                    FROM maintenances m
                    JOIN vehicles v ON m.vehicle_id = v.id
                    JOIN customers c ON v.customer_id = c.id
                    WHERE m.id = %s
                """
                db_obj.cur.execute(query, (maintenance_id,))
                record = db_obj.cur.fetchone()
                if record:
                    details_text = (
                        f"Vehicle Registration: {record[0]} ({record[1]} {record[2]})\n\n"
                        f"Owner: {record[3]} {record[4]}\n\n"
                        f"Mileage: {record[5] if record[5] is not None else 'N/A'}\n\n"
                        f"Last Service Date: {record[6] if record[6] else 'N/A'}\n\n"
                        f"Maintenance Date: {record[7] if record[7] else 'N/A'}\n\n"
                        f"Description: {record[8] if record[8] else 'N/A'}\n\n"
                        f"Cost: MWK {record[9]:.2f}" if record[9] is not None else "Cost: N/A\n\n"
                        f"Status: {record[10] if record[10] else 'N/A'}"
                    )
            except Exception as e:
                details_text = f"Error fetching details: {e}"
            finally:
                db_obj.con.close()

        # show the details
        CTkLabel(self, text=details_text, font=("Arial", 14), text_color="#ffffff", justify="left", anchor="w").pack(pady=10, padx=27, anchor="w")

    # show the add form
    def _show_add_form(self):
        self.clear_frame()
        customer_options = Utils.get_options("customers", "id")
        vehicle_options = Utils.get_options("vehicles", "id")
        mechanic_options = Utils.get_options("mechanics", "id")
        service_type_options = [service_type.value for service_type in ServiceType]
        add_form = AddMaintenancesForm(self, customer_options, vehicle_options, mechanic_options, service_type_options, back_command=self.show_maintenances_list_view)
        add_form.pack(expand=True, fill="both")