import os
import connection
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
from dashboard import Dashboard
from maintenances import Maintenances
from customers import Customers
from vehicles import Vehicles

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
        self.main_view.grid_rowconfigure(0, weight=0)    # For metrics_frame
        self.main_view.grid_rowconfigure(1, weight=1)    # For content_frame (expandable)
        self.main_view.grid_columnconfigure(0, weight=1) # Single column

        self.create_metrics_frame()
        # self.create_search_container()

        # Add this line to create the content_frame
        self.content_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=27, pady=21)
        self.show_page("dashboard")

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
        # ... other pages ...

    # metrics frame
    def create_metrics_frame(self):
        metrics_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        metrics_frame.grid(row=0, column=0, sticky="ew", padx=27, pady=(36, 0))

        # Metrics will be packed left-to-right and wrap automatically.
        # No explicit grid column configuration needed inside metrics_frame for this.
        # The individual metric frames will maintain their size due to grid_propagate(0).
        # padx=5 and pady=5 will provide spacing around each metric.

        # Customers metric
        customers_metric = CTkFrame(master=metrics_frame, fg_color="#040C15", width=200, height=60)
        customers_metric.grid_propagate(0)
        customers_metric.pack(side="left", anchor="nw", padx=5, pady=5)
        person_img = self.load_icon("assets/icons/person_icon.png", (43, 43))
        CTkLabel(master=customers_metric, image=person_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
        CTkLabel(master=customers_metric, text="Customers", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        self.customers_count_label = CTkLabel(master=customers_metric, text=str(get_customers_count()), text_color="#fff", font=("Arial Black", 15), justify="left")
        self.customers_count_label.grid(row=1, column=1, sticky="nw", pady=(0,10))
        customers_metric.grid_columnconfigure(1, weight=1) # Allow text label to use available space

        # Maintenances metric
        maintenances_metric = CTkFrame(master=metrics_frame, fg_color="#040C15", width=200, height=60)
        maintenances_metric.grid_propagate(0)
        maintenances_metric.pack(side="left", anchor="nw", padx=5, pady=5)
        maintenance_img = self.load_icon("assets/icons/maintenance_icon.png", (43, 43))
        CTkLabel(master=maintenances_metric, image=maintenance_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
        CTkLabel(master=maintenances_metric, text="Maintenances", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        self.maintenances_count_label = CTkLabel(master=maintenances_metric, text=str(get_maintenances_count()), text_color="#fff", font=("Arial Black", 15), justify="left")
        self.maintenances_count_label.grid(row=1, column=1, sticky="nw", pady=(0,10))
        maintenances_metric.grid_columnconfigure(1, weight=1)

        # Reminders metric
        reminders_metric = CTkFrame(master=metrics_frame, fg_color="#040C15", width=200, height=60)
        reminders_metric.grid_propagate(0)
        reminders_metric.pack(side="left", anchor="nw", padx=5, pady=5)
        reminder_img = self.load_icon("assets/icons/reminder_icon.png", (43, 43))
        CTkLabel(master=reminders_metric, image=reminder_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
        CTkLabel(master=reminders_metric, text="Reminders", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        self.reminders_count_label = CTkLabel(master=reminders_metric, text=str(get_reminders_count()), text_color="#fff", font=("Arial Black", 15), justify="left")
        self.reminders_count_label.grid(row=1, column=1, sticky="nw", pady=(0,10))
        reminders_metric.grid_columnconfigure(1, weight=1)

        # Payments metric
        payments_metric = CTkFrame(master=metrics_frame, fg_color="#040C15", width=200, height=60)
        payments_metric.grid_propagate(0)
        payments_metric.pack(side="left", anchor="nw", padx=5, pady=5)
        payment_img = self.load_icon("assets/icons/payment_icon.png", (43, 43)) # Assumed icon name
        CTkLabel(master=payments_metric, image=payment_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
        CTkLabel(master=payments_metric, text="Payments", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        self.payments_count_label = CTkLabel(master=payments_metric, text=str(get_payments_count()), text_color="#fff", font=("Arial Black", 15), justify="left")
        self.payments_count_label.grid(row=1, column=1, sticky="nw", pady=(0,10))
        payments_metric.grid_columnconfigure(1, weight=1)

        # Vehicles metric
        vehicles_metric = CTkFrame(master=metrics_frame, fg_color="#040C15", width=200, height=60)
        vehicles_metric.grid_propagate(0)
        vehicles_metric.pack(side="left", anchor="nw", padx=5, pady=5)
        vehicle_img = self.load_icon("assets/icons/vehicle_icon.png", (43, 43)) # Assumed icon name
        CTkLabel(master=vehicles_metric, image=vehicle_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
        CTkLabel(master=vehicles_metric, text="Vehicles", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        self.vehicles_count_label = CTkLabel(master=vehicles_metric, text=str(get_vehicles_count()), text_color="#fff", font=("Arial Black", 15), justify="left")
        self.vehicles_count_label.grid(row=1, column=1, sticky="nw", pady=(0,10))
        vehicles_metric.grid_columnconfigure(1, weight=1)

        # Start periodic update
        self.update_metrics()

    def update_metrics(self):
        self.customers_count_label.configure(text=str(get_customers_count()))
        self.maintenances_count_label.configure(text=str(get_maintenances_count()))
        self.reminders_count_label.configure(text=str(get_reminders_count()))
        self.payments_count_label.configure(text=str(get_payments_count()))
        self.vehicles_count_label.configure(text=str(get_vehicles_count()))
        self.after(5000, self.update_metrics)

    def load_icon(self, filename, size=None):
        img_data = Image.open(filename)
        if size:
            return CTkImage(light_image=img_data, dark_image=img_data, size=size)
        return CTkImage(light_image=img_data, dark_image=img_data)

    def create_search_container(self):
        search_container = CTkFrame(master=self.main_view, height=50, fg_color="#040C15")
        search_container.pack(fill="x", pady=(45, 0), padx=27)
        CTkEntry(master=search_container, width=305, placeholder_text="Search Job", border_color="#601E88", border_width=2).pack(side="left", padx=(13, 0), pady=15)
        CTkComboBox(master=search_container, width=125, values=["Date", "Most Recent Order", "Least Recent Order"], button_color="#601E88", border_color="#601E88", border_width=2, button_hover_color="#9569AF",dropdown_hover_color="#9569AF" , dropdown_fg_color="#030712", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)
        CTkComboBox(master=search_container, width=125, values=["Status", "Processing", "Confirmed", "Packing", "Shipping", "Delivered", "Cancelled"], button_color="#601E88", border_color="#601E88", border_width=2, button_hover_color="#9569AF",dropdown_hover_color="#9569AF" , dropdown_fg_color="#030712", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)

# pull data for metrics
def get_customers_count():
    db = connection
    dbcon = db.dbcon
    class Dummy: pass
    db_obj = Dummy()
    dbcon(db_obj)
    count = 0
    if db_obj.con:
        try:
            db_obj.cur.execute("SELECT COUNT(*) FROM customers")
            count = db_obj.cur.fetchone()[0]
        except Exception:
            pass
        finally:
            db_obj.con.close()
    return count

def get_maintenances_count():
    db = connection
    dbcon = db.dbcon
    class Dummy: pass
    db_obj = Dummy()
    dbcon(db_obj)
    count = 0
    if db_obj.con:
        try:
            db_obj.cur.execute("SELECT COUNT(*) FROM maintenances")
            count = db_obj.cur.fetchone()[0]
        except Exception:
            pass
        finally:
            db_obj.con.close()
    return count

def get_reminders_count():
    db = connection
    dbcon = db.dbcon
    class Dummy: pass
    db_obj = Dummy()
    dbcon(db_obj)
    count = 0
    if db_obj.con:
        try:
            db_obj.cur.execute("SELECT COUNT(*) FROM reminders")
            count = db_obj.cur.fetchone()[0]
        except Exception:
            pass
        finally:
            db_obj.con.close()
    return count

def get_payments_count():
    db = connection
    dbcon = db.dbcon
    class Dummy: pass
    db_obj = Dummy()
    dbcon(db_obj)
    count = 0
    if db_obj.con:
        try:
            db_obj.cur.execute("SELECT COUNT(*) FROM customer_payments") # Assuming table name
            count = db_obj.cur.fetchone()[0]
        except Exception as e:
            print(f"Error getting payments count: {e}")
            pass
        finally:
            db_obj.con.close()
    return count

def get_vehicles_count():
    db = connection
    dbcon = db.dbcon
    class Dummy: pass
    db_obj = Dummy()
    dbcon(db_obj)
    count = 0
    if db_obj.con:
        try:
            db_obj.cur.execute("SELECT COUNT(*) FROM vehicles") # Assuming table name
            count = db_obj.cur.fetchone()[0]
        except Exception as e:
            print(f"Error getting vehicles count: {e}")
            pass
        finally:
            db_obj.con.close()
    return count

if __name__ == "__main__":
    app = KitboyApp()
    app.mainloop()