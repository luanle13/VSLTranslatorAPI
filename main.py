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
BUFFER_SIZE = 49860
print('Listening at: ', socket_address)
while True:
    client_socket, address = server_socket.accept()
    print('Got connection from: ', address)
    if client_socket:
        while len(data) < payload_size:
            pack = server_socket.recv(BUFFER_SIZE)
            if not pack:
                break
            data += pack
        pack_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", pack_msg_size)[0]
        while len(data) < msg_size:
            data += server_socket.recv(BUFFER_SIZE)
        vec_data = data[:msg_size]
        data = b""
        vec = pickle.loads(vec_data)
        res = model.predict(vec)
        buf = pickle.dumps(res)
        mes = struct.pack("Q", len(buf)) + buf
        try:
            client_socket.sendall(mes)
        except Exception as e:
            raise Exception(e)
