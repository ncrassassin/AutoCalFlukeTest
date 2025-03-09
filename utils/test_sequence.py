import time

import pandas as pd
import os

def create_template(file_path):
    template = pd.DataFrame({
        "Quantity": ["Voltage", "Resistance"],
        "Value": [1.0, 1000.0],
        "Unit": ["V", "Ohm"],
        "Operate/Standby": ["Operate", "Standby"],
        "Delay (s)": [5, 5],
    })
    template.to_excel(file_path, index=False)
    os.startfile(file_path)

def run_sequence(file_path, calibrator_controller, logger):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        mode = row["Operate/Standby"]
        if mode == "Operate":
            calibrator_controller.set_operate()
        else:
            calibrator_controller.set_standby()
        calibrator_controller.apply_value(row["Value"], row["Unit"])
        logger.log(f"Waiting {row['Delay (s)']}s")
        time.sleep(row["Delay (s)"])
