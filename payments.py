import connection
from customtkinter import *
from CTkTable import CTkTable
from forms.payments_add import AddPaymentsForm
from enum import Enum
from utils import Utils

class PaymentType(Enum):
    TYPE1 = "Airtel Money"
    TYPE2 = "Tnm Mpamba"
    TYPE3 = "Hard Cash"
    TYPE4 = "National Bank"
    TYPE5 = "Standard Bank"
    TYPE6 = "FDH Bank"

class Payments(CTkScrollableFrame):
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
        CTkButton(master=title_frame, text="Record Payment", font=("Arial", 15), text_color="#fff", fg_color="#601E88", hover_color="#9569AF", command=self._show_add_form).pack(anchor="ne", side="right")

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
                db_obj.cur.execute("""
                    SELECT p.id, c.firstname, c.lastname, v.reg_number, p.amount, p.date
                    FROM customer_payments p
                    JOIN customers c ON p.customer_id = c.id
                    JOIN vehicles v ON p.vehicle_id = v.id
                    ORDER BY p.date DESC
                """)
                self.all_payments_data = db_obj.cur.fetchall()
            finally:
                db_obj.con.close()

        # Table header: Customer, Reg Number, Amount, Date, Action (ID is hidden)
        table_display_values = [["Customer", "Reg Number", "Amount", "Date", "Action"]]
        for row in self.all_payments_data:
            customer_name = f"{row[1]} {row[2]}"
            display_row = [customer_name, row[3], row[4], row[5], "View Details"]
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
            # Get the payment ID from self.all_payments_data (row_index-1 because header is row 0)
            payment_id = self.all_payments_data[row_index - 1][0]
            self.show_payment_detail_view(payment_id)

    def show_payment_detail_view(self, payment_id):
        self.clear_frame()
        self.current_view = "detail"

        # Navigation and action buttons
        button_frame = CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20, padx=27, fill="x")
        CTkButton(button_frame, text="Back", command=self.show_payments_list_view, fg_color="#601E88", hover_color="#9569AF").pack(side="left")
        CTkButton(button_frame, text="Delete", command=lambda: Utils.delete_record("customer_payments", payment_id, self.show_payments_list_view), fg_color="#601E88", hover_color="#DD4055").pack(padx=10, side="right")
        CTkButton(button_frame, text="Update", command=self._show_add_form, fg_color="#601E88", hover_color="#9569AF").pack(side="right")

        # Title
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
                    SELECT p.id, c.firstname, c.lastname, v.make, v.model, v.reg_number, p.payment_type, p.amount, m.description, mec.firstname, mec.lastname, p.date
                    FROM customer_payments p
                    JOIN customers c ON p.customer_id = c.id
                    JOIN vehicles v ON p.vehicle_id = v.id
                    JOIN maintenances m ON p.customer_id = m.id
                    JOIN mechanics mec ON m.mechanic_id = mec.id
                    WHERE p.id = %s
                """, (payment_id,))
                record = db_obj.cur.fetchone()
                if record:
                    details_text = (
                        f"Customer: {record[1]} {record[2]}\n\n"
                        f"Vehicle Make: {record[3]}\n\n"
                        f"Vehicle Model: {record[4]}\n\n"
                        f"Vehicle Registration: {record[5]}\n\n"
                        f"Payment Type: {record[6]}\n\n"
                        f"Amount: {record[7]}\n\n"
                        f"Description: {record[8]}\n\n"
                        f"Mechanic: {record[9]} {record[10]}\n\n"
                        f"Date: {record[11]}"
                    )
            except Exception as e:
                details_text = f"Error fetching details: {e}"
            finally:
                db_obj.con.close()

        CTkLabel(self, text=details_text, font=("Arial", 14), text_color="#ffffff", justify="left", anchor="w").pack(pady=10, padx=27, anchor="w")

        # show the add form
    def _show_add_form(self):
        self.clear_frame()
        customer_options = Utils.get_options("customers", "id")
        maintenances_options = Utils.get_options("maintenances", "id")
        vehicle_options = Utils.get_options("vehicles", "id")
        reminder_type_options = [reminder.value for reminder in PaymentType]
        add_form = AddPaymentsForm(self, customer_options, maintenances_options, vehicle_options, reminder_type_options, back_command=self.show_payments_list_view)
        add_form.pack(expand=True, fill="both")