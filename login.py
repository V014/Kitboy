import os
from customtkinter import *
from tkinter import messagebox
from main import KitboyApp
import pywinstyles
import auth
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Login(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x480")
        self.resizable(0, 0)
        self.title("KitboyLogin")
        self.application = None

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

        frame = CTkFrame(master=self, width=300, height=480, fg_color="#030712")
        frame.pack_propagate(0)
        frame.pack(expand=True, side="right")

        CTkLabel(master=frame, text="Welcome Back!", text_color="#ffffff", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
        CTkLabel(master=frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  Username:", text_color="#ffffff", anchor="w", justify="left", font=("Arial Bold", 14), image=self.email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
        self.username_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.username_entry.pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  Password:", text_color="#ffffff", anchor="w", justify="left", font=("Arial Bold", 14), image=self.password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
        self.password_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
        self.password_entry.pack(anchor="w", padx=(25, 0))

        CTkButton(master=frame, text="Login", fg_color="#601E88", hover_color="#9569AF", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=self.login_action).pack(anchor="w", pady=(40, 0), padx=(25, 0))
        CTkButton(master=frame, text="Coming soon...", fg_color="#202020", hover_color="#202020", font=("Arial Bold", 9), text_color="#EEEEEE", width=225, image=self.google_icon).pack(anchor="w", pady=(20, 0), padx=(25, 0))

    def login_action(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Sign in failed", "Enter your username and password.")
            return

        try:
            session = auth.authenticate(username, password)
            if not session:
                messagebox.showerror("Login Failed", "Invalid email or password.")
                return
            if session["bootstrap_admin"]:
                messagebox.showinfo(
                    "Administrator setup",
                    "No administrator existed, so this first signed-in account "
                    "has been assigned the Admin role.",
                )
            self.withdraw()
            try:
                self.application = KitboyApp(self, session, self.return_to_login)
                pywinstyles.apply_style(self.application, "optimised")
                self.application.iconbitmap("assets/icons/kitboy.ico")
            except Exception:
                if self.application is not None:
                    self.application.destroy()
                    self.application = None
                self.deiconify()
                raise
        except Exception as error:
            messagebox.showerror("Sign in error", str(error))

    def return_to_login(self):
        self.application = None
        self.deiconify()

if __name__ == "__main__":
    app = Login()
    app.mainloop()