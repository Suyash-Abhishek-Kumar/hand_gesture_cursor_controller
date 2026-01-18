import cv2
import mediapipe as mp
import pyautogui
import time
import math
from util import get_angle, get_distance

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands = 1, min_detection_confidence = 0.7, min_tracking_confidence = 0.6)

# gesture time control
pinch_start_time = None
click_times_L = []
click_times_R = []
click_cooldown = 0.5
sensitivity = 2
scroll_mode = False
freeze_cursor = False
is_dragging = False
screenshot_cooldown = 2
last_screenshot_time = 0

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
        index_connector = handLm.landmark[7]
        middle_tip = handLm.landmark[12]
        ring_tip = handLm.landmark[16]
        pinky_tip = handLm.landmark[20]

        fingers = [1 if handLm.landmark[tip].y < handLm.landmark[tip - 2].y else 0 for tip in [8, 12, 16, 20]]

        # Move Cursor
        if not freeze_cursor:
            # Normalize around center
            cx = (index_tip.x - 0.5) * sensitivity + 0.5
            cy = (index_tip.y - 0.5) * sensitivity + 0.5

            # Convert to screen space
            screen_x = int(cx * screen_w)
            screen_y = int(cy * screen_h)

            # Clamp to safe bounds
            screen_x = max(10, min(screen_w - 10, screen_x))
            screen_y = max(10, min(screen_h - 10, screen_y))

            # Smooth movement: Interpolate
            if prev_screen_x is not None and prev_screen_y is not None:
                screen_x = prev_screen_x + (screen_x - prev_screen_x) * 0.3
                screen_y = prev_screen_y + (screen_y - prev_screen_y) * 0.3

            pyautogui.moveTo(screen_x, screen_y, duration=0.01)
            prev_screen_x, prev_screen_y = screen_x, screen_y

        # Left Clicks
        distance_L = math.hypot(thumb_tip.x - index_connector.x, thumb_tip.y - index_connector.y)
        if distance_L < 0.05:
            if not freeze_cursor:
                freeze_cursor = True
                click_times_L.append(time.time())
                
                if len(click_times_L) >= 2 and click_times_L[-1] - click_times_L[-2] < 0.5:
                    pyautogui.doubleClick()
                    click_times_L = []
                else:
                    pyautogui.click()
        else:
            if freeze_cursor:
                time.sleep(0.1)
            freeze_cursor = False
        
        #Right Clicks
        distance_R = math.hypot(thumb_tip.x - middle_tip.x, thumb_tip.y - middle_tip.y)
        if distance_R < 0.05:
            if not freeze_cursor:
                freeze_cursor = True
                click_times_R.append(time.time())

                if len(click_times_R) >= 2 and click_times_R[-1] - click_times_R[-2] < 0.5:
                    pyautogui.doubleClick(button="right")
                    click_times_R = []
                else:
                    pyautogui.click(button="right")
        else:
            if freeze_cursor:
                time.sleep(0.1)
            freeze_cursor = False
        
        # Scroll
        if sum(fingers) == 4:
            scroll_mode = True
        else:
            scroll_mode = False
        
        # Scroll Actions
        if scroll_mode:
            if index_tip.y < 0.4:
                pyautogui.scroll(60)
            elif index_tip.y > 0.6:
                pyautogui.scroll(-60)

        

    cv2.imshow("Live Video", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()