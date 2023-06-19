from api import *

class VehicleEvent(Event):
    def __init__(self, vehicle_type):
        super().__init__()
        self.vehicle_type = vehicle_type

    def get_data(self):
        return self.vehicle_type