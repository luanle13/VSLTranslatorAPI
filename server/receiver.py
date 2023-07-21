# import websockets
# import threading
# import asyncio
# from queue import Queue


# class Receiver:
#     def __init__(self, port) -> None:
#         self.port = port
#         self.frame_data = Queue(64)

#     def set_frame_data(self, data):
#         # self.frame_data = data
#         self.frame_data.put(data)

#     def get_frame_data(self):
#         # return self.frame_data
#         return self.frame_data.get()

#     async def frame(self, websocket, path):
#         print("RECEIVER: Client connected")
#         try:
#             while True:
#                 data = await websocket.recv()
#                 # print(data)
#                 if data != None:
#                     self.set_frame_data(data)
#         except websockets.ConnectionClosed:
#             print("RECEIVER: Client disconnected")

#     def serve_callback(self):
#         # while True:
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         ws_server = websockets.serve(self.frame, 'localhost', self.port)
#         loop.run_until_complete(ws_server)
#         loop.run_forever()
#         loop.close()

#     def run(self):
#         threading.Thread(target=self.serve_callback, daemon=True).start()


import websockets
import threading
import asyncio
from queue import Queue

class Receiver:
    def __init__(self, port) -> None:
        self.port = port
        self.frame_data = Queue(64)
        self.connected_clients = set()

    def set_frame_data(self, data):
        self.frame_data.put(data)

    def get_frame_data(self):
        return self.frame_data.get()

    async def frame(self, websocket, path):
        print("RECEIVER: Client connected")
        self.connected_clients.add(websocket)
        try:
            while True:
                data = await websocket.recv()
                if data is not None:
                    self.set_frame_data(data)
        except websockets.ConnectionClosed:
            print("RECEIVER: Client disconnected")
        finally:
            self.connected_clients.remove(websocket)

    # async def send_data_to_clients(self):
    #     while True:
    #         data = self.get_frame_data()
    #         for client in self.connected_clients:
    #             try:
    #                 await client.send(data)
    #             except websockets.ConnectionClosed:
    #                 print("RECEIVER: Error sending data. Client disconnected.")
    #                 self.connected_clients.remove(client)

    def serve_callback(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ws_server = websockets.serve(self.frame, 'localhost', self.port)
        loop.run_until_complete(ws_server)
        # asyncio.ensure_future(self.send_data_to_clients())
        loop.run_forever()

    def run(self):
        threading.Thread(target=self.serve_callback, daemon=True).start()
