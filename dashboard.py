from customtkinter import *
from CTkTable import CTkTable

class Dashboard(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        # CTkLabel(self, text="Dashboard", font=("Arial Black", 25)).pack(pady=20)
        # Add more dashboard widgets here
        # Title
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Dashboard", font=("Arial Black", 25), text_color="#601E88").pack(anchor="nw", side="left")
        CTkButton(master=title_frame, text="+ New Order", font=("Arial Black", 15), text_color="#fff", fg_color="#601E88", hover_color="#207244").pack(anchor="ne", side="right")