import connection
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image

class Customers(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        # Title
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Customers", font=("Arial Black", 25), text_color="#ffffff").pack(anchor="nw", side="left")
        CTkButton(master=title_frame, text="+ New Customer", font=("Arial Black", 15), text_color="#fff", fg_color="#601E88", hover_color="#9569AF").pack(anchor="ne", side="right")

        self.load_customers_data()

    def load_customers_data(self):
        db = connection
        dbcon_func = db.dbcon # Get the function itself
        class DummyDB: pass
        db_obj = DummyDB() # Create an object to act as 'self'
        dbcon_func(db_obj) # Call dbcon with the dummy object

        customers = []
        if db_obj.con: # Check if connection was successful
            try:
                db_obj.cur.execute("SELECT id, firstname, lastname, contact FROM customers")
                customers = db_obj.cur.fetchall()
            finally:
                db_obj.con.close()

        table_data = [["ID", "Firstname", "Lastname", "Contact"]]
        table_data.extend([list(row) for row in customers])

        if hasattr(self, "customers_table"):
            self.customers_table.destroy()

        self.customers_table = CTkTable(
            master=self,
            values=table_data,
            colors=["#E6E6E6", "#EEEEEE"],
            header_color="#601E88",
            hover_color="#B4B4B4"
        )
        self.customers_table.edit_row(0, text_color="#fff", hover_color="#601E88")
        self.customers_table.pack(fill="both", expand=True, padx=27, pady=(10, 0))