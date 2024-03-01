import cv2
import socket
import pickle
import numpy as np
from dataclasses import dataclass
import struct
import sys

host = "172.30.1.79"
port = 8500
max_length = 65540

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 8000))

while True:
    #sock.sendto(bytes("input_string", 'utf-8'),(host, port))
    
    data, address = sock.recvfrom(max_length)
    if len(data) < 100:
        frame_info = pickle.loads(data)
        if frame_info:
            nums_of_packs = frame_info["packs"]

            for i in range(nums_of_packs):
                data, address = sock.recvfrom(max_length)

                if i == 0:
                    buffer = data
                else:
                    buffer += data

            frame = np.frombuffer(buffer, dtype=np.uint8)
            frame = frame.reshape(frame.shape[0], 1)

            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            frame = cv2.flip(frame, 1)
            
            if frame is not None and type(frame) == np.ndarray:
                cv2.imshow("Stream", frame)
                if cv2.waitKey(1) == 27:
                    break