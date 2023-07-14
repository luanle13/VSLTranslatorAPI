from api import Source
import socket
from event import FrameEvent
import cv2
import numpy as np
import eventlet
import socketio
import asyncio
from websockets.server import serve
from queue import Queue
from aiohttp import web
import base64


class FrameReader(Source):
    def __init__(self, name, parallelism, get_frame_callback):
        super().__init__(name, parallelism)
        self.get_frame_callback = get_frame_callback
        self.instance = 0


    def setup_instance(self, instance):
        self.instance = instance


    # def setup_socket(self, port):
    #     sio = socketio.AsyncServer()
    #     app = web.Application()
    #     sio.on('connect', self.connect)
    #     sio.on('frame', self.frame)
    #     sio.on('disconnect', self.disconnect)
    #     sio.attach(app)
    #     web.run_app(app)


    # def connect(self, sid, environ):
    #     print(f'Client connected: {sid}')


    # def disconnect(self, sid):
    #     print(f'Client disconnected: {sid}')


    async def frame(self, sid, data):
        print("Hello")
        nparr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imshow('receive', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            return
        self.data = img
        print(self.data)


    def get_events(self, event_collector):
        # print('vao get_events')
        data = self.get_frame_callback()
        # print(data)
        if data is not None:
            im_bytes = base64.b64decode(data)
            nparr = np.frombuffer(im_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imshow('receive', img)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                return
            event_collector.append(FrameEvent(img))

    

    
    # def call_back(self):
    #     @self.sio.on('connect')
    #     def connect(sid, environ):
    #         print(f'Client connected: {sid}')

    #     @self.sio.on('disconnect')
    #     def disconnect(sid):
    #         print(f'Client disconnected: {sid}')
        
    #     @self.sio.on('frame')
    #     def frame(sid, data):
    #         print(data)
            # nparr = np.frombuffer(data, np.uint8)
            # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # cv2.imshow('receive', img)
            # if cv2.waitKey(10) & 0xFF == ord('q'):
            #     return
            # self.event_collector.append(FrameEvent(img))

    # def get_events(self, event_collector):
    #     try:
    #         # self.count += 1
    #         # print(f"Frame Reader: {self.count}")
    #         if self.connect == None:
    #             self.connect, address = self.server_socket.accept()
    #             print(f"Client {address} connected on {self.connect}")
    #         else:
    #             header_buffer = b''
    #             while b'\n\n' not in header_buffer:
    #                 print(data)
    #                 data = self.connect.recv(1)
    #                 header_buffer += data
    #             len_message = b''
    #             frame_byte = b''
    #             len_message = self.connect.recv(8000)
    #             print(len_message)
    #             if len_message != b'':
    #                 len_frame = int.from_bytes(len_message)
    #                 len_message = b''
    #                 frame_byte = self.connect.recv(len_frame)
    #                 if frame_byte != b'':
    #                     nparr = np.frombuffer(frame_byte, np.uint8)
    #                     frame_byte = b''
    #                     frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    #                     cv2.imshow('', frame)
    #                     if cv2.waitKey(10) & 0xFF == ord('q'):
    #                         return
    #                     event_collector.append(FrameEvent(frame))
    #                     # print("Things okay here")
    #     except Exception as e:
    #         pass

    # def setup_socket(self, port):
    #     try:
    #         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #         host_name = socket.gethostname()
    #         host_ip = socket.gethostbyname(host_name)
    #         self.server_socket.bind((host_ip, port))
    #         self.server_socket.listen(120)
    #         print(f"Listening on {host_ip}:{port}")
    #     except Exception as e:
    #         print(f"Failed to create socket: {str(e)}")
    #         raise e
