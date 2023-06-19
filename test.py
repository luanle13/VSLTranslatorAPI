import socket
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
while True:
    for vehicle in vehicles:
        message = vehicle
        if message != None:
            client_socket.send(message.encode())