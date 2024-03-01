import numpy as np
import cv2

cap = cv2.VideoCapture(1)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

kernel = np.ones((3, 3))/3**2 #블러치리할 영역(), 나눌 숫자

array = np.array([[1, 1, 1, 1],[1, 1, 1, 1],[1, 1, 1, 1],[1, 1, 1, 1]]) #침식 범위
#array = np.array([[1, 1, 1, 1, 1],[1, 1, 1, 1, 1],[1, 1, 1, 1, 1],[1, 1, 1, 1, 1],[1, 1, 1, 1, 1]]) #침식 범위
#array = np.array([[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1],[1, 1, 1, 1, 1, 1],[1, 1, 1, 1, 1, 1],[1, 1, 1, 1, 1, 1],[1, 1, 1, 1, 1, 1]]) #침식 범위

ret_pre_frame, pre_frame = cap.read()

while cap.isOpened():
    success, frame = cap.read()
    if success:
        frame1_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blured = cv2.filter2D(frame1_gray, -1, kernel) #블러처리

        ret_set_binary, set_binary = cv2.threshold(blured, 200, 255, cv2.THRESH_BINARY) #이진화
        
        erode = cv2.erode(set_binary, array) #침식
        dilate = cv2.dilate(erode, array) #팽창

        cv2.imshow('Camera Window1', dilate)
        cv2.imshow('Camera Window2', frame)
        
        white_pixel_coordinates = np.column_stack(np.nonzero(dilate))

        if len(white_pixel_coordinates) > 0:
            center = np.mean(white_pixel_coordinates, axis=0)
            center = tuple(map(int, center))  # 정수형으로 변환
            y = center[0] - 240
            x = center[1] - 320
            print(x, ',', y)

        # ESC를 누르면 종료
        key = cv2.waitKey(1) & 0xFF
        if (key == 27): 
            break
 
cap.release()
cv2.destroyAllWindows()