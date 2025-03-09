# views/main_view.py

import tkinter as tk
from tkinter import ttk, filedialog
from controllers.calibrator_controller import CalibratorController
from controllers.multimeter_controller import MultimeterController
from utils.logger import Logger
from utils.test_sequence import create_template, run_sequence
import pyvisa

class MainView:
    def __init__(self, master):
        self.master = master
        master.title("Calibration and Multimeter Control Software")

        # Resource Manager
        try:
            self.rm = pyvisa.ResourceManager()
            self.available_devices = self.rm.list_resources()
        except Exception as e:
            self.available_devices = []
            print(f"PyVISA error: {e}")

        # Logger Widget
        self.log_box = tk.Text(self.master, height=10, width=70)
        self.log_box.grid(row=10, column=0, columnspan=3, padx=5, pady=5)
        self.logger = Logger(self.log_box)

        # Controllers (initialized when devices connect)
        self.calibrator_controller = None
        self.multimeter_controller = None

        # GUI Variables
        self.selected_calibrator = tk.StringVar(value=self.available_devices[0] if self.available_devices else "")
        self.selected_multimeter = tk.StringVar(value=self.available_devices[0] if self.available_devices else "")
        self.quantity = tk.StringVar(value="Voltage")
        self.unit = tk.StringVar(value="V")
        self.value = tk.DoubleVar(value=0.0)
        self.measure_quantity = tk.StringVar(value="Voltage")
        self.test_sequence_file = None

        self.create_widgets()

    def create_widgets(self):
        # Original widgets kept exactly as before
        ttk.Label(self.master, text="Select Calibrator:").grid(row=0, column=0, padx=5, pady=5)
        ttk.OptionMenu(self.master, self.selected_calibrator, self.selected_calibrator.get(), *self.available_devices).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.master, text="Connect Calibrator", command=self.connect_calibrator).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self.master, text="Select Multimeter:").grid(row=1, column=0, padx=5, pady=5)
        ttk.OptionMenu(self.master, self.selected_multimeter, self.selected_multimeter.get(), *self.available_devices).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.master, text="Connect Multimeter", command=self.connect_multimeter).grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(self.master, text="Quantity:").grid(row=2, column=0, padx=5, pady=5)
        ttk.OptionMenu(self.master, self.quantity, "Voltage", "Voltage", "Resistance", "Capacitance", "Current", "Frequency").grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.master, text="Value:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(self.master, textvariable=self.value).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.master, text="Unit:").grid(row=4, column=0, padx=5, pady=5)
        ttk.OptionMenu(self.master, self.unit, "V", "V", "mV", "uV", "A", "mA", "uA", "Ohm", "kOhm", "Hz", "kHz").grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(self.master, text="Apply", command=self.apply_value).grid(row=5, column=0, padx=5, pady=5)
        ttk.Button(self.master, text="Reset", command=self.reset_controls).grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(self.master, text="Operate", command=self.operate_calibrator).grid(row=6, column=0, padx=5, pady=5)
        ttk.Button(self.master, text="Standby", command=self.standby_calibrator).grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self.master, text="Measure Quantity:").grid(row=7, column=0, padx=5, pady=5)
        ttk.OptionMenu(self.master, self.measure_quantity, "Voltage", "Voltage", "Current", "Resistance", "Frequency").grid(row=7, column=1, padx=5, pady=5)
        ttk.Button(self.master, text="Measure", command=self.measure).grid(row=7, column=2, padx=5, pady=5)

        ttk.Button(self.master, text="Create Test Sequence", command=self.create_test_sequence).grid(row=8, column=0, padx=5, pady=5)
        ttk.Button(self.master, text="Run Test Sequence", command=self.run_test_sequence).grid(row=8, column=1, padx=5, pady=5)

    # GUI action handlers calling controllers
    def connect_calibrator(self):
        device = self.selected_calibrator.get()
        self.calibrator_controller = CalibratorController(device, self.logger)
        self.calibrator_controller.connect()

    def connect_multimeter(self):
        device = self.selected_multimeter.get()
        self.multimeter_controller = MultimeterController(device, self.logger)
        self.multimeter_controller.connect()

    def apply_value(self):
        if self.calibrator_controller:
            self.calibrator_controller.apply_value(self.value.get(), self.unit.get())
        else:
            self.logger.log("No calibrator connected.")

    def operate_calibrator(self):
        if self.calibrator_controller:
            self.calibrator_controller.set_operate()
        else:
            self.logger.log("No calibrator connected.")

    def standby_calibrator(self):
        if self.calibrator_controller:
            self.calibrator_controller.set_standby()
        else:
            self.logger.log("No calibrator connected.")

    def measure(self):
        if self.multimeter_controller:
            self.multimeter_controller.measure(self.measure_quantity.get())
        else:
            self.logger.log("No multimeter connected.")

    def reset_controls(self):
        self.value.set(0.0)
        self.quantity.set("Voltage")
        self.unit.set("V")
        if self.calibrator_controller:
            self.calibrator_controller.reset()

    def create_test_sequence(self):
        file = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if file:
            create_template(file)
            self.test_sequence_file = file
            self.logger.log(f"Sequence template created: {file}")

    def run_test_sequence(self):
        if self.test_sequence_file and self.calibrator_controller:
            run_sequence(self.test_sequence_file, self.calibrator_controller, self.logger)
        else:
            self.logger.log("Select a sequence file and connect calibrator first.")
