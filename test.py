import socket
import cv2
import imutils

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostbyname(socket.gethostname()), 9990))
vid = cv2.VideoCapture(0)
while vid.isOpened():
    _, frame = vid.read()
    image = imutils.resize(frame, width=320, height= 120)
    # cv2.imshow('',image)
    frame_byte = cv2.imencode('.jpg', frame)[1].tobytes()
    len_message = len(frame_byte).to_bytes(length=8, byteorder='big')
    len_frame = int.from_bytes(len_message, byteorder='big')
    # print(len_frame)
    try:
        client_socket.sendall(len_message)
        client_socket.sendall(frame_byte)
    except Exception as e:
        raise e
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break