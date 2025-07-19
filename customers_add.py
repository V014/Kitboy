from customtkinter import *
from tkinter import messagebox

class AddCustomerForm(CTkFrame):
    def __init__(self, master, back_command=None):
        super().__init__(master, fg_color="transparent")
        self.back_command = back_command

        CTkLabel(self, text="Add Customer", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pady=(29,0), padx=27)

        grid = CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", padx=27, pady=(31,0))

        # First Name
        CTkLabel(grid, text="First Name", font=("Arial Bold", 17), text_color="#fff").grid(row=0, column=0, sticky="w")
        self.firstname_entry = CTkEntry(grid, fg_color="#F0F0F0", border_width=0, width=300)
        self.firstname_entry.grid(row=1, column=0, ipady=10)

        # Last Name
        CTkLabel(grid, text="Last Name", font=("Arial Bold", 17), text_color="#fff").grid(row=0, column=1, sticky="w", padx=(25,0))
        self.lastname_entry = CTkEntry(grid, fg_color="#F0F0F0", border_width=0, width=300)
        self.lastname_entry.grid(row=1, column=1, ipady=10, padx=(24,0))

        # Contact
        CTkLabel(grid, text="Contact", font=("Arial Bold", 17), text_color="#fff").grid(row=2, column=0, sticky="w", pady=(38, 0))
        self.contact_entry = CTkEntry(grid, fg_color="#F0F0F0", border_width=0, width=300)
        self.contact_entry.grid(row=3, column=0, ipady=10, pady=(16,0))

        # Email
        CTkLabel(grid, text="Email", font=("Arial Bold", 17), text_color="#fff").grid(row=2, column=1, sticky="w", pady=(38, 0), padx=(25,0))
        self.email_entry = CTkEntry(grid, fg_color="#F0F0F0", border_width=0, width=300)
        self.email_entry.grid(row=3, column=1, ipady=10, padx=(24,0), pady=(16,0))

        # Address
        CTkLabel(grid, text="Address", font=("Arial Bold", 17), text_color="#fff").grid(row=4, column=0, sticky="w", pady=(38, 0))
        self.address_entry = CTkEntry(grid, fg_color="#F0F0F0", border_width=0, width=300)
        self.address_entry.grid(row=5, column=0, ipady=10, pady=(16,0))

        # Actions
        actions = CTkFrame(self, fg_color="transparent")
        actions.pack(fill="both")

        CTkButton(actions, text="Back", width=100, fg_color="transparent", font=("Arial Bold", 17), border_color="#601E88", hover_color="#eee", border_width=2, text_color="#601E88", command=self.back_command).pack(side="left", anchor="sw", pady=(30,0), padx=(27,24))
        CTkButton(actions, text="Add", width=100, font=("Arial Bold", 17), hover_color="#9569AF", fg_color="#601E88", text_color="#fff", command=self.add_customer).pack(side = "left", anchor="se", pady=(30,0), padx=(0,27))

    def add_customer(self):
        import connection
        firstname = self.firstname_entry.get().strip()
        lastname = self.lastname_entry.get().strip()
        contact = self.contact_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if not firstname or not lastname or not contact:
            messagebox.showerror("Error", "First name, last name, and contact are required.")
            return

        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        if db_obj.con:
            try:
                db_obj.cur.execute(
                    "INSERT INTO customers (firstname, lastname, contact, email, address) VALUES (%s, %s, %s, %s, %s)",
                    (firstname, lastname, contact, email, address)
                )
                db_obj.con.commit()
                messagebox.showinfo("Success", "Customer added successfully!")
                if self.back_command:
                    self.back_command()
            except Exception as e:
                messagebox.showerror("Database Error", f"Could not add customer: {e}")
            finally:
                db_obj.con.close()