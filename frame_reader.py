from api import Source
import socket
from frame_event import FrameEvent
import cv2
import struct
import pickle
import numpy


BUFFER_SIZE = 4665600


class FrameReader(Source):
    def __init__(self, name, parallelism, port):
        super().__init__(name, parallelism)
        self.port_base = port
        self.instance = 0
        self.connect = None
        self.server_socket = None
    
    def setup_instance(self, instance):
        self.instance = instance
        self.setup_socket(self.port_base + instance)

    def get_events(self, event_collector):
        try:
            data = b''
            if self.connect == None:
                self.connect, address = self.server_socket.accept()
            else:
                data = self.connect.recv(BUFFER_SIZE)
                if data != b'':
                    nparr = numpy.frombuffer(data, numpy.uint8)
                    data = b''
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    event_collector.append(FrameEvent(frame))
        except Exception as e:
            pass
    
    def setup_socket(self, port):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            self.server_socket.bind((host_ip, port))
            self.server_socket.listen(5)
        except Exception as e:
            print(f"Failed to create socket: {str(e)}")
            raise e            