import numpy as np
import cv2
import imutils
import pyautogui
from typing import Optional

# https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./models/haarcascade_eye.xml')


def detect_eyes(input):
    input = imutils.resize(input, width=700)
    grayscale = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)

    detected_face = face_cascade.detectMultiScale(grayscale, scaleFactor=1.3, minNeighbors=6)

    for (x, y, w, h) in detected_face:
        gray_frame = grayscale[y:y + (h // 2), x:x + w]
        face_rectangle = input[y:y + h, x:x + w]
        detected_eyes = eye_cascade.detectMultiScale(gray_frame, 1.3, 5)

        for (x_1, y_1, w_1, h_1) in detected_eyes:
            gray_eye_frame = gray_frame[y_1:y_1 + h_1, x_1:x_1 + w_1]
            blur = cv2.GaussianBlur(gray_eye_frame, (3, 3), 0)
            return blur

        #     cv2.drawKeypoints(eye_frame, keypoints, eye_frame, (0, 255, 255),
        #                       flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # commented out for now as this is not effecient and leads to delays
        # if keypoints:
        #     x, y = keypoints[0].pt
        #     pyautogui.FAILSAFE=False
        #     # determine the direction by comparing the x, y coordinates of the keypoints
        #     if x > w_1 / 2:
        #         print("Eyes are facing right")
        #         pyautogui.moveRel(-25, 0)
        #     elif x < w_1 / 2:
        #         print("Eyes are facing left")
        #         pyautogui.moveRel(25, 0)
        #     if y > h_1 / 2:
        #         print("Eyes are facing down")
        #         pyautogui.moveRel(0, 25)
        #     elif y < h_1 / 2:
        #         print("Eyes are facing up")
        #         pyautogui.moveRel(0, -25)

    cv2.imshow('output', input)
