from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
import matplotlib
matplotlib.use("Agg")  # Use a non-interactive backend
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Dashboard(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        # CTkLabel(self, text="Dashboard", font=("Arial Black", 25)).pack(pady=20)
        # Add more dashboard widgets here
        # Title
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Dashboard", font=("Arial Black", 25), text_color="#ffffff").pack(anchor="nw", side="left")
        CTkButton(master=title_frame, text="+ New Job", font=("Arial", 15), text_color="#fff", fg_color="#601E88", hover_color="#9569AF").pack(anchor="ne", side="right")
        self.create_payments_chart()

    def create_payments_chart(self):
        # Example data: Replace with your database query results
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        payments = [1200, 1500, 1100, 1800, 1700, 1600]

        # Create a matplotlib figure with custom background
        fig = Figure(figsize=(4, 2), dpi=100, facecolor="#040C15")
        ax = fig.add_subplot(111, facecolor="#040C15")  # Set axes background

        ax.bar(months, payments, color="#601E88")
        ax.set_title("Payments Over Time", color="white")
        ax.set_ylabel("Amount ($)", color="white")
        ax.set_xlabel("Month", color="white")

        # Change tick and spine colors for better visibility
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_color("white")

        # Embed the figure in the Tkinter frame
        chart_frame = CTkFrame(master=self, fg_color="#040C15")
        chart_frame.pack(fill="x", padx=27, pady=(10, 0))

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)