from models.calibrator import Calibrator

class CalibratorController:
    def __init__(self, resource, logger):
        self.calibrator = Calibrator(resource)
        self.logger = logger

    def connect(self):
        try:
            self.calibrator.connect()
            self.logger.log(f"Connected to calibrator: {self.calibrator.resource}")
        except Exception as e:
            self.logger.log(f"Error connecting calibrator: {e}")

    def apply_value(self, value, unit):
        try:
            self.calibrator.apply_value(value, unit)
            self.logger.log(f"Value applied: {value} {unit}")
        except Exception as e:
            self.logger.log(f"Error applying value: {e}")

    def set_operate(self):
        self.calibrator.operate()
        self.logger.log("Calibrator set to OPERATE mode")

    def set_standby(self):
        self.calibrator.standby()
        self.logger.log("Calibrator set to STANDBY mode")

    def reset(self):
        self.calibrator.reset()
        self.logger.log("Calibrator reset")
