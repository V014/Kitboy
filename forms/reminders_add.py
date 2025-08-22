from customtkinter import *
from tkinter import messagebox

class AddRemindersForm(CTkFrame):
    def __init__(self, master, customer_options, vehicle_options, reminder_type_options, back_command=None, reminder_id=None, reminder_data=None):
        super().__init__(master, fg_color="transparent")
        self.back_command = back_command
        self.reminder_id = reminder_id