from api import Operator
import socketio
import eventlet
# import socket


class OutputEmittor(Operator):
    def __init__(self, name, parallelism, port, grouping=None):
        super().__init__(name, parallelism, grouping)
        self.instance = 0
        self.port_base = port
        self.sio = socketio.Server(async_mode='eventlet')
        self.app = socketio.WSGIApp(self.sio)
        eventlet.wsgi.server(eventlet.listen(('', self.port_base)), self.app)

    def setup_instance(self, instance):
        self.instance = instance
        # self.setup_socket(self.port_base + instance)

    def apply(self, event, event_collector):
        @self.sio.event
        def connect(sid, environ):
            print(f'Client connected: {sid}')

        @self.sio.event
        def disconnect(sid):
            print(f'Client disconnected: {sid}')

        self.sio.emit('label', event)

        # try:
        #     if self.connect == None:
        #         self.connect, address = self.server_socket.accept()
        #     else:
        #         data = event.get_data()
        #         if data is not None:
        #             message = int(data).to_bytes(8, 'big')
        #             self.connect.sendall(message)
        #             data = None
        #     # data = event.get_data()
        #     # print("Output Emitter")
        #     # print(data)
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
    #         pass
