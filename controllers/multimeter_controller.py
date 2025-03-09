from models.multimeter import Multimeter

class MultimeterController:
    def __init__(self, resource, logger):
        self.multimeter = Multimeter(resource)
        self.logger = logger

    def connect(self):
        try:
            self.multimeter.connect()
            self.logger.log(f"Connected to multimeter: {self.multimeter.resource}")
        except Exception as e:
            self.logger.log(f"Error connecting multimeter: {e}")

    def measure(self, quantity):
        try:
            result = self.multimeter.measure(quantity)
            self.logger.log(f"Measured {quantity}: {result}")
            return result
        except Exception as e:
            self.logger.log(f"Measurement error: {e}")
            return None
