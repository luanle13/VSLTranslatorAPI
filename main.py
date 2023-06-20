import socket
import numpy
import pickle
import cv2

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('Host IP: ', host_ip)
port = 8000
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen(5)
data = b""
BUFFER_SIZE = 4665600
print('Listening at: ', socket_address)

# for i in range(1, 10):
#     sck, add = server_socket.accept()
#     if sck:
#         data = sck.recv(BUFFER_SIZE)
#         print(data)
#         m = b"K"
#         sck.sendall(m)
#         data = sck.recv(BUFFER_SIZE)
#         print(data)
#         m = b"B"
#         sck.sendall(m)
while True:
    sck, add = server_socket.accept()
    while sck:
        data = sck.recv(BUFFER_SIZE)
        # print(len(data))
        print(data)
        # if data != b"":
        #     # print(data)
        #     # nparr = numpy.frombuffer(data, numpy.uint8)
        #     # frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        #     # print(frame)
        #     # frame = numpy.frombuffer(data, numpy.uint8)
        #     # print(frame.size)
        #     # frame.reshape(320, 40, 3)
        #     print(data)
        # key = cv2.waitKey(1) & 0xFF
        # if key == ord('q'):
        #     break
    break