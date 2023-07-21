import websockets
import threading
import asyncio
import cv2
import base64
import numpy as np


async def receive_message(uri):
    async with websockets.connect(uri, ping_interval=None) as websocket:
        while True:
            data = await websocket.recv()
            await websocket.send('')
            print(data)


def client():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(receive_message('ws://localhost:8000'))
    # loop.run_forever()
    loop.close()


if __name__ == "__main__":
    c = threading.Thread(target=client, daemon=True)
    c.start()
    c.join()
    # client()