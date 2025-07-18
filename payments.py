import connection
from customtkinter import *
from CTkTable import CTkTable

class Payments(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.all_payments_data = []
        self.current_view = "list"
        self.show_payments_list_view()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_payments_list_view(self):
        self.clear_frame()
        self.current_view = "list"

        # Title
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Customer Payments", font=("Arial", 25), text_color="#ffffff").pack(anchor="nw", side="left")

        self._load_and_display_payments_table()

    def _load_and_display_payments_table(self):
        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        self.all_payments_data = []
        if db_obj.con:
            try:
                # Join with customers, vehicles, maintenances for richer info
                db_obj.cur.execute("""
                    SELECT p.id, c.firstname, c.lastname, v.reg_number, m.service_type, p.method, p.amount, p.recipt_number, p.date
                    FROM customer_payments p
                    JOIN customers c ON p.customer_id = c.id
                    JOIN vehicles v ON p.vehicle_id = v.id
                    JOIN maintenances m ON p.maintenance_id = m.id
                    ORDER BY p.date DESC
                """)
                self.all_payments_data = db_obj.cur.fetchall()
            finally:
                db_obj.con.close()

        table_display_values = [["ID", "First Name", "Last Name", "Reg Number", "Service", "Method", "Amount", "Receipt", "Date", "Action"]]
        for row in self.all_payments_data:
            display_row = list(row) + ["View Details"]
            table_display_values.append(display_row)

        if hasattr(self, "payments_table"):
            self.payments_table.destroy()

        self.payments_table = CTkTable(
            master=self,
            values=table_display_values,
            colors=["#030712", "#040C15"],
            header_color="#601E88",
            hover_color="#9569AF",
            text_color="#ffffff",
            command=self.handle_table_action
        )
        self.payments_table.edit_row(0, text_color="#ffffff", hover_color="#601E88")
        self.payments_table.pack(fill="both", expand=True, padx=27, pady=(10, 0))

    def handle_table_action(self, event_data):
        row_index = event_data["row"]
        col_index = event_data["column"]
        action_column_index = len(self.payments_table.values[0]) - 1

        if col_index == action_column_index and row_index > 0:
            payment_id = self.payments_table.values[row_index][0]
            self.show_payment_detail_view(payment_id)

    def show_payment_detail_view(self, payment_id):
        self.clear_frame()
        self.current_view = "detail"

        CTkLabel(self, text=f"Payment Details (ID: {payment_id})", font=("Arial Black", 20), text_color="#ffffff").pack(pady=20, padx=27, anchor="w")

        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        details_text = "Payment details not found."
        if db_obj.con:
            try:
                db_obj.cur.execute("""
                    SELECT p.id, c.firstname, c.lastname, v.reg_number, m.service_type, p.method, p.amount, p.recipt_number, p.date
                    FROM customer_payments p
                    JOIN customers c ON p.customer_id = c.id
                    JOIN vehicles v ON p.vehicle_id = v.id
                    JOIN maintenances m ON p.maintenance_id = m.id
                    WHERE p.id = %s
                """, (payment_id,))
                record = db_obj.cur.fetchone()
                if record:
                    details_text = (
                        f"Payment ID: {record[0]}\n"
                        f"Customer: {record[1]} {record[2]}\n"
                        f"Vehicle Reg: {record[3]}\n"
                        f"Service: {record[4]}\n"
                        f"Method: {record[5]}\n"
                        f"Amount: {record[6]}\n"
                        f"Receipt #: {record[7]}\n"
                        f"Date: {record[8]}"
                    )
            except Exception as e:
                details_text = f"Error fetching details: {e}"
            finally:
                db_obj.con.close()

        CTkLabel(self, text=details_text, font=("Arial", 14), text_color="#ffffff", justify="left", anchor="w").pack(pady=10, padx=27, anchor="w")
        CTkButton(self, text="Back to List", command=self.show_payments_list_view, fg_color="#601E88", hover_color="#9569AF").pack(pady=20, padx=27)