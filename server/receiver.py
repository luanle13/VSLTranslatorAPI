import websockets
import threading
import asyncio
from queue import Queue


class Receiver:
    def __init__(self, port) -> None:
        self.port = port
        self.frame_data = Queue(64)

    def set_frame_data(self, data):
        # self.frame_data = data
        self.frame_data.put(data)

    def get_frame_data(self):
        # return self.frame_data
        return self.frame_data.get()

    async def frame(self, websocket, path):
        data = await websocket.recv()
        # print(data)
        self.set_frame_data(data)

    def serve_callback(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ws_server = websockets.serve(self.frame, 'localhost', self.port)
        loop.run_until_complete(ws_server)
        loop.run_forever()
        loop.close()

    def run(self):
        threading.Thread(target=self.serve_callback, daemon=True).start()
