import os
from customtkinter import *
from PIL import Image
from tkinter import messagebox

class KitboyApp(CTkToplevel):
    def __init__(self, master, current_user, on_logout=None):
        super().__init__(master)
        self.current_user = current_user
        self.on_logout = on_logout
        self.setup_environment()
        self.setup_window()
        self.create_sidebar()
        self.create_main_view()
        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def close_app(self):
        self.destroy()
        if self.on_logout:
            self.on_logout()

    def setup_environment(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    def setup_window(self):
        self.geometry("1080x760")
        self.minsize(860, 620)
        # self.resizable(0, 0) # Allow resizing
        self.title("Kitboy")
        set_appearance_mode("light")

        # Configure grid layout for the main window
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def create_main_view(self):
        self.main_view = CTkFrame(master=self, fg_color="#030712", width=680, height=650, corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.grid(row=0, column=1, sticky="nsew")

        self.main_view.grid_rowconfigure(0, weight=0)
        self.main_view.grid_rowconfigure(1, weight=1)
        self.main_view.grid_columnconfigure(0, weight=1)

        self.create_search_container()

        self.content_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=27, pady=21)
        self.show_page("dashboard")

    def create_search_container(self):
        search_container = CTkFrame(
            master=self.main_view, height=50, fg_color="#040C15"
        )
        search_container.grid(row=0, column=0, sticky="ew", pady=(45, 0), padx=27)
        CTkLabel(
            search_container,
            text="KITBOY  /  VEHICLE SERVICE WORKSHOP",
            font=("Arial Bold", 14),
            text_color="#fff",
        ).pack(side="left", padx=16, pady=14)
        CTkLabel(
            search_container,
            text="Customer care  ·  Maintenance  ·  Diagnostics",
            font=("Arial", 12),
            text_color="#b8c2d1",
        ).pack(side="right", padx=16, pady=14)

    def create_sidebar(self):
        self.sidebar_frame = CTkFrame(master=self, fg_color="#040C15", width=176, height=650, corner_radius=0)
        self.sidebar_frame.pack_propagate(0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.add_sidebar_logo()
        self.sidebar_buttons_frame = CTkScrollableFrame(
            self.sidebar_frame, width=176, fg_color="transparent", corner_radius=0
        )
        self.sidebar_buttons_frame.pack(fill="both", expand=True)
        self.add_sidebar_buttons()
        CTkLabel(
            self.sidebar_frame,
            text="{} · {}".format(self.current_user["username"], self.current_user["role"]),
            text_color="#b8c2d1",
            font=("Arial", 11),
            wraplength=155,
        ).pack(side="bottom", pady=(0, 12))

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
            ("assets/icons/vehicle_icon.png", "Diagnostics", "diagnostics", "transparent", None, 16),
            ("assets/icons/mechanic_icon.png", "User access", "users", "transparent", None, 16),
            ("assets/icons/turn-off_icon.png", "Logout", "logout", "transparent", None, 16),
        ]
        for icon, text, page, fg, text_color, pady in buttons:
            if page not in self.allowed_pages() and page != "logout":
                continue
            img_data = Image.open(icon)
            img = CTkImage(dark_image=img_data, light_image=img_data)
            CTkButton(
                master=self.sidebar_buttons_frame,
                image=img,
                text=text,
                fg_color=fg,
                font=("Arial Bold", 14),
                hover_color="#9569AF",
                anchor="w",
                text_color=text_color if text_color else "#fff",
                command=lambda p=page: self.show_page(p)
            ).pack(anchor="center", ipady=5, pady=(pady, 0))

    def allowed_pages(self):
        from auth import ROLE_PAGES

        return ROLE_PAGES.get(self.current_user["role"], set())

    def show_page(self, page_name):
        if page_name == "logout":
            self.close_app()
            return
        if page_name not in self.allowed_pages():
            messagebox.showerror(
                "Access denied", "Your workshop role cannot open this section.", parent=self
            )
            return

        for widget in self.content_frame.winfo_children():
            widget.destroy()
        if page_name == "dashboard":
            from dashboard import Dashboard

            Dashboard(self.content_frame).pack(expand=True, fill="both")
        elif page_name == "maintenances":
            from maintenances import Maintenances

            Maintenances(self.content_frame).pack(expand=True, fill="both")
        elif page_name == "customers":
            from customers import Customers

            Customers(self.content_frame).pack(expand=True, fill="both")
        elif page_name == "vehicles":
            from vehicles import Vehicles

            Vehicles(self.content_frame).pack(expand=True, fill="both")
        elif page_name == "mechanics":
            from mechanics import Mechanics

            Mechanics(self.content_frame).pack(expand=True, fill="both")
        elif page_name == "reminders":
            from reminders import Reminders

            Reminders(self.content_frame).pack(expand=True, fill="both")
        elif page_name == "payments":
            from payments import Payments

            Payments(self.content_frame).pack(expand=True, fill="both")
        elif page_name == "diagnostics":
            from diagnostics import Diagnostics

            Diagnostics(self.content_frame).pack(expand=True, fill="both")
        elif page_name == "users":
            from user_management import UserManagement

            UserManagement(self.content_frame, self.current_user).pack(
                expand=True, fill="both"
            )

    def load_icon(self, filename, size=None):
        img_data = Image.open(filename)
        if size:
            return CTkImage(light_image=img_data, dark_image=img_data, size=size)
        return CTkImage(light_image=img_data, dark_image=img_data)

if __name__ == "__main__":
    from login import Login

    login = Login()
    login.mainloop()