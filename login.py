import os
import sys
import importlib
import connection
from customtkinter import *
from tkinter import messagebox
from main import KitboyApp
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Login(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x480")
        self.resizable(0, 0)
        self.title("Login")

        # Load images using organized asset paths
        self.side_img = CTkImage(
            dark_image=Image.open(os.path.join("assets", "images", "side-img.png")),
            light_image=Image.open(os.path.join("assets", "images", "side-img.png")),
            size=(300, 480)
        )
        self.email_icon = CTkImage(
            dark_image=Image.open(os.path.join("assets", "icons", "email-icon.png")),
            light_image=Image.open(os.path.join("assets", "icons", "email-icon.png")),
            size=(20, 20)
        )
        self.password_icon = CTkImage(
            dark_image=Image.open(os.path.join("assets", "icons", "password-icon.png")),
            light_image=Image.open(os.path.join("assets", "icons", "password-icon.png")),
            size=(17, 17)
        )
        self.google_icon = CTkImage(
            dark_image=Image.open(os.path.join("assets", "icons", "google-icon.png")),
            light_image=Image.open(os.path.join("assets", "icons", "google-icon.png")),
            size=(17, 17)
        )

        CTkLabel(master=self, text="", image=self.side_img).pack(expand=True, side="left")

        frame = CTkFrame(master=self, width=300, height=480, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(expand=True, side="right")

        CTkLabel(master=frame, text="Welcome Back!", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
        CTkLabel(master=frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  Username:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=self.email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
        self.username_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.username_entry.pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=self.password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
        self.password_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
        self.password_entry.pack(anchor="w", padx=(25, 0))

        CTkButton(master=frame, text="Login", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=self.login_action).pack(anchor="w", pady=(40, 0), padx=(25, 0))
        CTkButton(master=frame, text="Continue With Google", fg_color="#EEEEEE", hover_color="#EEEEEE", font=("Arial Bold", 9), text_color="#601E88", width=225, image=self.google_icon).pack(anchor="w", pady=(20, 0), padx=(25, 0))

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        db = connection
        dbcon = db.dbcon
        class Dummy: pass
        db_obj = Dummy()
        dbcon(db_obj)
        if db_obj.con is None:
            messagebox.showerror("Error", "Database connection failed.")
            return
        try:
            db_obj.cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            result = db_obj.cur.fetchone()
            if result:
                self.destroy()
                app = KitboyApp()
                app.mainloop()
            else:
                messagebox.showerror("Login Failed", "Invalid email or password.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if db_obj.con:
                db_obj.con.close()

if __name__ == "__main__":
    app = Login()
    app.mainloop()