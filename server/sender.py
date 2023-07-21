# import websockets
# import threading
# import asyncio
# from queue import Queue


# class Sender:
#     def __init__(self, port) -> None:
#         self.port = port
#         self.output = Queue(64)

#     def set_out_data(self, data):
#         # self.frame_data = data
#         self.output.put(data)

#     def get_out_data(self):
#         # return self.frame_data
#         return self.output.get()

#     async def send(self, websocket, path):
#         print("SENDER: Client connected")
#         while True:
#             # data = self.get_out_data()
#             # if data is not None:
#             try:
#                 await websocket.send(str(self.get_out_data()))
#                 await websocket.recv()
#             except Exception as e:
#                 print(e)


#     def serve_callback(self):
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         # while True:
#         ws_server = websockets.serve(self.send, 'localhost', self.port, ping_interval=None)
#         loop.run_until_complete(ws_server)
#         loop.run_forever()
#         loop.close()

#     def run(self):
#         c = threading.Thread(target=self.serve_callback, daemon=True)
#         c.start()


import websockets
import threading
import asyncio
from queue import Queue


class Sender:
    def __init__(self, port) -> None:
        self.port = port
        self.output = Queue(64)
        self.connected_clients = set()

    def set_out_data(self, data):
        self.output.put(data)

    def get_out_data(self):
        return self.output.get()

    async def send(self, websocket, path):
        print("SENDER: Client connected")
        self.connected_clients.add(websocket)
        try:
            while True:
                try:
                    await websocket.send(str(self.get_out_data()))
                    await websocket.recv()
                except websockets.ConnectionClosed:
                    print("SENDER: Client disconnected")
                    break
        finally:
            self.connected_clients.remove(websocket)
            

    def serve_callback(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ws_server = websockets.serve(self.send, 'localhost', self.port, ping_interval=None)
        loop.run_until_complete(ws_server)
        # asyncio.ensure_future(self.broadcast_data())
        loop.run_forever()

    def run(self):
        threading.Thread(target=self.serve_callback, daemon=True).start()



# import websockets
# import threading
# import asyncio
# from queue import Queue

# my_connections = set()

# class Sender:
#     def __init__(self, port) -> None:
#         self.port = port
#         self.output = Queue(64)

#     def set_out_data(self, data):
#         # self.frame_data = data
#         self.output.put(data)

#     def get_out_data(self):
#         # return self.frame_data
#         return self.output.get()

#     async def send(self, websocket, path):
#         print("SENDER: Client connected")
#         my_connections.add(websocket)

#         async with websockets.connect('ws://192.168.120.158:8000', ping_interval=None) as ws:
#             while True:
#                 data = self.get_out_data()
#                 if data is not None:
#                     try:
#                         # await websocket.send(str(data))
#                         # print('Sent data to remote address: ', websocket.remote_address)
#                         # await ws.send(str(data))
#                         # print('new send')

#                         for client in my_connections:
#                             await client.send(str(data))
#                             print('send to client: ', data)
#                             print('Sent data to remote address: ', websocket.remote_address)

#                     except Exception as e:
#                         print(e)

#     def serve_callback(self):
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         ws_server = websockets.serve(self.send, '192.168.120.158', 8000, ping_interval=None)
#         loop.run_until_complete(ws_server)
#         loop.run_forever()
#         loop.close()

#     def run(self):
#         threading.Thread(target=self.serve_callback, daemon=True).start()
