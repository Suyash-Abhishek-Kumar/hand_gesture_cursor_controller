import cv2
import mediapipe as mp
import pyautogui
import time
import math

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands = 1, min_detection_confidence = 0.7, min_tracking_confidence = 0.6)

# gesture time control
click_start_time = None
click_times = []
click_cooldown = 0.5
sensitivity = 3
scroll_mode = False
freeze_cursor = False

screen_w, screen_h = pyautogui.size()
prev_screen_x, prev_screen_y = 0, 0

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

    if result.multi_hand_landmarks:
        for handLm in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, handLm, mp_hands.HAND_CONNECTIONS)

        thumb_tip = handLm.landmark[4]
        index_tip = handLm.landmark[8]
        middle_tip = handLm.landmark[12]
        ring_tip = handLm.landmark[16]
        pinky_tip = handLm.landmark[20]

        fingers = [1 if handLm.landmark[tip].y < handLm.landmark[tip - 2].y else 0 for tip in [8, 12, 16, 20]]

        # Left Clicks
        distance = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
        if distance < 0.05:
            if not freeze_cursor:
                freeze_cursor = True
                click_times.append(time.time())
                
                if len(click_times) >= 2 and click_times[-1] - click_times[-2] < 0.5:
                    pyautogui.doubleClick()
                    cv2.putText(frame, "Double Click", (10, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255, 0, 255), 2)
                    click_times = []
                else:
                    pyautogui.click()
                    cv2.putText(frame, "Single Click", (10, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255, 0, 255), 2)
        else:
            if freeze_cursor:
                time.sleep(0.1)
            freeze_cursor = False

        #Move Cursor
        if not freeze_cursor:
            screen_x = max(min(int(index_tip.x * screen_w * sensitivity), screen_w - 10), 10)
            screen_y = max(min(int(index_tip.y * screen_h * sensitivity), screen_h - 10), 10)
            if prev_screen_x and prev_screen_y:
                screen_x = prev_screen_x + (screen_x - prev_screen_x) * 0.3
                screen_y = prev_screen_y + (screen_y - prev_screen_y) * 0.3

            pyautogui.moveTo(screen_x, screen_y, duration = 0.01)
            prev_screen_x, prev_screen_y = screen_x, screen_y
    
    cv2.imshow("Live Video", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()