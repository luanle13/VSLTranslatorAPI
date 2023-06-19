from api import *
from engine import *
from sensor_reader import SensorReader
from vehicle_counter import VehicleCounter

if __name__ == "__main__":
    job = Job("vehicle_count")
    bridge_stream = job.add_source(SensorReader("sensor_reader", 1, 9990))
    bridge_stream.apply_operator(VehicleCounter("vehicle_counter", 1, FieldsGrouping()))
    starter = JobStarter(job)
    starter.start()