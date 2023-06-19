from api import *
from typing import List
from vehicle_event import VehicleEvent

class VehicleCounter(Operator):
    def __init__(self, name, parallelism, grouping=None) -> None:
        super().__init__(name, parallelism, grouping)
        self.instance = 0
        self.count_map = {}

    def setup_instance(self, instance):
        self.instance = instance
    
    def apply(self, event, event_collector):
        # print("Counter")
        vehicle_event = event
        vehicle = vehicle_event.get_data()
        count = self.count_map.get(vehicle, 0) + 1
        self.count_map[vehicle] = count
        print(f"VehicleCounter :: instance {self.instance} -->")
        print(self.count_map)