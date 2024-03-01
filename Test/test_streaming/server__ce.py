import cv2
import socket
import math
import pickle
import sys
from dataclasses import dataclass
import struct
import time

max_length = 65000
host = "172.30.1.79"
port = 9000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

cap = cv2.VideoCapture(0)

ret, frame = cap.read()

while True:
    # compress frame
    # data_ = sock.recvfrom(max_length)
    # print(data_)

    ret, frame = cap.read()
    if ret:
        retval, buffer = cv2.imencode(".jpg", frame)
        if retval:
            buffer = buffer.tobytes()
            buffer_size = len(buffer)

            num_of_packs = 1
            if buffer_size > max_length:
                num_of_packs = math.ceil(buffer_size/max_length)

            frame_info = {"packs":num_of_packs}

            #sock.sendto(pickle.dumps(frame_info), (host, 8000))
            left = 0
            right = max_length

            for i in range(num_of_packs):
                data = buffer[left:right]
                left = right
                right += max_length

                sock.sendto(data, (host, 8000))