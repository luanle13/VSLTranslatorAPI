# import socketio
# import cv2
# import imutils

# # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # client_socket.connect((socket.gethostbyname(socket.gethostname()), 9990))
# sio = socketio.AsyncClient()
# # sio2 = socketio.Client()
# sio.connect('http://localhost:9990', wait_timeout=100)
# # sio2.connect('http://0.0.0.0:8000')
# vid = cv2.VideoCapture(0)

# # @sio2.on('label')
# # def print_label(data):
# #     print(data)

# while vid.isOpened():
#     _, frame = vid.read()
#     image = imutils.resize(frame, width=320, height=120)
#     # cv2.imshow('',image)
#     frame_byte = cv2.imencode('.jpg', frame)[1].tobytes()
#     # len_message = len(frame_byte).to_bytes(length=8, byteorder='big')
#     # len_frame = int.from_bytes(len_message, byteorder='big')
#     # print(len_frame)
#     try:
#         # client_socket.sendall(len_message)
#         sio.emit('frame', 'abcd')
#         sio.disconnect()
#         break
#     except Exception as e:
#         raise e
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         sio.disconnect()
#         break
import websockets
import threading
import asyncio
import cv2
import base64
import numpy as np


vid = cv2.VideoCapture(0)


async def send_message(uri):
    async with websockets.connect(uri) as websocket:
        while vid.isOpened():
            _, frame = vid.read()
            _, img_arr = cv2.imencode('.jpg', frame)
            await websocket.send(base64.b64encode(img_arr.tobytes()))


def client():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_message('ws://localhost:9990'))
    # loop.run_forever()
    loop.close()


if __name__ == "__main__":
    c = threading.Thread(target=client, daemon=True)
    c.start()
    c.join()
    # client()