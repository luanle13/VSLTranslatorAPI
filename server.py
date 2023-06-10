import socket, cv2, pickle, struct, imutils

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('Host IP: ', host_ip)
port = 9999
socket_address = (host_ip, port)

server_socket.bind(socket_address)

server_socket.listen(5)
print("Listening at: ", socket_address)

while True:
    client_socket, address = server_socket.accept()
    print('Got connection from: ', address)
    if client_socket:
        vid = cv2.VideoCapture(0)
        while (vid.isOpened()):
            img, frame = vid.read()
            frame = imutils.resize(frame, width=320)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            try:
                client_socket.sendall(message)
            except Exception as e:
                print(e)
                raise Exception(e)
            cv2.imshow('TRANSMITTING VIDEO', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()