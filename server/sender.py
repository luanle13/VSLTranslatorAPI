import websockets
import threading
import asyncio
from queue import Queue


class Sender:
    def __init__(self, port) -> None:
        self.port = port
        self.output = Queue(64)

    def set_out_data(self, data):
        # self.frame_data = data
        self.output.put(data)

    def get_out_data(self):
        # return self.frame_data
        return self.output.get()

    async def send(self, websocket, path):
        if self.output.not_empty:
            await websocket.send(self.get_out_data())


    def serve_callback(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ws_server = websockets.serve(self.send, 'localhost', self.port)
        loop.run_until_complete(ws_server)
        loop.run_forever()
        loop.close()

    def run(self):
        threading.Thread(target=self.serve_callback, daemon=True).start()
