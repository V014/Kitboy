import threading
from tkinter import Canvas, TclError

from customtkinter import CTkFrame, CTkLabel

import connection


class Dashboard(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        heading = CTkFrame(self, fg_color="transparent")
        heading.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        CTkLabel(
            heading, text="Workshop overview", font=("Arial", 25), text_color="#fff"
        ).pack(anchor="w", side="left")

        metrics = CTkFrame(self, fg_color="transparent")
        metrics.pack(fill="x", padx=27, pady=(16, 0))
        self.metric_values = {}
        for column, title in enumerate(("Customers", "Vehicles", "Service jobs")):
            card = CTkFrame(metrics, fg_color="#040C15")
            card.grid(row=0, column=column, sticky="ew", padx=(0, 10))
            CTkLabel(
                card, text=title, font=("Arial", 13), text_color="#b8c2d1"
            ).pack(anchor="w", padx=14, pady=(12, 4))
            value = CTkLabel(
                card, text="Loading...", font=("Arial", 22), text_color="#fff"
            )
            value.pack(anchor="w", padx=14, pady=(0, 12))
            self.metric_values[title] = value
        for column in range(3):
            metrics.grid_columnconfigure(column, weight=1)

        self.chart_frame = CTkFrame(self, fg_color="#040C15")
        self.chart_frame.pack(fill="both", expand=True, padx=27, pady=20)
        CTkLabel(
            self.chart_frame,
            text="Payments over time",
            font=("Arial", 17),
            text_color="#fff",
        ).pack(anchor="w", padx=18, pady=(14, 0))
        self.status = CTkLabel(
            self.chart_frame, text="Loading payment history...", text_color="#b8c2d1"
        )
        self.status.pack(anchor="w", padx=18, pady=(8, 0))
        self.canvas = Canvas(
            self.chart_frame,
            height=300,
            background="#040C15",
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True, padx=18, pady=(0, 14))
        self.canvas.bind("<Configure>", self._draw_chart)
        self._chart_data = []
        threading.Thread(target=self._load_data, daemon=True).start()

    def _load_data(self):
        try:
            db = connection.open_connection()
            cursor = db.cursor()
            try:
                cursor.execute(
                    """
                    SELECT
                        (SELECT COUNT(*) FROM customers),
                        (SELECT COUNT(*) FROM vehicles),
                        (SELECT COUNT(*) FROM maintenances)
                    """
                )
                counts = cursor.fetchone()
                cursor.execute(
                    """
                    SELECT DATE_FORMAT(date, '%b %Y'), SUM(amount)
                    FROM customer_payments
                    GROUP BY DATE_FORMAT(date, '%Y-%m')
                    ORDER BY MIN(date) DESC
                    LIMIT 6
                    """
                )
                rows = cursor.fetchall()
            finally:
                cursor.close()
                db.close()
            self._chart_data = [
                (str(month), float(total or 0)) for month, total in reversed(rows)
            ]
            self._schedule(lambda: self._show_data(counts))
        except Exception as error:
            self._schedule(
                lambda error=error: self._show_error(error)
            )

    def _schedule(self, callback):
        try:
            self.after(0, callback)
        except (TclError, RuntimeError):
            pass

    def _show_data(self, counts):
        for title, count in zip(("Customers", "Vehicles", "Service jobs"), counts):
            self.metric_values[title].configure(text=str(count))
        self.status.configure(
            text="Last six months" if self._chart_data else "No payment history yet."
        )
        self._draw_chart()

    def _show_error(self, error):
        for value in self.metric_values.values():
            value.configure(text="Unavailable")
        self.status.configure(text="Workshop data unavailable: {}".format(error))

    def _draw_chart(self, _event=None):
        if not hasattr(self, "canvas"):
            return
        canvas = self.canvas
        canvas.delete("all")
        width = max(canvas.winfo_width(), 320)
        height = max(canvas.winfo_height(), 180)
        left, right, top, bottom = 56, width - 18, 18, height - 42
        if right <= left or bottom <= top:
            return

        values = [value for _, value in self._chart_data]
        maximum = max(values, default=0) or 1
        for line in range(4):
            y = bottom - (bottom - top) * line / 3
            value = maximum * line / 3
            canvas.create_line(left, y, right, y, fill="#293445")
            canvas.create_text(
                left - 8,
                y,
                text="{:,.0f}".format(value),
                fill="#b8c2d1",
                anchor="e",
                font=("Arial", 9),
            )

        if not self._chart_data:
            canvas.create_text(
                (left + right) / 2,
                (top + bottom) / 2,
                text="Payment totals will appear here",
                fill="#b8c2d1",
                font=("Arial", 12),
            )
            return

        count = len(self._chart_data)
        points = []
        for index, (month, value) in enumerate(self._chart_data):
            x = left + (right - left) * index / max(count - 1, 1)
            y = bottom - (bottom - top) * value / maximum
            points.extend((x, y))
            canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="#E44982", outline="")
            canvas.create_text(
                x, bottom + 18, text=month, fill="#b8c2d1", font=("Arial", 9)
            )
        if len(points) >= 4:
            canvas.create_line(*points, fill="#E44982", width=2, smooth=True)
