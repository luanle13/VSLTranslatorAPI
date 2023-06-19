import socket
import struct
import cv2
import imutils
import pickle
import numpy
import time
import sys

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 9990
data = b""
# BUFFER_SIZE = 1
# img, frame = vid.read()
# message = cv2.imencode('', frame)[1]
vehicles = [
    'bus',
    'van',
    'bike',
    'truck',
    'van',
    'bike',
    'truck',
    'bike',
    'bike',
    'bike',
    'van',
    'bike',
    'truck',
    'bike',
    'bike',
]
client_socket.connect((host_ip, port))
# while True:
#     for vehicle in vehicles:
#         try:
#             message = vehicle
#             if message != None:
#                 print(message)
#                 client_socket.send(message.encode())
#                 time.sleep(0.3)
#         except Exception as e:
#             raise e
#     time.sleep(2)
vid = cv2.VideoCapture(0)
while vid.isOpened():
    img, frame = vid.read()
    frame = imutils.resize(frame, width=320, height=60)
    message = cv2.imencode('.jpg', frame)[1]
    # print(len(message))
    try:
        client_socket.sendall(message)
    except Exception as e:
        raise e
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        client_socket.close()