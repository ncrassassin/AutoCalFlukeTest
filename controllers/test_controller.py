import time

class TestController:
    TOLERANCE = 0.05

    def __init__(self, calibrator, dmm, db):
        self.calibrator = calibrator
        self.dmm = dmm
        self.db = db

    def perform_voltage_test(self, voltage, ac=False, freq=50):
        test_point = f'{voltage}V AC' if ac else f'{voltage}V DC'
        self.calibrator.output_voltage(voltage, ac, freq)
        time.sleep(2)
        measured_voltage = self.dmm.measure_voltage(ac)
        result = 'PASS' if abs((measured_voltage - voltage)/voltage) <= self.TOLERANCE else 'FAIL'
        self.db.log_result(test_point, voltage, measured_voltage, result)
        self.calibrator.output_off()
        return test_point, measured_voltage, result