from api import Source
import socket
from event import FrameEvent
import cv2
import numpy as np
import socketio
import eventlet


# BUFFER_SIZE = 8

sio = socketio.Server(async_mode='eventlet')
app = socketio.WSGIApp(sio)
eventlet.wsgi.server(eventlet.listen(('', 9990)), app)


class FrameReader(Source):
    def __init__(self, name, parallelism, port):
        super().__init__(name, parallelism)
        self.port_base = port
        self.instance = 0
        self.sio = socketio.Server(async_mode='eventlet')
        self.app = socketio.WSGIApp(self.sio)
        eventlet.wsgi.server(eventlet.listen(('', self.port_base)), self.app)


    def setup_instance(self, instance):
        self.instance = instance


    def get_events(self, event_collector):
        pass


    @sio.event
    def connect(sid, environ):
        print(f'Client connected: {sid}')

    @sio.event
    def disconnect(sid):
        print(f'Client disconnected: {sid}')
    
    @sio.on('frame')
    def frame(self, sid, data):
        print(data)
        nparr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imshow('receive', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            return
        self.event_collector.append(FrameEvent(img))

        # try:
        #     # self.count += 1
        #     # print(f"Frame Reader: {self.count}")
        #     if self.connect == None:
        #         self.connect, address = self.server_socket.accept()
        #     else:
        #         len_message = b''
        #         frame_byte = b''
        #         len_message = self.connect.recv(8)
        #         if len_message != b'':
        #             len_frame = int.from_bytes(len_message)
        #             len_message = b''
        #             frame_byte = self.connect.recv(len_frame)
        #             if frame_byte != b'':
        #                 nparr = numpy.frombuffer(frame_byte, numpy.uint8)
        #                 frame_byte = b''
        #                 frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        #                 cv2.imshow('', frame)
        #                 if cv2.waitKey(10) & 0xFF == ord('q'):
        #                     return
        #                 event_collector.append(FrameEvent(frame))
        #                 # print("Things okay here")
        # except Exception as e:
        #     pass

    # def setup_socket(self, port):
    #     try:
    #         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #         host_name = socket.gethostname()
    #         host_ip = socket.gethostbyname(host_name)
    #         self.server_socket.bind((host_ip, port))
    #         self.server_socket.listen(5)
    #     except Exception as e:
    #         print(f"Failed to create socket: {str(e)}")
    #         raise e
