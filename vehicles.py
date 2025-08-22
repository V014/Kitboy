from customtkinter import *
from CTkTable import CTkTable
from utils import Utils
from forms.vehicle_add import AddVehicleForm
from enum import Enum

# list of transmission types
class TransmissionType(Enum):
    TYPE1 = "Manual"
    TYPE2 = "Automatic"

class Vehicles(CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.all_vehicles_data = [] # To store data including IDs
        self.current_view = "list" # To manage view state: "list" or "detail"

        self.show_vehicles_list_view()

    def clear_frame(self):
        # Clears all widgets from this frame.
        for widget in self.winfo_children():
            widget.destroy()

    def show_vehicles_list_view(self):
        self.clear_frame()
        self.current_view = "list"

        # Title
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Vehicles", font=("Arial", 25), text_color="#ffffff").pack(anchor="nw", side="left")
        CTkButton(master=title_frame, text="Add Vehicle", font=("Arial", 15), text_color="#fff", fg_color="#601E88", hover_color="#9569AF", command=self._show_add_form).pack(anchor="ne", side="right")
        
        self._load_and_display_vehicles_table()

    def _load_and_display_vehicles_table(self):
        import connection
        db = connection
        dbcon_func = db.dbcon # Get the function itself
        class DummyDB: pass
        db_obj = DummyDB() # Create an object to act as 'self'
        dbcon_func(db_obj) # Call dbcon with the dummy object

        self.all_vehicles_data = []
        if db_obj.con: # Check if connection was successful
            try:
                # Ensure you select the 'id' column first
                # Query to get vehicle info and customer's name
                query = """
                    SELECT v.id, v.reg_number, v.make, v.model, c.firstname, c.lastname
                    FROM vehicles v
                    JOIN customers c ON v.customer_id = c.id
                """
                db_obj.cur.execute(query)
                self.all_vehicles_data = db_obj.cur.fetchall()
            finally:
                db_obj.con.close()

        table_display_values = [["Reg Number", "Make", "Model", "Owner", "Action"]]
        for row_data in self.all_vehicles_data:
            owner_name = f"{row_data[4]} {row_data[5]}" # Combine firstname and lastname
            display_row = [row_data[1], row_data[2], row_data[3], owner_name, "View Details"]
            table_display_values.append(display_row)

        if hasattr(self, "vehicles_table"):
            self.vehicles_table.destroy()

        self.vehicles_table = CTkTable(
            master=self,
            values=table_display_values,
            colors=["#030712", "#040C15"],
            header_color="#601E88",
            hover_color="#9569AF",
            text_color="#ffffff",
            command=self.handle_table_action  # <-- Respond to event
        )
        self.vehicles_table.edit_row(0, text_color="#ffffff", hover_color="#601E88")
        self.vehicles_table.pack(fill="both", expand=True, padx=27, pady=(10, 0))

    def handle_table_action(self, event_data):
        row_index = event_data["row"]    # 0 is header, 1 is first data row
        col_index = event_data["column"]
        action_column_index = len(self.vehicles_table.values[0]) - 1

        if col_index == action_column_index and row_index > 0: # Clicked on "Action" cell in a data row
            actual_data_index = row_index - 1 # Adjust for header row
            if 0 <= actual_data_index < len(self.all_vehicles_data):
                vehicle_id = self.all_vehicles_data[actual_data_index][0] # Get the vehicle ID (first element)
                self.show_vehicle_detail_view(vehicle_id)

    def show_vehicle_detail_view(self, vehicle_id):
        self.clear_frame()
        self.current_view = "detail"

        # Navigation and action buttons
        button_frame = CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20, padx=27, fill="x")
        CTkButton(button_frame, text="Back", command=self.show_vehicles_list_view, fg_color="#601E88", hover_color="#9569AF").pack(side="left")
        CTkButton(button_frame, text="Delete", command=lambda: Utils.delete_record("vehicles", vehicle_id, self.show_vehicles_list_view), fg_color="#601E88", hover_color="#DD4055").pack(padx=10, side="right")
        CTkButton(button_frame, text="Update", command=lambda: self._show_add_form(vehicle_id), fg_color="#601E88", hover_color="#9569AF").pack(side="right")

        # Title
        CTkLabel(self, text=f"Vehicle Details (ID: {vehicle_id})", font=("Arial Black", 20), text_color="#ffffff").pack(pady=20, padx=27, anchor="w")

        # Fetch more comprehensive details from DB
        import connection
        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        details_text = "Vehicle details not found."
        if db_obj.con:
            try:
                # Query to get detailed vehicle info and customer's name
                query = """
                    SELECT v.reg_number, v.make, v.model, v.year, v.color, v.vin_number, c.firstname, c.lastname, c.contact AS customer_contact
                    FROM vehicles v
                    JOIN customers c ON v.customer_id = c.id
                    WHERE v.id = %s
                """
                db_obj.cur.execute(query, (vehicle_id,))
                record = db_obj.cur.fetchone()
                if record:
                    details_text = (
                        f"Registration Number: {record[0]}\n\n"
                        f"Make: {record[1]}\n\n"
                        f"Model: {record[2]}\n\n"
                        f"Year: {record[3] if record[3] else 'N/A'}\n\n"
                        f"Color: {record[4] if record[4] else 'N/A'}\n\n"
                        f"VIN Number: {record[5] if record[5] else 'N/A'}\n\n"
                        f"Owner: {record[6]} {record[7]}\n\n"
                        f"Owner Contact: {record[8] if record[8] else 'N/A'}"
                    )
            except Exception as e:
                details_text = f"Error fetching details: {e}"
            finally:
                db_obj.con.close()
        
        CTkLabel(self, text=details_text, font=("Arial", 14), text_color="#ffffff", justify="left", anchor="w").pack(pady=10, padx=27, anchor="w")

    def get_customer_options(self):
        import connection
        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)
        options = []
        if db_obj.con:
            try:
                db_obj.cur.execute("SELECT id FROM customers")
                options = [str(row[0]) for row in db_obj.cur.fetchall()]
            finally:
                db_obj.con.close()
        return options

    def _show_add_form(self, vehicle_id=None):
        self.clear_frame()
        customer_options = self.get_customer_options()
        transmission_type_options = [transmission_type.value for transmission_type in TransmissionType]

        add_form = AddVehicleForm(
            self, 
            customer_options,
            transmission_type_options, 
            back_command=self.show_vehicles_list_view,
            vehicle_id=vehicle_id)
        
        add_form.pack(expand=True, fill="both")