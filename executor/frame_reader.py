from api import Source
import socket
from event import FrameEvent
import cv2
import numpy


BUFFER_SIZE = 8


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
            if self.connect == None:
                self.connect, address = self.server_socket.accept()
            else:
                len_message = b''
                frame_byte = b''
                len_message = self.connect.recv(8)
                if len_message != b'':
                    len_frame = int.from_bytes(len_message)
                    len_message = b''
                    frame_byte = self.connect.recv(len_frame)
                    if frame_byte != b'':
                        nparr = numpy.frombuffer(frame_byte, numpy.uint8)
                        frame_byte = b''
                        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        cv2.imshow('', frame)
                        if cv2.waitKey(10) & 0xFF == ord('q'):
                            return
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