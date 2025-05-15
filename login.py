import os # change the current working directory to the directory where the script is located.
import importlib
import connection.db
from customtkinter import *
from tkinter import messagebox
from PIL import Image

# get the absolute path of the script's directory.
# Set the working directory to the script's directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def login_action():
    username = username_entry.get()
    password = password_entry.get()
    # Connect to DB
    db = connection.db
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
            app.destroy()
            dashboard = importlib.import_module("dashboard.main")
            dashboard.main()  # Assumes dashboard.py has a main() function to start the dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        if db_obj.con:
            db_obj.con.close()

app = CTk()
app.geometry("600x480")
app.resizable(0,0)

side_img_data = Image.open("side-img.png")
email_icon_data = Image.open("email-icon.png")
password_icon_data = Image.open("password-icon.png")
google_icon_data = Image.open("google-icon.png")

side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20,20))
password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17,17))
google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17,17))

CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

CTkLabel(master=frame, text="Welcome Back!", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
CTkLabel(master=frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

username_entry = CTkLabel(master=frame, text="  Username:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
username_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
username_entry.pack(anchor="w", padx=(25, 0))

password_entry = CTkLabel(master=frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
password_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
password_entry.pack(anchor="w", padx=(25, 0))

CTkButton(master=frame, text="Login", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=login_action).pack(anchor="w", pady=(40, 0), padx=(25, 0))
CTkButton(master=frame, text="Continue With Google", fg_color="#EEEEEE", hover_color="#EEEEEE", font=("Arial Bold", 9), text_color="#601E88", width=225, image=google_icon).pack(anchor="w", pady=(20, 0), padx=(25, 0))

app.mainloop()