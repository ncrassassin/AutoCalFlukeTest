import pyvisa

class Calibrator:
    def __init__(self, resource):
        self.resource = resource
        self.instrument = None

    def connect(self):
        self.instrument = pyvisa.ResourceManager().open_resource(self.resource)
        self.instrument.timeout = 5000
        self.reset()

    def apply_value(self, value, unit):
        command = f"OUT {value} {unit}"
        self.instrument.write(command)

    def operate(self):
        self.instrument.write("OPER")

    def standby(self):
        self.instrument.write("STBY")

    def reset(self):
        self.instrument.write("*RST")
        self.instrument.write("*CLS")