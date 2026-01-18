import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands = 1, min_detection_confidence = 0.7, min_tracking_confidence = 0.6)

if not cap.isOpened():
    print("Cannot open Camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot recieve frame")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    height, width, _ = frame.shape

    if result.multi_hand_landmarks:
        for handLm in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, handLm, mp_hands.HAND_CONNECTIONS)
            for id, landmark in enumerate(handLm.landmark):
                if id % 4 == 0:
                    point = (int(landmark.x * width), int(landmark.y * height))
                    cv2.circle(frame, point, 7, (255, 0, 255), 10)
    
    cv2.imshow("Live Video", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()