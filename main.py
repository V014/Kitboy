import os
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
from dashboard import Dashboard

class KitboyApp(CTk):
    def __init__(self): # constructor
        super().__init__() # inherit from custom tkinter
        self.setup_environment() # call method that identifies files in root folder
        self.setup_window() # call method that sets the ui theme and resolution
        self.create_main_view() # call method that shows area with forms
        self.create_sidebar() # call method that loads the sidebar

    def setup_environment(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    def setup_window(self):
        self.geometry("856x645")
        self.resizable(0, 0)
        set_appearance_mode("light")

    def create_main_view(self):
        self.main_view = CTkFrame(master=self, fg_color="#fff", width=680, height=650, corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.pack(side="left")

        self.create_title_frame()
        self.create_metrics_frame()
        self.create_search_container()
        self.create_table()

        # Add this line to create the content_frame
        self.content_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        self.content_frame.pack(expand=True, fill="both", padx=27, pady=21)
        self.show_page("dashboard")

    def create_sidebar(self):
        self.sidebar_frame = CTkFrame(master=self, fg_color="#601E88", width=176, height=650, corner_radius=0)
        self.sidebar_frame.pack_propagate(0)
        self.sidebar_frame.pack(fill="y", anchor="w", side="left")

        self.add_sidebar_logo()
        self.add_sidebar_buttons()

    def add_sidebar_logo(self):
        logo_img_data = Image.open("logo.png")
        logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))
        CTkLabel(master=self.sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

    def add_sidebar_buttons(self):
        buttons = [
            ("analytics_icon.png", "Dashboard", "dashboard", "transparent", None, 60),
            ("package_icon.png", "Orders", "#fff", "#eee", "#601E88", 16),
            ("list_icon.png", "Orders", "transparent", "transparent", None, 16),
            ("returns_icon.png", "Returns", "transparent", "transparent", None, 16),
            ("settings_icon.png", "Settings", "transparent", "transparent", None, 16),
            ("person_icon.png", "Account", "transparent", "transparent", None, 160),
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
                hover_color="#601E88",
                anchor="w",
                text_color=text_color if text_color else "#fff",
                command=lambda p=page: self.show_page(p)
            ).pack(anchor="center", ipady=5, pady=(pady, 0))

    def create_title_frame(self):
        title_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Orders", font=("Arial Black", 25), text_color="#601E88").pack(anchor="nw", side="left")
        CTkButton(master=title_frame, text="+ New Order", font=("Arial Black", 15), text_color="#fff", fg_color="#601E88", hover_color="#207244").pack(anchor="ne", side="right")

    def show_page(self, page_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        if page_name == "dashboard":
            Dashboard(self.content_frame).pack(expand=True, fill="both")
        # elif page_name == "orders":
        #    OrdersPage(self.content_frame).pack(expand=True, fill="both")
        # ... other pages ...

    def create_metrics_frame(self):
        metrics_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        metrics_frame.pack(anchor="n", fill="x", padx=27, pady=(36, 0))

        # Orders metric
        orders_metric = CTkFrame(master=metrics_frame, fg_color="#601E88", width=200, height=60)
        orders_metric.grid_propagate(0)
        orders_metric.pack(side="left")
        logistics_img = self.load_icon("logistics_icon.png", (43, 43))
        CTkLabel(master=orders_metric, image=logistics_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
        CTkLabel(master=orders_metric, text="Orders", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        CTkLabel(master=orders_metric, text="123", text_color="#fff", font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))

        # Shipping metric
        shipped_metric = CTkFrame(master=metrics_frame, fg_color="#601E88", width=200, height=60)
        shipped_metric.grid_propagate(0)
        shipped_metric.pack(side="left", expand=True, anchor="center")
        shipping_img = self.load_icon("shipping_icon.png", (43, 43))
        CTkLabel(master=shipped_metric, image=shipping_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
        CTkLabel(master=shipped_metric, text="Shipping", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        CTkLabel(master=shipped_metric, text="91", text_color="#fff", font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))

        # Delivered metric
        delivered_metric = CTkFrame(master=metrics_frame, fg_color="#601E88", width=200, height=60)
        delivered_metric.grid_propagate(0)
        delivered_metric.pack(side="right")
        delivered_img = self.load_icon("delivered_icon.png", (43, 43))
        CTkLabel(master=delivered_metric, image=delivered_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
        CTkLabel(master=delivered_metric, text="Delivered", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        CTkLabel(master=delivered_metric, text="23", text_color="#fff", font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))

    def load_icon(self, filename, size=None):
        img_data = Image.open(filename)
        if size:
            return CTkImage(light_image=img_data, dark_image=img_data, size=size)
        return CTkImage(light_image=img_data, dark_image=img_data)

    def create_search_container(self):
        search_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
        search_container.pack(fill="x", pady=(45, 0), padx=27)
        CTkEntry(master=search_container, width=305, placeholder_text="Search Order", border_color="#601E88", border_width=2).pack(side="left", padx=(13, 0), pady=15)
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

if __name__ == "__main__":
    app = KitboyApp()
    app.mainloop()