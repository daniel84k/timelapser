import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

# --- Parametry ---
LOCATIONS = ["teresin", "tivoli"]
MODES = ["timelapse", "startrails", "simulation"]

class TimelapserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Timelapser GUI")
        self.root.geometry("320x480")
        self.root.resizable(False, False)

        self.build_ui()

    def build_ui(self):
        self.mode_var = tk.StringVar(value="timelapse")
        self.location_var = tk.StringVar(value="teresin")
        self.rule_var = tk.StringVar(value="500")
        self.focal_var = tk.StringVar(value="35")
        self.gradient_var = tk.BooleanVar()
        self.duration_var = tk.StringVar(value="1")
        self.interval_var = tk.StringVar(value="1")
        self.exposure_var = tk.StringVar(value="15")
        self.gap_var = tk.StringVar(value="5")
        self.iso_var = tk.StringVar(value="800")
        self.altitude_var = tk.StringVar(value="-5")

        row = 0
        ttk.Label(self.root, text="Mode:").grid(row=row, column=0, sticky="w")
        ttk.OptionMenu(self.root, self.mode_var, self.mode_var.get(), *MODES).grid(row=row, column=1)

        row += 1
        ttk.Label(self.root, text="Location:").grid(row=row, column=0, sticky="w")
        ttk.OptionMenu(self.root, self.location_var, self.location_var.get(), *LOCATIONS).grid(row=row, column=1)

        row += 1
        ttk.Label(self.root, text="Rule:").grid(row=row, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.rule_var).grid(row=row, column=1)

        row += 1
        ttk.Label(self.root, text="Focal Length:").grid(row=row, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.focal_var).grid(row=row, column=1)

        row += 1
        ttk.Checkbutton(self.root, text="Gradient", variable=self.gradient_var).grid(row=row, columnspan=2)

        row += 1
        ttk.Label(self.root, text="Duration (h):").grid(row=row, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.duration_var).grid(row=row, column=1)

        row += 1
        ttk.Label(self.root, text="Interval (s):").grid(row=row, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.interval_var).grid(row=row, column=1)

        row += 1
        ttk.Label(self.root, text="Exposure (s):").grid(row=row, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.exposure_var).grid(row=row, column=1)

        row += 1
        ttk.Label(self.root, text="Gap (s):").grid(row=row, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.gap_var).grid(row=row, column=1)

        row += 1
        ttk.Label(self.root, text="ISO:").grid(row=row, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.iso_var).grid(row=row, column=1)

        row += 1
        ttk.Label(self.root, text="Altitude (for simulation):").grid(row=row, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.altitude_var).grid(row=row, column=1)

        row += 1
        ttk.Button(self.root, text="Start", command=self.run_script).grid(row=row, columnspan=2, pady=10)

    def run_script(self):
        args = ["python3", "exposure_test.py"]

        mode = self.mode_var.get()
        args += ["--mode", mode] if mode != "simulation" else ["--simulation"]

        args += ["--location", self.location_var.get()]
        args += ["--rule", self.rule_var.get()]
        args += ["--focal", self.focal_var.get()]

        if self.gradient_var.get():
            args += ["--gradient"]

        if mode == "simulation":
            args += ["--altitude", self.altitude_var.get()]
        else:
            args += ["--duration", self.duration_var.get()]
            if mode == "timelapse":
                args += ["--interval", self.interval_var.get()]
            elif mode == "startrails":
                args += ["--exposure", self.exposure_var.get(), "--gap", self.gap_var.get(), "--iso", self.iso_var.get()]

        try:
            subprocess.Popen(args)
            messagebox.showinfo("Started", f"Script started with mode: {mode}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TimelapserGUI(root)
    root.mainloop()
