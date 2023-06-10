import socket
import pickle
import struct
import cv2
import imutils

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.1.12'
port = 9999
client_socket.connect((host_ip, port))
data = b""
payload_size = struct.calcsize("Q")
vid = cv2.VideoCapture(0)
BUFFER_SIZE = 4 * 1024
i = 0
while i < 30:
    try:
        i += 1
        m = b"123"
        client_socket.sendall(m)
        data = client_socket.recv(BUFFER_SIZE)
        print(data)
    except Exception as e:
        print(e)
        raise Exception(e)
