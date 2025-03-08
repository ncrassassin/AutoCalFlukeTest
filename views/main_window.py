from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from controllers.test_controller import TestController
from models.instruments import Fluke5522A, DMM
from models.database import Database

class TestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.calibrator = Fluke5522A('GPIB0::1::INSTR')
        self.dmm = DMM('GPIB0::2::INSTR')
        self.db = Database()
        self.test_controller = TestController(self.calibrator, self.dmm, self.db)

    def initUI(self):
        self.setWindowTitle('Automated Voltage Test')
        self.layout = QVBoxLayout()

        self.label = QLabel('Click to start Voltage Tests')
        self.layout.addWidget(self.label)

        self.btn_dc = QPushButton('Start DC Voltage Tests')
        self.btn_dc.clicked.connect(self.run_dc_tests)
        self.layout.addWidget(self.btn_dc)

        self.btn_ac = QPushButton('Start AC Voltage Tests')
        self.btn_ac.clicked.connect(self.run_ac_tests)
        self.layout.addWidget(self.btn_ac)

        self.setLayout(self.layout)

    def run_dc_tests(self):
        voltages = [1, 5, 10]
        results = []
        for voltage in voltages:
            results.append(self.test_controller.perform_voltage_test(voltage, ac=False))
        self.show_results(results)

    def run_ac_tests(self):
        test_points = [(1, 50), (5, 1000)]
        results = []
        for voltage, freq in test_points:
            results.append(self.test_controller.perform_voltage_test(voltage, ac=True, freq=freq))
        self.show_results(results)

    def show_results(self, results):
        message = '\n'.join([f'{tp}: Measured={mv:.3f}V, Result={res}' for tp, mv, res in results])
        QMessageBox.information(self, 'Test Results', message)

    def closeEvent(self, event):
        self.calibrator.close()
        self.dmm.close()
        self.db.close()
        event.accept()