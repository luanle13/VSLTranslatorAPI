import socket
import cv2
import pickle
import imutils
import struct
import tensorflow
from tensorflow import keras

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
model = keras.models.load_model('./action.h5')
print('Host IP: ', host_ip)
port = 9999
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen(5)
payload_size = struct.calcsize("Q")
data = b""
BUFFER_SIZE = 4 * 1024
print('Listening at: ', socket_address)
i = 0
while i < 30:
    try:
        i += 1
        sck, add = server_socket.accept()
        print('Got connection from: ', add)
        if sck:
            data = sck.recv(BUFFER_SIZE)
            print(data)
            m = b"456"
            sck.sendall(m)
    except Exception as e:
        print(e)
        raise Exception(e)
