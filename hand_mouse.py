import cv2 as cv
import mediapipe as mp
import math
import win32api
import win32con
import screeninfo


def distance(a: tuple[int, int], b: tuple[int, int]):
    return abs(math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1] ** 2)))


cap = cv.VideoCapture(0)

# for tracking whether the mouse is held down
down = False

while cap.isOpened():
    success, img = cap.read()

    # hand tracker
    with mp.solutions.hands.Hands() as hands:
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        improcess = hands.process(imgRGB)
        landmarks = improcess.multi_hand_landmarks

        if landmarks:

            # get position of fingers
            index_finger = landmarks[0].landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger = (index_finger.x, index_finger.y)

            thumb = landmarks[0].landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
            thumb = (thumb.x, thumb.y)

            # find relative mouse position
            screen = screeninfo.get_monitors()[0]
            mouse_pos = (int(screen.width * (1 - thumb[0])), int(screen.height * thumb[1]))

            # set cursor position to thumb position (index finger moves too much)
            win32api.SetCursorPos(mouse_pos)

            # distance between thumb and index finger
            dist = distance(index_finger, thumb)
            dist = dist <= .55

            # do click
            if dist and not down:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, mouse_pos[0], mouse_pos[1], 0, 0)
                down = True
            elif dist:
                pass
            elif down:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, mouse_pos[0], mouse_pos[1], 0, 0)
                down = False

    cv.imshow('Window', img)
    cv.waitKey(1)
