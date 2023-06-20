import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 8000
data = b""
BUFFER = 256

client_socket.connect((host_ip, port))
while True:
    data = client_socket.recv(BUFFER)
    if data is not None:
        data = int.from_bytes(data, byteorder='big')
        print(data)