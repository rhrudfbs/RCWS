import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np

# 모델 로드
model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
movenet = model.signatures['serving_default']

def draw_bounding_box(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))
    valid_points = [kp for kp in shaped if kp[2] > confidence_threshold]
    if not valid_points:
        return None

    min_x = min([kp[1] for kp in valid_points])
    min_y = min([kp[0] for kp in valid_points])
    max_x = max([kp[1] for kp in valid_points])
    max_y = max([kp[0] for kp in valid_points])

    cv2.rectangle(frame, (int(min_x), int(min_y)), (int(max_x), int(max_y)), (255, 0, 0), 2)
    return (min_x, min_y, max_x, max_y)

def loop_through_people(frame, keypoints_with_scores, confidence_threshold):
    rectangles = []
    for person in keypoints_with_scores:
        # 트래커가 활성화되지 않았을 때만 바운딩 박스를 그립니다.
        if tracker is None:
            rect = draw_bounding_box(frame, person, confidence_threshold)
            if rect is not None:
                rectangles.append(rect)
    return rectangles

# Tracker 초기화
tracker = None

def mouse_callback(event, x, y, flags, param):
    global tracker
    if event == cv2.EVENT_LBUTTONDOWN:
        for rect in rectangles_info:
            min_x, min_y, max_x, max_y = rect
            if min_x <= x <= max_x and min_y <= y <= max_y:
                tracker = cv2.TrackerCSRT_create()
                bbox = (int(min_x), int(min_y), int(max_x - min_x), int(max_y - min_y))
                tracker.init(frame, bbox)
                break
    elif event == cv2.EVENT_RBUTTONDOWN:
        tracker = None


gpus = tf.config.list_physical_devices('GPU')
if gpus:
  # 텐서플로가 첫 번째 GPU만 사용하도록 제한
  try:
    tf.config.set_visible_devices(gpus[2], 'GPU')
  except RuntimeError as e:
    # 프로그램 시작시에 접근 가능한 장치가 설정되어야만 합니다
    print(e)

# gpus = tf.config.experimental.list_physical_devices('GPU')
# for gpu in gpus:
#     tf.config.experimental.set_memory_growth(gpu[1], True)

cap = cv2.VideoCapture(0)
cv2.namedWindow("Movenet Multipose")
cv2.setMouseCallback("Movenet Multipose", mouse_callback)

while cap.isOpened():
    ret, frame = cap.read()
    
    if ret:
        img = frame.copy()
        img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 480, 640)
        input_img = tf.cast(img, dtype=tf.int32)
    
        results = movenet(input_img)
        keypoints_with_scores = results['output_0'].numpy()[:,:,:51].reshape((6,17,3))
    
        rectangles_info = loop_through_people(frame, keypoints_with_scores, 0.5)

        if tracker is not None:
            success, bbox = tracker.update(frame)
            if success:
                x, y, w, h = [int(v) for v in bbox]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                print(((x + x + w) / 2) - 320, ', ', ((y + y + h) / 2) - 240)
            else:
                # 트래킹 실패 시 트래커 리셋
                tracker = None
    
    cv2.imshow('Movenet Multipose', frame)
    
    if cv2.waitKey(3) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
