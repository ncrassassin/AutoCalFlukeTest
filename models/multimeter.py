import pyvisa

class Multimeter:
    SCPI_COMMANDS = {
        "Voltage": "MEAS:VOLT:DC?",
        "Current": "MEAS:CURR:DC?",
        "Resistance": "MEAS:RES?",
        "Frequency": "MEAS:FREQ?"
    }

    def __init__(self, resource):
        self.resource = resource
        self.instrument = None

    def connect(self):
        self.instrument = pyvisa.ResourceManager().open_resource(self.resource)
        self.instrument.timeout = 5000

    def measure(self, quantity):
        command = self.SCPI_COMMANDS.get(quantity, "")
        if command:
            return self.instrument.query(command).strip()
        else:
            raise ValueError("Invalid quantity specified")
