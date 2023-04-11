import numpy as np
import cv2
import imutils
import pyautogui
from typing import Optional

face_cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./models/haarcascade_eye.xml')

def detect_eyes(input):
    input = imutils.resize(input, width=700)
    grayscale = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)

    detected_face = face_cascade.detectMultiScale(grayscale, scaleFactor=1.3, minNeighbors=6)

    for (x, y, w, h) in detected_face:
        gray_frame = grayscale[y:y + (h // 2), x:x + w]
        #face_rectangle = input[y:y + h, x:x + w]
        detected_eyes = eye_cascade.detectMultiScale(gray_frame, 1.3, 5)

        left_eye = None
        right_eye = None


        if len(detected_eyes) > 0:
            for (x_1, y_1, w_1, h_1) in detected_eyes:
                eyecenter = x_1 + w_1 / 2  # get the eye center
                if eyecenter < w * 0.5:
                    left_eye = gray_frame[y_1:y_1 + h_1, x_1:x_1 + w_1]
                    left_eye = cv2.GaussianBlur(left_eye, (3, 3), 0)
                else:
                    right_eye = gray_frame[y_1:y_1 + h_1, x_1:x_1 + w_1]
                    right_eye = cv2.GaussianBlur(right_eye, (3, 3), 0)
            
            if (left_eye, right_eye):
                return [left_eye, right_eye]
