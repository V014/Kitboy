import connection
from customtkinter import *
from CTkTable import CTkTable
from utils import Utils
from forms.customers_add import AddCustomerForm

class Customers(CTkScrollableFrame):
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
        CTkButton(master=title_frame, text="New Customer", font=("Arial", 15), text_color="#fff", fg_color="#601E88", hover_color="#9569AF", command=self._show_add_form).pack(anchor="ne", side="right")

        self._load_and_display_customers_table()

    def _show_add_form(self, customer_id=NONE):
        self.clear_frame()

        add_form = AddCustomerForm(
            self,  
            back_command=self.show_customers_list_view, 
            customer_id=customer_id
        )
        add_form.pack(expand=True, fill="both")

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
            display_row = list(row_data[1:]) + ["View Details"]
            table_display_values.append(display_row)

        if hasattr(self, "customers_table"):
            self.customers_table.destroy()

        self.customers_table = CTkTable(
            master=self,
            values=table_display_values,
            colors=["#030712", "#040C15"],
            header_color="#601E88",
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

        # Navigation and action buttons
        button_frame = CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20, padx=27, fill="x")
        CTkButton(button_frame, text="Back", command=self.show_customers_list_view, fg_color="#601E88", hover_color="#9569AF").pack(side="left")
        CTkButton(button_frame, text="Delete", command=lambda: Utils.delete_record("customers", customer_id, self.show_customers_list_view), fg_color="#601E88", hover_color="#DD4055").pack(padx=10, side="right")
        CTkButton(button_frame, text="Update", command=lambda: self._show_add_form(customer_id), fg_color="#601E88", hover_color="#9569AF").pack(side="right")

        # Title
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
                db_obj.cur.execute(
                    "SELECT firstname, lastname, contact, email, address, payment_status, DATE_FORMAT(date_registered, '%Y-%m-%d') FROM customers WHERE id = %s",
                    (customer_id,)
                )
                record = db_obj.cur.fetchone()
                if record:
                    details_text = (
                        f"First Name: {record[0]}\n\n"
                        f"Last Name: {record[1]}\n\n"
                        f"Contact: {record[2]}\n\n"
                        f"Email: {record[3] if record[3] else 'N/A'}\n\n"
                        f"Address: {record[4] if record[4] else 'N/A'}\n\n"
                        f"Payment Status: {record[5] if record[5] else 'N/A'}\n\n"
                        f"Registration Date: {record[6] if record[6] else 'N/A'}"
                    )
            except Exception as e:
                details_text = f"Error fetching details: {e}"
            finally:
                db_obj.con.close()

        CTkLabel(self, text=details_text, font=("Arial", 14), text_color="#ffffff", justify="left", anchor="w").pack(pady=10, padx=27, anchor="w")

    def update_customer_payment_status(customer_id):
        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        if db_obj.con:
            try:
                # Get all maintenances for this customer
                db_obj.cur.execute("SELECT id, cost FROM maintenances WHERE customers_id = %s", (customer_id,))
                maintenances = db_obj.cur.fetchall()

                # Get all payments for this customer
                db_obj.cur.execute("SELECT maintenance_id, amount FROM customer_payments WHERE customer_id = %s", (customer_id,))
                payments = db_obj.cur.fetchall()

                # Map maintenance_id to cost
                maintenance_costs = {m[0]: float(m[1]) for m in maintenances}
                # Map maintenance_id to total paid
                paid = {}
                for p in payments:
                    paid[p[0]] = paid.get(p[0], 0) + float(p[1])

                # Check payment status for each maintenance
                all_complete = True
                any_paid = False
                for mid, cost in maintenance_costs.items():
                    paid_amount = paid.get(mid, 0)
                    if paid_amount >= cost:
                        any_paid = True
                    else:
                        all_complete = False
                        if paid_amount > 0:
                            any_paid = True

                if all_complete and maintenance_costs:
                    status = 'complete'
                elif any_paid:
                    status = 'pending'
                else:
                    status = 'incomplete'

                # Update the customer table
                db_obj.cur.execute("UPDATE customers SET payment_status = %s WHERE id = %s", (status, customer_id))
                db_obj.con.commit()
            finally:
                db_obj.con.close()