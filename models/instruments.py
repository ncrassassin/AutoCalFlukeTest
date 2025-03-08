import pyvisa

class InstrumentController:
    def __init__(self, resource_name):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(resource_name)

    def write(self, command):
        self.inst.write(command)

    def query(self, command):
        return self.inst.query(command)

    def close(self):
        self.inst.close()

class Fluke5522A(InstrumentController):
    def output_voltage(self, voltage, ac=False, freq=50):
        if ac:
            self.write(f'OUT {voltage}V,{freq}HZ')
        else:
            self.write(f'OUT {voltage}V')
        self.write('OPER')

    def output_off(self):
        self.write('STBY')

class DMM(InstrumentController):
    def measure_voltage(self, ac=False):
        mode = 'VOLT:AC?' if ac else 'VOLT:DC?'
        reading = self.query(mode)
        return float(reading.strip())