from api import *
from typing import List
import socket as sck
import sys
from vehicle_event import VehicleEvent

BUFFER_SIZE = 16

class SensorReader(Source):
    def __init__(self, name, parallelism, port):
        super().__init__(name, parallelism)
        self.port_base = port
        self.instance = 0
        self.socket = None
        self.server_socket = None

    def setup_instance(self, instance):
        self.instance = instance
        self.setup_socket(self.port_base + instance)
    
    def get_events(self, event_collector):
        try:
            if self.socket == None:
                self.socket, address = self.server_socket.accept()
            vehicle = self.socket.recv(BUFFER_SIZE)
            if vehicle != b'':
                vehicle = vehicle.decode()
                event_collector.append(VehicleEvent(vehicle))
                print(f"SensorReader :: instance {self.instance} --> {vehicle}")
        except Exception as e:
            print(e)
            raise e
        
    def setup_socket(self, port):
        try:
            self.server_socket = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
            self.server_socket.setsockopt(sck.SOL_SOCKET, sck.SO_REUSEADDR, 1)
            host_name = sck.gethostname()
            host_ip = sck.gethostbyname(host_name)
            self.server_socket.bind((host_ip, port))
            self.server_socket.listen(10)
        except Exception as e:
            print(f"Failed to create socket: {str(e)}")
            raise e
