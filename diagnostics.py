import threading
from tkinter import TclError, messagebox

from customtkinter import (
    CTkButton,
    CTkComboBox,
    CTkFrame,
    CTkLabel,
    CTkTextbox,
)

import obd2


class Diagnostics(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self._busy = False

        heading = CTkFrame(self, fg_color="transparent")
        heading.pack(fill="x", padx=27, pady=(29, 12))
        CTkLabel(
            heading, text="OBD-II Diagnostics", font=("Arial", 25), text_color="#fff"
        ).pack(side="left")
        CTkButton(
            heading,
            text="Refresh ports",
            fg_color="#601E88",
            hover_color="#9569AF",
            command=self.refresh_ports,
        ).pack(side="right")

        CTkLabel(
            self,
            text="Pair your Bluetooth adapter in Windows first. Select its outgoing COM port below.",
            text_color="#b8c2d1",
            wraplength=620,
            justify="left",
        ).pack(anchor="w", padx=27, pady=(0, 10))

        controls = CTkFrame(self, fg_color="#040C15")
        controls.pack(fill="x", padx=27, pady=8)
        self.port_box = CTkComboBox(controls, width=180, values=["No ports found"])
        self.port_box.pack(side="left", padx=12, pady=12)
        self.scan_button = CTkButton(
            controls,
            text="Connect & scan",
            fg_color="#601E88",
            hover_color="#9569AF",
            command=self.scan,
        )
        self.scan_button.pack(side="left", padx=8, pady=12)

        self.status_label = CTkLabel(
            self, text="Ready to connect", text_color="#b8c2d1"
        )
        self.status_label.pack(anchor="w", padx=27, pady=(12, 4))

        self.results = CTkTextbox(
            self,
            fg_color="#040C15",
            text_color="#fff",
            wrap="word",
            font=("Consolas", 13),
        )
        self.results.pack(fill="both", expand=True, padx=27, pady=(4, 20))
        self.results.insert(
            "1.0",
            "Vehicle data and stored diagnostic trouble codes will appear here.\n"
            "This screen reads codes and live data; it does not clear codes or change vehicle settings.",
        )
        self.refresh_ports()

    def refresh_ports(self):
        try:
            ports = obd2.available_ports()
        except ImportError:
            messagebox.showerror(
                "OBD-II support unavailable",
                "Install the project dependencies to enable Bluetooth diagnostics.",
                parent=self,
            )
            return
        except Exception as error:
            messagebox.showerror("Could not list COM ports", str(error), parent=self)
            return

        self.port_box.configure(values=ports or ["No ports found"])
        self.port_box.set(ports[0] if ports else "No ports found")

    def scan(self):
        port = self.port_box.get().strip()
        if not port or port == "No ports found":
            messagebox.showwarning(
                "Select an adapter", "Select a paired adapter COM port first.", parent=self
            )
            return
        if self._busy:
            return

        self._busy = True
        self.scan_button.configure(state="disabled", text="Scanning...")
        self.status_label.configure(
            text="Connecting to adapter; this can take several seconds..."
        )
        self.results.delete("1.0", "end")

        def run_scan():
            try:
                data = obd2.read_vehicle_data(port)
                callback = lambda: self._show_result(data, None)
            except Exception as error:
                callback = lambda error=error: self._show_result(None, error)
            try:
                self.after(0, callback)
            except (TclError, RuntimeError):
                pass

        threading.Thread(target=run_scan, daemon=True).start()

    def _show_result(self, result, error):
        self._busy = False
        self.scan_button.configure(state="normal", text="Connect & scan")
        if error:
            self.status_label.configure(text="Scan failed")
            self.results.insert("1.0", str(error))
            return

        readings, trouble_codes = result
        self.status_label.configure(text="Scan complete")
        lines = ["LIVE DATA"]
        lines.extend(
            "{}: {}".format(label, value) for label, value in readings
        )
        if not readings:
            lines.append("No supported live data was returned by this vehicle.")

        lines.extend(("", "DIAGNOSTIC TROUBLE CODES"))
        if trouble_codes:
            lines.extend(
                "{} - {}".format(code, description)
                for code, description in trouble_codes
            )
        else:
            lines.append("No stored trouble codes reported.")
        self.results.insert("1.0", "\n".join(lines))
