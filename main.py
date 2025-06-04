import os
import connection
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
from dashboard import Dashboard
from maintenances import Maintenances
from customers import Customers

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
        self.resizable(0, 0)
        self.title("Kitboy")
        set_appearance_mode("light")

    def create_main_view(self):
        self.main_view = CTkFrame(master=self, fg_color="#fff", width=680, height=650, corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.pack(side="left")

        # self.create_title_frame()
        self.create_metrics_frame()
        self.create_search_container()
        # self.create_table()

        # Add this line to create the content_frame
        self.content_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        self.content_frame.pack(expand=True, fill="both", padx=27, pady=21)
        self.show_page("dashboard")

    # sidebar
    def create_sidebar(self):
        self.sidebar_frame = CTkFrame(master=self, fg_color="#040C15", width=176, height=650, corner_radius=0)
        self.sidebar_frame.pack_propagate(0)
        self.sidebar_frame.pack(fill="y", anchor="w", side="left")

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
            ("assets/icons/settings_icon.png", "Settings", "settings", "transparent", None, 160),
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

    # title frame
    def create_title_frame(self):
        title_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Orders", font=("Arial Black", 25), text_color="#601E88").pack(anchor="nw", side="left")
        CTkButton(master=title_frame, text="+ New Job", font=("Arial Black", 15), text_color="#fff", fg_color="#601E88", hover_color="#9569AF").pack(anchor="ne", side="right")

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
        # ... other pages ...

    # metrics frame
    def create_metrics_frame(self):
        metrics_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        metrics_frame.pack(anchor="n", fill="x", padx=27, pady=(36, 0))

        # Customers metric
        customers_metric = CTkFrame(master=metrics_frame, fg_color="#601E88", width=200, height=60)
        customers_metric.grid_propagate(0)
        customers_metric.pack(side="left")
        person_img = self.load_icon("assets/icons/person_icon.png", (43, 43))
        CTkLabel(master=customers_metric, image=person_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
        CTkLabel(master=customers_metric, text="Customers", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        self.customers_count_label = CTkLabel(master=customers_metric, text=str(get_customers_count()), text_color="#fff", font=("Arial Black", 15), justify="left")
        self.customers_count_label.grid(row=1, column=1, sticky="nw", pady=(0,10))

        # Maintenances metric
        maintenances_metric = CTkFrame(master=metrics_frame, fg_color="#601E88", width=200, height=60)
        maintenances_metric.grid_propagate(0)
        maintenances_metric.pack(side="left", expand=True, anchor="center")
        maintenance_img = self.load_icon("assets/icons/maintenance_icon.png", (43, 43))
        CTkLabel(master=maintenances_metric, image=maintenance_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
        CTkLabel(master=maintenances_metric, text="Maintenances", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        self.maintenances_count_label = CTkLabel(master=maintenances_metric, text=str(get_maintenances_count()), text_color="#fff", font=("Arial Black", 15), justify="left")
        self.maintenances_count_label.grid(row=1, column=1, sticky="nw", pady=(0,10))

        # Reminders metric
        reminders_metric = CTkFrame(master=metrics_frame, fg_color="#601E88", width=200, height=60)
        reminders_metric.grid_propagate(0)
        reminders_metric.pack(side="right")
        reminder_img = self.load_icon("assets/icons/reminder_icon.png", (43, 43))
        CTkLabel(master=reminders_metric, image=reminder_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
        CTkLabel(master=reminders_metric, text="Reminders", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        self.reminders_count_label = CTkLabel(master=reminders_metric, text=str(get_reminders_count()), text_color="#fff", font=("Arial Black", 15), justify="left")
        self.reminders_count_label.grid(row=1, column=1, sticky="nw", pady=(0,10))

        # Start periodic update
        self.update_metrics()

    def update_metrics(self):
        self.customers_count_label.configure(text=str(get_customers_count()))
        self.maintenances_count_label.configure(text=str(get_maintenances_count()))
        self.reminders_count_label.configure(text=str(get_reminders_count()))
        self.after(5000, self.update_metrics)

    def load_icon(self, filename, size=None):
        img_data = Image.open(filename)
        if size:
            return CTkImage(light_image=img_data, dark_image=img_data, size=size)
        return CTkImage(light_image=img_data, dark_image=img_data)

    def create_search_container(self):
        search_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
        search_container.pack(fill="x", pady=(45, 0), padx=27)
        CTkEntry(master=search_container, width=305, placeholder_text="Search Job", border_color="#601E88", border_width=2).pack(side="left", padx=(13, 0), pady=15)
        CTkComboBox(master=search_container, width=125, values=["Date", "Most Recent Order", "Least Recent Order"], button_color="#601E88", border_color="#601E88", border_width=2, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color="#601E88", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)
        CTkComboBox(master=search_container, width=125, values=["Status", "Processing", "Confirmed", "Packing", "Shipping", "Delivered", "Cancelled"], button_color="#601E88", border_color="#601E88", border_width=2, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color="#601E88", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)

    def create_table(self):
        table_data = [
            ["Order ID", "Item Name", "Customer", "Address", "Status", "Quantity"],
            ['3833', 'Smartphone', 'Alice', '123 Main St', 'Confirmed', '8'],
            ['6432', 'Laptop', 'Bob', '456 Elm St', 'Packing', '5'],
            ['2180', 'Tablet', 'Crystal', '789 Oak St', 'Delivered', '1'],
            ['5438', 'Headphones', 'John', '101 Pine St', 'Confirmed', '9'],
            ['9144', 'Camera', 'David', '202 Cedar St', 'Processing', '2'],
            ['7689', 'Printer', 'Alice', '303 Maple St', 'Cancelled', '2'],
            ['1323', 'Smartwatch', 'Crystal', '404 Birch St', 'Shipping', '6'],
            ['7391', 'Keyboard', 'John', '505 Redwood St', 'Cancelled', '10'],
            ['4915', 'Monitor', 'Alice', '606 Fir St', 'Shipping', '6'],
            ['5548', 'External Hard Drive', 'David', '707 Oak St', 'Delivered', '10'],
            ['5485', 'Table Lamp', 'Crystal', '808 Pine St', 'Confirmed', '4'],
            ['7764', 'Desk Chair', 'Bob', '909 Cedar St', 'Processing', '9'],
            ['8252', 'Coffee Maker', 'John', '1010 Elm St', 'Confirmed', '6'],
            ['2377', 'Blender', 'David', '1111 Redwood St', 'Shipping', '2'],
            ['5287', 'Toaster', 'Alice', '1212 Maple St', 'Processing', '1'],
            ['7739', 'Microwave', 'Crystal', '1313 Cedar St', 'Confirmed', '8'],
            ['3129', 'Refrigerator', 'John', '1414 Oak St', 'Processing', '5'],
            ['4789', 'Vacuum Cleaner', 'Bob', '1515 Pine St', 'Cancelled', '10']
        ]
        table_frame = CTkScrollableFrame(master=self.main_view, fg_color="transparent")
        table_frame.pack(expand=True, fill="both", padx=27, pady=21)
        table = CTkTable(master=table_frame, values=table_data, colors=["#E6E6E6", "#EEEEEE"], header_color="#601E88", hover_color="#B4B4B4")
        table.edit_row(0, text_color="#fff", hover_color="#601E88")
        table.pack(expand=True)

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

if __name__ == "__main__":
    app = KitboyApp()
    app.mainloop()