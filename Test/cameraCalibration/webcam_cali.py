import cv2 as cv
import numpy as np
import pickle

# 캘리브레이션 데이터 로드
with open("calibration.pkl", "rb") as f:
    cameraMatrix, dist = pickle.load(f)

# 웹캠 설정
cap = cv.VideoCapture(0) # 0은 기본 웹캠

if not cap.isOpened():
    print("웹캠을 열 수 없습니다.")
    exit()

while True:
    # 웹캠으로부터 영상 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다. 종료합니다.")
        break

    # 영상 보정
    frame_undistorted = cv.undistort(frame, cameraMatrix, dist, None)

    # 보정된 영상 출력
    cv.imshow('Undistorted Image', frame_undistorted)

    # 'q'를 누르면 반복문 탈출
    if cv.waitKey(1) == ord('q'):
        break

# 종료 처리
cap.release()
cv.destroyAllWindows()
