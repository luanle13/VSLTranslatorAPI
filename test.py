import socket, pickle, struct, cv2, imutils

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.120.158'
port = 9999
client_socket.connect((host_ip, port))