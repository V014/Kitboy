from customtkinter import *
from CTkTable import CTkTable
import connection # Import the connection module
from PIL import Image
import matplotlib
matplotlib.use("Agg")  # Use a non-interactive backend
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.interpolate import make_interp_spline

class Dashboard(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        # CTkLabel(self, text="Dashboard", font=("Arial Black", 25)).pack(pady=20)
        # Add more dashboard widgets here
        # Title
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Dashboard", font=("Arial", 25), text_color="#ffffff").pack(anchor="nw", side="left")
        CTkButton(master=title_frame, text="New Job", font=("Arial", 15), text_color="#fff", fg_color="#601E88", hover_color="#9569AF").pack(anchor="ne", side="right")
        self.create_payments_chart()

    def get_monthly_payments_data(self):
        # Fetches and aggregates monthly payment data from the database.
        db = connection
        dbcon_func = db.dbcon
        class DummyDB: pass
        db_obj = DummyDB()
        dbcon_func(db_obj)

        months = []
        payments = []

        if db_obj.con:
            try:
                # Query to get sum of payments grouped by month.
                query = """
                    SELECT DATE_FORMAT(date, '%b') AS month, SUM(amount) AS total_payments
                    FROM customer_payments
                    GROUP BY DATE_FORMAT(date, '%Y-%m')
                    ORDER BY MIN(date)
                    LIMIT 6; 
                """ # Limiting to 6 months for display, adjust as needed
                db_obj.cur.execute(query)
                results = db_obj.cur.fetchall()
                for row in results:
                    months.append(row[0])
                    payments.append(float(row[1])) # Ensure amount is float
            except Exception as e:
                print(f"Error fetching payment data: {e}")
            finally:
                db_obj.con.close()
        return months, payments

    def create_payments_chart(self):
        months, payments = self.get_monthly_payments_data()
        if not months or not payments:
            months = ["N/A"]
            payments = [0]

        fig = Figure(figsize=(4, 2), dpi=100, facecolor="#030712")
        ax = fig.add_subplot(111, facecolor="#040C15")

        # Convert months to numbers for interpolation
        x = np.arange(len(months))
        y = np.array(payments)

        # Smooth the line if enough points
        if len(x) > 2:
            x_smooth = np.linspace(x.min(), x.max(), 300)
            spl = make_interp_spline(x, y, k=3)
            y_smooth = spl(x_smooth)
            ax.plot(x_smooth, y_smooth, color="#E44982", linewidth=2)
            ax.set_xticks(x)
            ax.set_xticklabels(months)
        else:
            ax.plot(x, y, color="#E44982", linewidth=2)

        # ax.bar(x, y, color="#601E88", alpha=0.5)

        ax.set_title("Payments Over Time", color="white")
        ax.set_ylabel("Amount (MWK)", color="white")
        ax.set_xlabel("Month", color="white")
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_color("purple")

        chart_frame = CTkFrame(master=self, fg_color="#030712")
        chart_frame.pack(fill="x", padx=27, pady=(10, 0))
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)