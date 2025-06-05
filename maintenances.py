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

        self.details_frame = CTkFrame(self, fg_color="#040C15")
        self.details_frame.pack(fill="x", padx=27, pady=(0, 10))
        self.details_label = CTkLabel(self.details_frame, text="", text_color="#fff", font=("Arial", 13), anchor="w", justify="left")
        self.details_label.pack(anchor="w", padx=10, pady=10)

        self.load_maintenances_data()

    def open_form(self):
        # Fetch data from your DB here:

        def on_submit(data):
            # Save to DB or process as needed
            print("Job assigned:", data)

        MaintenanceForm(self, on_submit)
    
    def load_maintenances_data(self):
        db = connection
        dbcon_func = db.dbcon # Get the function itself
        class DummyDB: pass
        db_obj = DummyDB() # Create an object to act as 'self'
        dbcon_func(db_obj) # Call dbcon with the dummy object

        maintenances = []
        if db_obj.con: # Check if connection was successful
            try:
                db_obj.cur.execute("SELECT reg_number, mileage, last_service, date FROM maintenances")
                maintenances = db_obj.cur.fetchall()
            finally:
                db_obj.con.close()

        table_data = [["Reg number", "Mileage", "Last Service", "Date", "Action"]]
        for row in maintenances:
            table_data.append(list(row) + ["More"])

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

        # Bind row click event
        self.maintenances_table.bind("<ButtonRelease-1>", self.on_row_click)

    def on_row_click(self, event):
        row_index = self.maintenances_table.get_selected_row()
        print("row_index:", row_index, type(row_index))  # Debug print

        # Handle if row_index is a dict or string
        if isinstance(row_index, dict):
            row_index = int(row_index.get("row", 0))
        elif isinstance(row_index, str):
            row_index = int(row_index)

        if row_index > 0:
            row_data = self.maintenances_table.get_row(row_index)
            details = (
                f"Reg Number: {row_data[0]}\n"
                f"Mileage: {row_data[1]}\n"
                f"Last Service: {row_data[2]}\n"
                f"Date: {row_data[3]}"
            )
            self.details_label.configure(text=details)
        else:
            self.details_label.configure(text="")