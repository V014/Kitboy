import os
from customtkinter import *
import pywinstyles
from PIL import Image
from dashboard import Dashboard
from maintenances import Maintenances
from customers import Customers
from vehicles import Vehicles
from mechanics import Mechanics
from reminders import Reminders
from payments import Payments

class KitboyApp(CTk):
    def __init__(self): # constructor
        super().__init__() # inherit from custom tkinter
        self.setup_environment() # call method that identifies files in root folder
        self.setup_window() # call method that sets the ui theme and resolution
        self.create_sidebar() # call sidebar first 
        self.create_main_view() # call view after

    def setup_environment(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    def setup_window(self):
        self.geometry("856x645")
        # self.resizable(0, 0) # Allow resizing
        self.title("Kitboy")
        set_appearance_mode("light")

        # Configure grid layout for the main window
        self.grid_columnconfigure(0, weight=0)  # Sidebar (fixed width)
        self.grid_columnconfigure(1, weight=1)  # Main content (expandable)
        self.grid_rowconfigure(0, weight=1)     # Single row for sidebar and main content

    def create_main_view(self):
        self.main_view = CTkFrame(master=self, fg_color="#030712", width=680, height=650, corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.grid(row=0, column=1, sticky="nsew")

        # Configure grid layout for the main_view
        self.main_view.grid_rowconfigure(0, weight=0)    # For search_container
        self.main_view.grid_rowconfigure(1, weight=1)    # For content_frame (expandable)
        self.main_view.grid_columnconfigure(0, weight=1) # Single column

        self.create_search_container() # Call the method to create and place the search container

        # create the content_frame
        self.content_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=27, pady=21)
        self.show_page("dashboard")

    def create_search_container(self):
        # The master for search_container should be self.main_view
        search_container = CTkFrame(master=self.main_view, height=50, fg_color="#040C15")
        # Place the search_container using grid within main_view
        # It should be in row 0, column 0 of main_view's grid
        search_container.grid(row=0, column=0, sticky="ew", pady=(45, 0), padx=27)

        CTkEntry(master=search_container, width=305, placeholder_text="Search Maintenance", border_color="#601E88", border_width=2).pack(side="left", padx=(13, 0), pady=15)
        CTkComboBox(master=search_container, width=125, values=["Date", "Most Recent", "Least Recent"], button_color="#601E88", border_color="#601E88", border_width=2, button_hover_color="#9569AF",dropdown_hover_color="#9569AF" , dropdown_fg_color="#030712", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)
        CTkComboBox(master=search_container, width=125, values=["Status", "Processing", "Confirmed", "Packing", "Shipping", "Delivered", "Cancelled"], button_color="#601E88", border_color="#601E88", border_width=2, button_hover_color="#9569AF",dropdown_hover_color="#9569AF" , dropdown_fg_color="#030712", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)

    # sidebar
    def create_sidebar(self):
        self.sidebar_frame = CTkFrame(master=self, fg_color="#040C15", width=176, height=650, corner_radius=0)
        self.sidebar_frame.pack_propagate(0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.add_sidebar_logo()
        self.add_sidebar_buttons()

    def add_sidebar_logo(self):
        logo_img_data = Image.open("assets/images/logo.png")
        logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))
        CTkLabel(master=self.sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

    def add_sidebar_buttons(self):
        buttons = [
            ("assets/icons/analytics_icon.png", "Dashboard", "dashboard", "transparent", None, 60),
            ("assets/icons/maintenance_icon.png", "Maintenances", "maintenances", "transparent", None, 16),
            ("assets/icons/person_icon.png", "Customers", "customers", "transparent", None, 16),
            ("assets/icons/vehicle_icon.png", "Vehicles", "vehicles", "transparent", None, 16),
            ("assets/icons/bell_icon.png", "Reminders", "reminders", "transparent", None, 16),
            ("assets/icons/mechanic_icon.png", "Mechanics", "mechanics", "transparent", None, 16),
            ("assets/icons/payment_icon.png", "Payments", "payments", "transparent", None, 16),
            ("assets/icons/turn-off_icon.png", "Logout", "logout", "transparent", None, 16),
            # ("assets/icons/settings_icon.png", "Settings", "settings", "transparent", None, 16)
        ]
        for icon, text, page, fg, text_color, pady in buttons:
            img_data = Image.open(icon)
            img = CTkImage(dark_image=img_data, light_image=img_data)
            CTkButton(
                master=self.sidebar_frame,
                image=img,
                text=text,
                fg_color=fg,
                font=("Arial Bold", 14),
                hover_color="#9569AF",
                anchor="w",
                text_color=text_color if text_color else "#fff",
                command=lambda p=page: self.show_page(p)
            ).pack(anchor="center", ipady=5, pady=(pady, 0))

    # show page
    def show_page(self, page_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        if page_name == "dashboard":
            Dashboard(self.content_frame).pack(expand=True, fill="both")
        elif page_name == "maintenances":
            Maintenances(self.content_frame).pack(expand=True, fill="both")
        elif page_name == "customers":
            Customers(self.content_frame).pack(expand=True, fill="both")
        elif page_name == "vehicles":
            Vehicles(self.content_frame).pack(expand=True, fill="both")
        elif page_name == "mechanics":
            Mechanics(self.content_frame).pack(expand=True, fill="both")
        elif page_name == "reminders":
            Reminders(self.content_frame).pack(expand=True, fill="both")
        elif page_name == "payments":
            Payments(self.content_frame).pack(expand=True, fill="both")
        # ... other pages ...

    def load_icon(self, filename, size=None):
        img_data = Image.open(filename)
        if size:
            return CTkImage(light_image=img_data, dark_image=img_data, size=size)
        return CTkImage(light_image=img_data, dark_image=img_data)

if __name__ == "__main__":
    app = KitboyApp()
    pywinstyles.apply_style(app, "optimised")  # Apply a style to the app
    app.iconbitmap("assets/icons/kitboy.ico")  # Set the application icon
    # Available styles: ['dark', 'mica', 'aero', 'transparent', 'acrylic', 'win7', 'inverse', 'popup', 'native', 'optimised', 'light', 'normal']
    app.mainloop()