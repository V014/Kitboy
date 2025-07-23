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

class Dashboard(CTkScrollableFrame):
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

        # metrics frame
    def create_metrics_frame(self):
        metrics_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        metrics_frame.grid(row=0, column=0, sticky="ew", padx=27, pady=(36, 0))

        # Customers metric
        customers_metric = CTkFrame(master=metrics_frame, fg_color="#040C15", width=200, height=60)
        customers_metric.grid_propagate(0)
        customers_metric.pack(side="left", anchor="nw", padx=5, pady=5)
        person_img = self.load_icon("assets/icons/person_icon.png", (43, 43))
        CTkLabel(master=customers_metric, image=person_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
        CTkLabel(master=customers_metric, text="Customers", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        self.customers_count_label = CTkLabel(master=customers_metric, text=str(get_customers_count()), text_color="#fff", font=("Arial Black", 15), justify="left")
        self.customers_count_label.grid(row=1, column=1, sticky="nw", pady=(0,10))
        customers_metric.grid_columnconfigure(1, weight=1) # Allow text label to use available space

        # Maintenances metric
        maintenances_metric = CTkFrame(master=metrics_frame, fg_color="#040C15", width=200, height=60)
        maintenances_metric.grid_propagate(0)
        maintenances_metric.pack(side="left", anchor="nw", padx=5, pady=5)
        maintenance_img = self.load_icon("assets/icons/maintenance_icon.png", (43, 43))
        CTkLabel(master=maintenances_metric, image=maintenance_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
        CTkLabel(master=maintenances_metric, text="Maintenances", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        self.maintenances_count_label = CTkLabel(master=maintenances_metric, text=str(get_maintenances_count()), text_color="#fff", font=("Arial Black", 15), justify="left")
        self.maintenances_count_label.grid(row=1, column=1, sticky="nw", pady=(0,10))
        maintenances_metric.grid_columnconfigure(1, weight=1)

        # Reminders metric
        reminders_metric = CTkFrame(master=metrics_frame, fg_color="#040C15", width=200, height=60)
        reminders_metric.grid_propagate(0)
        reminders_metric.pack(side="left", anchor="nw", padx=5, pady=5)
        reminder_img = self.load_icon("assets/icons/reminder_icon.png", (43, 43))
        CTkLabel(master=reminders_metric, image=reminder_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
        CTkLabel(master=reminders_metric, text="Reminders", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        self.reminders_count_label = CTkLabel(master=reminders_metric, text=str(get_reminders_count()), text_color="#fff", font=("Arial Black", 15), justify="left")
        self.reminders_count_label.grid(row=1, column=1, sticky="nw", pady=(0,10))
        reminders_metric.grid_columnconfigure(1, weight=1)

        # Payments metric
        payments_metric = CTkFrame(master=metrics_frame, fg_color="#040C15", width=200, height=60)
        payments_metric.grid_propagate(0)
        payments_metric.pack(side="left", anchor="nw", padx=5, pady=5)
        payment_img = self.load_icon("assets/icons/payment_icon.png", (43, 43))
        CTkLabel(master=payments_metric, image=payment_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
        CTkLabel(master=payments_metric, text="Payments", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        self.payments_count_label = CTkLabel(master=payments_metric, text=str(get_payments_count()), text_color="#fff", font=("Arial Black", 15), justify="left")
        self.payments_count_label.grid(row=1, column=1, sticky="nw", pady=(0,10))
        payments_metric.grid_columnconfigure(1, weight=1)

        # Vehicles metric
        vehicles_metric = CTkFrame(master=metrics_frame, fg_color="#040C15", width=200, height=60)
        vehicles_metric.grid_propagate(0)
        vehicles_metric.pack(side="left", anchor="nw", padx=5, pady=5)
        vehicle_img = self.load_icon("assets/icons/vehicle_icon.png", (43, 43))
        CTkLabel(master=vehicles_metric, image=vehicle_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)
        CTkLabel(master=vehicles_metric, text="Vehicles", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        self.vehicles_count_label = CTkLabel(master=vehicles_metric, text=str(get_vehicles_count()), text_color="#fff", font=("Arial Black", 15), justify="left")
        self.vehicles_count_label.grid(row=1, column=1, sticky="nw", pady=(0,10))
        vehicles_metric.grid_columnconfigure(1, weight=1)

        # Start periodic update
        self.update_metrics()

    def update_metrics(self):
        self.customers_count_label.configure(text=str(get_customers_count()))
        self.maintenances_count_label.configure(text=str(get_maintenances_count()))
        self.reminders_count_label.configure(text=str(get_reminders_count()))
        self.payments_count_label.configure(text=str(get_payments_count()))
        self.vehicles_count_label.configure(text=str(get_vehicles_count()))
        self.after(5000, self.update_metrics)

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
            spine.set_color("#030712")

        chart_frame = CTkFrame(master=self, fg_color="#030712")
        chart_frame.pack(fill="x", padx=27, pady=(10, 0))
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # pull data for metrics
def get_customers_count():
    db = connection
    dbcon = db.dbcon
    class Dummy: pass
    db_obj = Dummy()
    dbcon(db_obj)
    count = 0
    if db_obj.con:
        try:
            db_obj.cur.execute("SELECT COUNT(*) FROM customers")
            count = db_obj.cur.fetchone()[0]
        except Exception:
            pass
        finally:
            db_obj.con.close()
    return count

def get_maintenances_count():
    db = connection
    dbcon = db.dbcon
    class Dummy: pass
    db_obj = Dummy()
    dbcon(db_obj)
    count = 0
    if db_obj.con:
        try:
            db_obj.cur.execute("SELECT COUNT(*) FROM maintenances")
            count = db_obj.cur.fetchone()[0]
        except Exception:
            pass
        finally:
            db_obj.con.close()
    return count

def get_reminders_count():
    db = connection
    dbcon = db.dbcon
    class Dummy: pass
    db_obj = Dummy()
    dbcon(db_obj)
    count = 0
    if db_obj.con:
        try:
            db_obj.cur.execute("SELECT COUNT(*) FROM reminders")
            count = db_obj.cur.fetchone()[0]
        except Exception:
            pass
        finally:
            db_obj.con.close()
    return count

def get_payments_count():
    db = connection
    dbcon = db.dbcon
    class Dummy: pass
    db_obj = Dummy()
    dbcon(db_obj)
    count = 0
    if db_obj.con:
        try:
            db_obj.cur.execute("SELECT COUNT(*) FROM customer_payments") # Assuming table name
            count = db_obj.cur.fetchone()[0]
        except Exception as e:
            print(f"Error getting payments count: {e}")
            pass
        finally:
            db_obj.con.close()
    return count

def get_vehicles_count():
    db = connection
    dbcon = db.dbcon
    class Dummy: pass
    db_obj = Dummy()
    dbcon(db_obj)
    count = 0
    if db_obj.con:
        try:
            db_obj.cur.execute("SELECT COUNT(*) FROM vehicles") # Assuming table name
            count = db_obj.cur.fetchone()[0]
        except Exception as e:
            print(f"Error getting vehicles count: {e}")
            pass
        finally:
            db_obj.con.close()
    return count