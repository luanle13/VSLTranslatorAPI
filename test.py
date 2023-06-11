import socket
import cv2
import imutils
import pickle
import numpy

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.120.158'
port = 9999
client_socket.connect((host_ip, port))
data = b""
# BUFFER_SIZE = 1

# for i in range(1, 10):
#     m = b"G"
#     client_socket.sendall(m)
#     data = client_socket.recv(BUFFER_SIZE)
#     print(data)
#     m = b"A"
#     client_socket.sendall(m)
#     data = client_socket.recv(BUFFER_SIZE)
#     print(data)
vid = cv2.VideoCapture(0)

while vid.isOpened():
    img, frame = vid.read()
    # frame = imutils.resize(frame, width=40, height=640)
    # frame = cv2.resize(frame, (320, 40))
    # print(frame)
    message = cv2.imencode('.jpg', frame)[1]
    # print(frame.size)
    # message = numpy.array(frame, numpy.uint8)
    # print(message.size)
    client_socket.sendall(message)