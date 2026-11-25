from tkinter import messagebox

from customtkinter import (
    CTkButton,
    CTkComboBox,
    CTkEntry,
    CTkFrame,
    CTkLabel,
    CTkScrollableFrame,
)

import auth
import connection


class UserManagement(CTkScrollableFrame):
    def __init__(self, master, current_user):
        super().__init__(master, fg_color="transparent")
        self.current_user = current_user
        self.users = []

        CTkLabel(
            self, text="User access", font=("Arial", 25), text_color="#fff"
        ).pack(anchor="w", padx=27, pady=(29, 12))

        CTkLabel(
            self,
            text="Create workshop accounts and assign each person the access needed for their role.",
            text_color="#b8c2d1",
            wraplength=650,
            justify="left",
        ).pack(anchor="w", padx=27, pady=(0, 12))

        create_frame = CTkFrame(self, fg_color="#040C15")
        create_frame.pack(fill="x", padx=27, pady=8)
        CTkLabel(
            create_frame, text="Create account", font=("Arial", 17), text_color="#fff"
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(12, 8))
        self.username_entry = CTkEntry(
            create_frame, width=220, placeholder_text="Username"
        )
        self.username_entry.grid(row=1, column=0, padx=14, pady=8, sticky="w")
        self.password_entry = CTkEntry(
            create_frame, width=220, placeholder_text="Password (8+ characters)", show="*"
        )
        self.password_entry.grid(row=1, column=1, padx=8, pady=8, sticky="w")
        self.new_role = CTkComboBox(create_frame, values=list(auth.ROLES), width=180)
        self.new_role.set("Mechanic")
        self.new_role.grid(row=2, column=0, padx=14, pady=(0, 12), sticky="w")
        CTkButton(
            create_frame,
            text="Create user",
            fg_color="#601E88",
            hover_color="#9569AF",
            command=self.create_account,
        ).grid(row=2, column=1, padx=8, pady=(0, 12), sticky="w")

        role_frame = CTkFrame(self, fg_color="#040C15")
        role_frame.pack(fill="x", padx=27, pady=8)
        CTkLabel(
            role_frame, text="Change role", font=("Arial", 17), text_color="#fff"
        ).pack(anchor="w", padx=14, pady=(12, 8))
        self.user_choice = CTkComboBox(role_frame, values=[], width=220)
        self.user_choice.pack(side="left", padx=(14, 8), pady=(0, 12))
        self.role_choice = CTkComboBox(role_frame, values=list(auth.ROLES), width=180)
        self.role_choice.pack(side="left", padx=8, pady=(0, 12))
        CTkButton(
            role_frame,
            text="Update role",
            fg_color="#601E88",
            hover_color="#9569AF",
            command=self.change_role,
        ).pack(side="left", padx=8, pady=(0, 12))

        self.account_list = CTkFrame(self, fg_color="#040C15")
        self.account_list.pack(fill="x", padx=27, pady=(8, 24))
        self.refresh_users()

    def create_account(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if not username:
            messagebox.showerror("Invalid account", "Enter a username.", parent=self)
            return
        try:
            auth.create_user(username, password, self.new_role.get())
        except Exception as error:
            messagebox.showerror("Could not create account", str(error), parent=self)
            return

        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        messagebox.showinfo("Account created", "The workshop account is ready.", parent=self)
        self.refresh_users()

    def change_role(self):
        username = self.user_choice.get().strip()
        if not username:
            messagebox.showerror("Select a user", "Choose an account first.", parent=self)
            return
        if username == self.current_user["username"] and self.role_choice.get() != "Admin":
            messagebox.showerror(
                "Role change unavailable",
                "You cannot remove your own administrator access while signed in.",
                parent=self,
            )
            return
        try:
            auth.update_user_role(username, self.role_choice.get())
        except Exception as error:
            messagebox.showerror("Could not update role", str(error), parent=self)
            return

        self.refresh_users()

    def refresh_users(self):
        try:
            db = connection.open_connection()
            cursor = db.cursor()
            try:
                auth.ensure_role_column(cursor)
                db.commit()
                cursor.execute("SELECT username, role FROM users ORDER BY username")
                self.users = cursor.fetchall()
            finally:
                cursor.close()
                db.close()
        except Exception as error:
            messagebox.showerror("Could not load accounts", str(error), parent=self)
            return

        usernames = [row[0] for row in self.users]
        self.user_choice.configure(values=usernames)
        self.user_choice.set(usernames[0] if usernames else "")
        for child in self.account_list.winfo_children():
            child.destroy()

        CTkLabel(
            self.account_list, text="Accounts", font=("Arial", 17), text_color="#fff"
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(12, 8))
        for column, heading in enumerate(("Username", "Role")):
            CTkLabel(
                self.account_list,
                text=heading,
                font=("Arial Bold", 13),
                text_color="#c7a6df",
            ).grid(row=1, column=column, sticky="w", padx=14, pady=6)
        for row_index, (username, role) in enumerate(self.users, start=2):
            CTkLabel(self.account_list, text=username, text_color="#fff").grid(
                row=row_index, column=0, sticky="w", padx=14, pady=5
            )
            CTkLabel(self.account_list, text=role, text_color="#fff").grid(
                row=row_index, column=1, sticky="w", padx=14, pady=5
            )
