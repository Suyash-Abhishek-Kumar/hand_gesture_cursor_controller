import cv2  # video processing
import mediapipe as mp
import pyautogui as pg


def main():
    vid = cv2.VideoCapture(0)  # Start video capture from the default camera (index 0)
    vid.set(3, 960)  # Set the width of the video (3 = camera property) frame to 960 pixels
    mphands = mp.solutions.hands
    Hands = mphands.Hands(max_num_hands = 2, min_detection_confidence = 0.7, min_tracking_confidence = 0.6)
    mpDraw = mp.solutions.drawing_utils

    while vid.isOpened():
        success, frame = vid.read()  # Read a frame from the video capture
        frame = cv2.flip(frame, 1)

        # Convert from BGR to RGB
        RGBframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = Hands.process(RGBframe)
        if result.multi_hand_landmarks:
            # print("hand found")
            for handLm in result.multi_hand_landmarks:
                for id, landmark in enumerate(handLm.landmark):
                    height, width, _ = frame.shape
                    cx, cy = int(landmark.x * width), int(landmark.y * height)
                    mpDraw.draw_landmarks(frame, handLm, mphands.HAND_CONNECTIONS)

                    #Thumb Tip
                    if id == 4:
                        thumb = (int(landmark.x * width), int(landmark.y * height))
                        cv2.circle(frame, thumb, 7, (255, 0, 255), cv2.FILLED)

        cv2.imshow("Video", frame)  # Display the frame in a window named "Video"
        cv2.waitKey(1)  # Wait for 1 millisecond before displaying the next frame


if __name__ == "__main__":
    main()