from customtkinter import *
from tkinter import messagebox

class AddMechanicForm(CTkFrame):
    def __init__(self, master, back_command=None):
        super().__init__(master, fg_color="transparent")
        self.back_command = back_command

        CTkLabel(self, text="Add Mechanic", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pady=(29,0), padx=27)

        # Scrollable frame for form fields
        scroll_frame = CTkScrollableFrame(self, fg_color="transparent", width=1, height=420)
        scroll_frame.pack(fill="both", expand=True, padx=27, pady=(10,0))

        # First Name
        CTkLabel(scroll_frame, text="First Name", font=("Arial Bold", 17), text_color="#fff").grid(row=0, column=0, sticky="w", pady=(0, 2))
        self.firstname_entry = CTkEntry(scroll_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.firstname_entry.grid(row=1, column=0, ipady=10, pady=(0, 10))

        # Last Name
        CTkLabel(scroll_frame, text="Last Name", font=("Arial Bold", 17), text_color="#fff").grid(row=0, column=1, sticky="w", padx=(25,0), pady=(0, 2))
        self.lastname_entry = CTkEntry(scroll_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.lastname_entry.grid(row=1, column=1, ipady=10, padx=(24,0), pady=(0, 10))

        # Identification
        CTkLabel(scroll_frame, text="Identification", font=("Arial Bold", 17), text_color="#fff").grid(row=2, column=0, sticky="w", pady=(0, 2))
        self.identification_entry = CTkEntry(scroll_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.identification_entry.grid(row=3, column=0, ipady=10, pady=(0, 10))

        # Certification
        CTkLabel(scroll_frame, text="Certification", font=("Arial Bold", 17), text_color="#fff").grid(row=2, column=1, sticky="w", padx=(25,0), pady=(0, 2))
        self.certification_entry = CTkEntry(scroll_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.certification_entry.grid(row=3, column=1, ipady=10, padx=(24,0), pady=(0, 10))

        # Certified On
        CTkLabel(scroll_frame, text="Certified On (YYYY-MM-DD)", font=("Arial Bold", 17), text_color="#fff").grid(row=4, column=0, sticky="w", pady=(0, 2))
        self.certified_on_entry = CTkEntry(scroll_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.certified_on_entry.grid(row=5, column=0, ipady=10, pady=(0, 10))

        # Institute
        CTkLabel(scroll_frame, text="Institute", font=("Arial Bold", 17), text_color="#fff").grid(row=4, column=1, sticky="w", padx=(25,0), pady=(0, 2))
        self.institute_entry = CTkEntry(scroll_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.institute_entry.grid(row=5, column=1, ipady=10, padx=(24,0), pady=(0, 10))

        # Skills
        CTkLabel(scroll_frame, text="Skills", font=("Arial Bold", 17), text_color="#fff").grid(row=6, column=0, sticky="w", pady=(0, 2))
        self.skills_entry = CTkEntry(scroll_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.skills_entry.grid(row=7, column=0, ipady=10, pady=(0, 10))

        # Specification
        CTkLabel(scroll_frame, text="Specification", font=("Arial Bold", 17), text_color="#fff").grid(row=6, column=1, sticky="w", padx=(25,0), pady=(0, 2))
        self.specification_entry = CTkEntry(scroll_frame, fg_color="#F0F0F0", border_width=0, width=300)
        self.specification_entry.grid(row=7, column=1, ipady=10, padx=(24,0), pady=(0, 10))

        # Actions (always visible at the bottom)
        actions = CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", pady=(10, 20))

        CTkButton(actions, text="Back", width=138, height=40, fg_color="transparent", font=("Arial Bold", 17), border_color="#601E88", hover_color="#601E88", border_width=2, text_color="#fff", command=self.back_command).pack(side="left", anchor="sw", padx=(27,24))
        CTkButton(actions, text="Add", width=138, height=40, font=("Arial Bold", 17), hover_color="#9569AF", fg_color="#601E88", text_color="#fff", command=self.add_mechanic).pack(side = "left", anchor="se", padx=(0,27))

    def add_mechanic(self):
        import connection
        firstname = self.firstname_entry.get().strip()
        lastname = self.lastname_entry.get().strip()
        identification = self.identification_entry.get().strip()
        certification = self.certification_entry.get().strip()
        certified_on = self.certified_on_entry.get().strip()
        institute = self.institute_entry.get().strip()
        skills = self.skills_entry.get().strip()
        specification = self.specification_entry.get().strip()

        if not firstname or not lastname or not identification:
            messagebox.showerror("Error", "First name, last name, and identification are required.")
            return

        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        if db_obj.con:
            try:
                db_obj.cur.execute(
                    "INSERT INTO mechanics (firstname, lastname, identification, certification, certified_on, institute, skills, specification) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (firstname, lastname, identification, certification, certified_on, institute, skills, specification)
                )
                db_obj.con.commit()
                messagebox.showinfo("Success", "Mechanic added successfully!")
                if self.back_command:
                    self.back_command()
            except Exception as e:
                messagebox.showerror("Database Error", f"Could not add mechanic: {e}")
            finally:
                db_obj.con.close()