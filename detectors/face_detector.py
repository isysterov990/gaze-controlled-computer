import numpy as np
import cv2
import imutils
import pyautogui
from typing import Optional

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./models/haarcascade_eye.xml')

parameters = cv2.SimpleBlobDetector_Params()

parameters.filterByColor = False

parameters.minThreshold = 0
parameters.maxThreshold = 100

parameters.filterByArea = True
parameters.minArea = 50
parameters.maxArea = 600

parameters.filterByCircularity = True
parameters.minCircularity = 0.2
parameters.maxCircularity = 1

parameters.filterByInertia = True
parameters.minInertiaRatio = 0.2
parameters.maxInertiaRatio = 1

parameters.filterByConvexity = True
parameters.minConvexity = 0.2
parameters.maxConvexity = 1


detector = cv2.SimpleBlobDetector_create(parameters)


def feature_detector(input, average_x, average_y, count):
    input = imutils.resize(input, width=700)
    grayscale = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)

    detected_faces = face_cascade.detectMultiScale(grayscale, scaleFactor=1.3, minNeighbors=6)

    for (x, y, w, h) in detected_faces:
        gray_frame = grayscale[y:y + (h // 2), x:x + w]
        face_rectangle = input[y:y + h, x:x + w]
        detected_eyes = eye_cascade.detectMultiScale(gray_frame, 1.3, 5)

        for (x_1, y_1, w_1, h_1) in detected_eyes:
            eye_frame = face_rectangle[y_1:y_1 + h_1, x_1:x_1 + w_1]
            gray_eye_frame = gray_frame[y_1:y_1 + h_1, x_1:x_1 + w_1]

            blur = cv2.GaussianBlur(gray_eye_frame, (3, 3), 0)

            keypoints = detector.detect(blur)
            cv2.drawKeypoints(eye_frame, keypoints, eye_frame, (0, 255, 255),
                              flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            # commented out for now as this is not effecient and leads to delays
            if keypoints:
                x, y = keypoints[0].pt

                pyautogui.FAILSAFE = False

                if count == 5:
                    if len(average_x) > 0 and len(average_y) > 0:
                        avg_x = 0
                        for av in average_x:
                            avg_x += av
                        avg_x /= len(average_x)
                        avg_y = 0
                        for av in average_y:
                            avg_y += av
                        avg_y /= len(average_y)
                        print(average_x)
                        print(avg_x)
                        print(avg_y)
                        if avg_x > w_1 / 2:
                            print(f"Eyes are facing right {x} {y}")
                            pyautogui.moveRel(-30, 0)
                        elif avg_x < w_1 / 2:
                            print(f"Eyes are facing left {x} {y}")
                            pyautogui.moveRel(30, 0)
                        if avg_y > h_1 / 1.9:
                            print(f"Eyes are facing down {x} {y}")
                            pyautogui.moveRel(0, 30)
                        elif avg_y < h_1 / 1.7:
                            print(f"Eyes are facing up {x} {y}")
                            pyautogui.moveRel(0, -30)
                        average_x.clear()
                        average_y.clear()
                else:
                    average_x.append(x)
                    average_y.append(y)

                # print(f"Eyes are facing right {(x-15)*40} {(y-20)*20}")
                # pyautogui.moveTo((x-15)*100, (y-20)*70)
                # determine the direction by comparing the x, y coordinates of the keypoints
                # if x > w_1 / 2:
                #     print(f"Eyes are facing right {x} {y}")
                #     # print(keypoints)
                #     pyautogui.moveRel(-30, 0)
                #     rel_x = x
                #     # pyautogui.moveTo((x-18)*100+730, y+450)
                # elif x < w_1 / 2:
                #     print(f"Eyes are facing left {x} {y}")
                #     pyautogui.moveRel(30, 0)
                #     # pyautogui.moveTo((x-18)*100+730, y+450)
                # if y > h_1 / 1.9:
                #     print(f"Eyes are facing down {x} {y}")
                #     pyautogui.moveRel(0, 30)
                #     # pyautogui.moveTo((x-18)*100+730, y+450)
                # elif y < h_1 / 1.7:
                #     print(f"Eyes are facing up {x} {y}")
                #     pyautogui.moveRel(0, -30)
                #     # pyautogui.moveTo((x-18)*100+730, y+450)

    cv2.imshow('output', input)
