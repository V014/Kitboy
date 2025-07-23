import connection
from customtkinter import *
from CTkTable import CTkTable
from forms.mechanics_add import AddMechanicForm

class Mechanics(CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.all_mechanics_data = []  # To store data including IDs
        self.current_view = "list"  # To manage view state: "list" or "detail"

        self.show_mechanics_list_view()

    def clear_frame(self):
        # Clears all widgets from this frame.
        for widget in self.winfo_children():
            widget.destroy()

    def show_mechanics_list_view(self):
        self.clear_frame()
        self.current_view = "list"

        # Title
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Mechanics", font=("Arial", 25), text_color="#ffffff").pack(anchor="nw", side="left")
        CTkButton(master=title_frame, text="Add Mechanic", font=("Arial", 15), text_color="#fff", fg_color="#601E88", hover_color="#9569AF", command=self._show_add_form).pack(anchor="ne", side="right")

        self._load_and_display_mechanics_table()

    def _load_and_display_mechanics_table(self):
        db = connection
        dbcon_func = db.dbcon  # Get the function itself
        class DummyDB: pass
        db_obj = DummyDB() # Create an object to act as 'self'
        dbcon_func(db_obj)  # Call dbcon with the dummy object

        if db_obj.con: # Check if connection was successful
            try:
                # Ensure you select the 'id' column first
                # Query to get mechanic's info
                query = """
                    SELECT id, firstname, lastname, identification, certification, specification
                    FROM mechanics
                    """
                db_obj.cur.execute(query)
                self.all_mechanics_data = db_obj.cur.fetchall()
            finally:
                db_obj.con.close()

        table_display_values = [["Name", "Identification", "Certification", "Specification", "Action"]]
        for row_data in self.all_mechanics_data:
            mechanics_name = f"{row_data[1]} {row_data[2]}" # Combile firstname and lastname
            display_row = [mechanics_name, row_data[3], row_data[4], row_data[5], "View Details"]
            table_display_values.append(display_row)

        if hasattr(self, "mechanics_table"):
            self.mechanics_table.destroy()

        self.mechanics_table = CTkTable(
            master=self,
            values=table_display_values,
            colors=["#030712", "#040C15"],
            header_color="#030712",
            hover_color="#9569AF",
            text_color="#ffffff",
            command=self.handle_table_action  # <-- Respond to event
        )
        self.mechanics_table.edit_row(0, text_color="#ffffff", hover_color="#601E88")
        self.mechanics_table.pack(fill="both", expand=True, padx=27, pady=(10, 0))

    def handle_table_action(self, event_data):
        row_index = event_data["row"]    # 0 is header, 1 is first data row
        col_index = event_data["column"]
        action_column_index = len(self.mechanics_table.values[0]) - 1

        if col_index == action_column_index and row_index > 0: # Clicked on "Action" cell in a data row
            actual_data_index = row_index - 1 # Adjust for header row
            if 0 <= actual_data_index < len(self.all_mechanics_data):
                mechanic_id = self.all_mechanics_data[actual_data_index][0] # Get the mechanics ID (first element)
                self.show_mechanic_details_view(mechanic_id)

    def show_mechanic_details_view(self, mechanic_id):
        self.clear_frame()
        self.current_view = "details"

        CTkLabel(self, text=f"Mechanic Details (ID: {mechanic_id})", font=("Arial Black", 20), text_color="#ffffff").pack(pady=20, padx=27, anchor="w")

        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        details_text = "Mechanics details not found."
        if db_obj.con:
            try:
                query = """
                    SELECT firstname, lastname, identification, certification, certified_on, institute, skills, specification, date_registered
                    FROM mechanics WHERE id = %s"""
                db_obj.cur.execute(query, (mechanic_id,))
                record = db_obj.cur.fetchone()
                if record:
                    details_text = (
                        f"Firstname: {record[0]}\n"
                        f"Lastname: {record[1]}\n"
                        f"Identification: {record[2]}\n"
                        f"Certification: {record[3]}\n"
                        f"Certified on: {record[4]}\n"
                        f"Institute: {record[5]}\n"
                        f"Skills: {record[6]}\n"
                        f"Specification: {record[7]}\n"
                        f"Date Registered: {record[8]}\n"
                    )
            except Exception as e:
                details_text = f"Error fetching details: {e}"
            finally:
                db_obj.con.close()
        
        CTkLabel(self, text=details_text, font=("Arial", 14), text_color="#ffffff", justify="left", anchor="w").pack(pady=10, padx=27, anchor="w")
        CTkButton(self, text="Back to List", command=self.show_mechanics_list_view, fg_color="#601E88", hover_color="#9569AF").pack(pady=20, padx=27)

    def _show_add_form(self):
        self.clear_frame()
        add_form = AddMechanicForm(self, back_command=self.show_mechanics_list_view)
        add_form.pack(expand=True, fill="both")