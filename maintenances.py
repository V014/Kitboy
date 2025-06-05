import connection
from customtkinter import *
from CTkTable import CTkTable
from forms.maintenance_form import MaintenanceForm

class Maintenances(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        # Title
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Vehicle Maintenances", font=("Arial Black", 25), text_color="#ffffff").pack(anchor="nw", side="left")
        CTkButton(master=title_frame, text="+ New Job", font=("Arial Black", 15), text_color="#fff", fg_color="#601E88", hover_color="#207244", command=self.open_form).pack(anchor="ne", side="right")

    def open_form(self):
        # Fetch data from your DB here:
        customers = self.fetch_customers()   # e.g., ["John Doe", "Jane Smith"]
        cars = self.fetch_cars()             # e.g., ["Toyota Corolla", "Honda Civic"]
        mechanics = self.fetch_mechanics()   # e.g., ["Mike", "Anna"]

        def on_submit(data):
            # Save to DB or process as needed
            print("Job assigned:", data)

        MaintenanceForm(self, customers, cars, mechanics, on_submit)

    def fetch_maintenances(self):
        # Replace with actual DB query
        return ["John Doe", "Jane Smith"]

    def fetch_cars(self):
        # Replace with actual DB query
        return ["Toyota Corolla", "Honda Civic"]

    def fetch_mechanics(self):
        # Replace with actual DB query
        return ["Mike", "Anna"]
    
    def load_customers_data(self):
        db = connection
        dbcon_func = db.dbcon # Get the function itself
        class DummyDB: pass
        db_obj = DummyDB() # Create an object to act as 'self'
        dbcon_func(db_obj) # Call dbcon with the dummy object

        maintenances = []
        if db_obj.con: # Check if connection was successful
            try:
                db_obj.cur.execute("SELECT id, firstname, lastname, contact FROM customers")
                maintenances = db_obj.cur.fetchall()
            finally:
                db_obj.con.close()

        table_data = [["ID", "Firstname", "Lastname", "Contact", "Action"]]
        table_data.extend([list(row) for row in maintenances])

        if hasattr(self, "maintenances_table"):
            self.maintenances_table.destroy()

        self.maintenances_table = CTkTable(
            master=self,
            values=table_data,
            colors=["#030712", "#040C15"],
            header_color="#601E88",
            hover_color="#9569AF",
            text_color="#ffffff"
        )
        self.maintenances_table.edit_row(0, text_color="#ffffff", hover_color="#601E88")
        self.maintenances_table.pack(fill="both", expand=True, padx=27, pady=(10, 0))