import connection
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image

class Customers(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.all_customers_data = [] # To store data including IDs
        self.current_view = "list" # To manage view state: "list" or "detail"

        self.show_customers_list_view()

    def clear_frame(self):
        # Clears all widgets from this frame.
        for widget in self.winfo_children():
            widget.destroy()

    def show_customers_list_view(self):
        self.clear_frame()
        self.current_view = "list"

        # Title
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Customers", font=("Arial", 25), text_color="#ffffff").pack(anchor="nw", side="left")
        CTkButton(master=title_frame, text="New Customer", font=("Arial", 15), text_color="#fff", fg_color="#601E88", hover_color="#9569AF").pack(anchor="ne", side="right")
        self.create_search_container()
        self._load_and_display_customers_table()

    def create_search_container(self):
        search_container = CTkFrame(master=self, height=50, fg_color="#040C15")
        search_container.pack(fill="x", pady=(45, 0), padx=27)
        CTkEntry(master=search_container, width=305, placeholder_text="Search Customer", border_color="#601E88", border_width=2).pack(side="left", padx=(13, 0), pady=15)
        CTkComboBox(master=search_container, width=125, values=["Date", "Most Recent", "Least Recent"], button_color="#601E88", border_color="#601E88", border_width=2, button_hover_color="#9569AF",dropdown_hover_color="#9569AF" , dropdown_fg_color="#030712", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)
        CTkComboBox(master=search_container, width=125, values=["Pending", "Complete", "Incomplete"], button_color="#601E88", border_color="#601E88", border_width=2, button_hover_color="#9569AF",dropdown_hover_color="#9569AF" , dropdown_fg_color="#030712", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)

    def _load_and_display_customers_table(self):
        db = connection
        dbcon_func = db.dbcon # Get the function itself
        class DummyDB: pass
        db_obj = DummyDB() # Create an object to act as 'self'
        dbcon_func(db_obj) # Call dbcon with the dummy object

        self.all_customers_data = []
        if db_obj.con: # Check if connection was successful
            try:
                # Ensure you select the 'id' column first
                db_obj.cur.execute("SELECT id, firstname, lastname, contact FROM customers")
                self.all_customers_data = db_obj.cur.fetchall()
            finally:
                db_obj.con.close()

        table_display_values = [["Firstname", "Lastname", "Contact", "Action"]]
        for row_data in self.all_customers_data:
            # row_data is (id, firstname, lastname, contact)
            # We display firstname, lastname, contact, and "View Details" for action
            display_row = list(row_data[1:]) + ["View Details"]
            table_display_values.append(display_row)

        if hasattr(self, "customers_table"):
            self.customers_table.destroy()

        self.customers_table = CTkTable(
            master=self,
            values=table_display_values,
            colors=["#030712", "#040C15"],
            header_color="#030712",
            hover_color="#9569AF",
            text_color="#ffffff",
            command=self.handle_table_action  # <-- Respond to event
        )
        self.customers_table.edit_row(0, text_color="#ffffff", hover_color="#601E88")
        self.customers_table.pack(fill="both", expand=True, padx=27, pady=(10, 0))

    def handle_table_action(self, event_data):
        row_index = event_data["row"]    # 0 is header, 1 is first data row
        col_index = event_data["column"]
        action_column_index = len(self.customers_table.values[0]) - 1

        if col_index == action_column_index and row_index > 0: # Clicked on "Action" cell in a data row
            actual_data_index = row_index - 1 # Adjust for header row
            if 0 <= actual_data_index < len(self.all_customers_data):
                customer_id = self.all_customers_data[actual_data_index][0] # Get the ID (first element)
                self.show_customer_detail_view(customer_id)

    def show_customer_detail_view(self, customer_id):
        self.clear_frame()
        self.current_view = "detail"

        CTkLabel(self, text=f"Customer Details (ID: {customer_id})", font=("Arial Black", 20), text_color="#ffffff").pack(pady=20, padx=27, anchor="w")

        # Fetch more comprehensive details from DB
        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        details_text = "Details not found."
        if db_obj.con:
            try:
                # Customize this query to fetch all relevant details for a customer
                db_obj.cur.execute("SELECT firstname, lastname, contact, email, address, payment_status, DATE_FORMAT(date_registered, '%Y-%m-%d') FROM customers WHERE id = %s", (customer_id,))
                record = db_obj.cur.fetchone()
                if record:
                    details_text = (
                        f"First Name: {record[0]}\n"
                        f"Last Name: {record[1]}\n"
                        f"Contact: {record[2]}\n"
                        f"Email: {record[3] if record[3] else 'N/A'}\n"
                        f"Address: {record[4] if record[4] else 'N/A'}\n"
                        f"Payment Status: {record[5] if record[5] else 'N/A'}\n"
                        f"Registration Date: {record[6] if record[6] else 'N/A'}"
                    )
            except Exception as e:
                details_text = f"Error fetching details: {e}"
            finally:
                db_obj.con.close()
        
        CTkLabel(self, text=details_text, font=("Arial", 14), text_color="#ffffff", justify="left", anchor="w").pack(pady=10, padx=27, anchor="w")

        CTkButton(self, text="Back to List", command=self.show_customers_list_view, fg_color="#601E88", hover_color="#9569AF").pack(pady=20, padx=27)

        if col_index == action_column_index and row_index > 0:
            # Get the customer ID from the table (first column)
            customer_id = self.customers_table.values[row_index][0]
            self.show_customer_detail_view(customer_id)