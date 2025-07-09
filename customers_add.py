from customtkinter import *

class AddCustomerForm(CTkFrame):
    def __init__(self, master, back_command, **kwargs):
        super().__init__(master, **kwargs)

        self.back_command = back_command
        self.configure(fg_color="transparent")

        # Title
        CTkLabel(master=self, text="Add New Customer", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pady=(29,0), padx=27)

        # Full Name
        CTkLabel(master=self, text="Full Name", font=("Arial Bold", 17), text_color="#fff").pack(anchor="nw", pady=(25,0), padx=27)
        self.name_entry = CTkEntry(master=self, fg_color="#040C15", border_color="#601E88", border_width=2, height=50)
        self.name_entry.pack(fill="x", pady=(12,0), padx=27)

        # Grid for other details
        grid = CTkFrame(master=self, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=27, pady=(31,0))
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        # Email
        CTkLabel(master=grid, text="Email Address", font=("Arial Bold", 17), text_color="#fff", justify="left").grid(row=0, column=0, sticky="w")
        self.email_entry = CTkEntry(master=grid, fg_color="#040C15", border_color="#601E88", border_width=2, height=50)
        self.email_entry.grid(row=1, column=0, sticky="ew", padx=(0, 12))

        # Phone Number
        CTkLabel(master=grid, text="Phone Number", font=("Arial Bold", 17), text_color="#fff", justify="left").grid(row=0, column=1, sticky="w", padx=(12,0))
        self.phone_entry = CTkEntry(master=grid, fg_color="#040C15", border_color="#601E88", border_width=2, height=50)
        self.phone_entry.grid(row=1, column=1, sticky="ew", padx=(12,0))

        # Address
        CTkLabel(master=grid, text="Address", font=("Arial Bold", 17), text_color="#fff", justify="left").grid(row=2, column=0, columnspan=2, sticky="w", pady=(38, 0))
        self.address_textbox = CTkTextbox(master=grid, fg_color="#040C15", border_color="#601E88", border_width=2)
        self.address_textbox.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(16, 0))
        grid.grid_rowconfigure(3, weight=1) # Allow textbox to expand vertically

        # Action Buttons
        actions = CTkFrame(master=self, fg_color="transparent")
        actions.pack(side="bottom", fill="x", pady=(20, 20), padx=27)
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)

        CTkButton(master=actions, text="Back", height=50, fg_color="transparent", font=("Arial Bold", 17), border_color="#601E88", hover_color="#25192f", border_width=2, text_color="#fff", command=self.back_command).grid(row=0, column=0, sticky="ew", padx=(0, 12))
        CTkButton(master=actions, text="Add Customer", height=50, font=("Arial Bold", 17), hover_color="#9569AF", fg_color="#601E88", text_color="#fff", command=self._add_customer_handler).grid(row=0, column=1, sticky="ew", padx=(12, 0))

    def _add_customer_handler(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        address = self.address_textbox.get("1.0", "end-1c")
        print(f"Adding Customer:\nName: {name}\nEmail: {email}\nPhone: {phone}\nAddress: {address}")
        # Here you would add the logic to save the customer to a database or file
        # After saving, you can call the back_command to return to the list
        self.back_command()