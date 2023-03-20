import numpy as np
import cv2
import imutils
from typing import Optional

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

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


def feature_detector(input):
    input = imutils.resize(input, width=700)
    grayscale = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)

    detected_faces = face_cascade.detectMultiScale(grayscale, scaleFactor=1.3, minNeighbors=6) 

    for (x, y, w, h) in detected_faces:
        #cv2.rectangle(input, (x, y), (x + w, y + (h//2)), (255, 0 , 0), 2) #divide height by 2 to restrict area to upper half of the face where the eyes are
        gray_frame = grayscale[y:y+(h//2), x:x+w]
        face_rectangle = input[y:y+h, x:x+w]

        detected_eyes = eye_cascade.detectMultiScale(gray_frame, 1.3, 5)

        for(x_1, y_1, w_1, h_1) in detected_eyes:
            #cv2.rectangle(face_rectangle, (x_1, y_1), (x_1 + w_1, y_1 + h_1), (0, 0, 255), 2)

            eye_frame = face_rectangle[y_1:y_1+h_1, x_1:x_1+w_1]
            gray_eye_frame = gray_frame[y_1:y_1+h_1, x_1:x_1+w_1]

            blur = cv2.GaussianBlur(gray_eye_frame, (3, 3), 0)
            #, eye_threshold = cv2.threshold(blur, 130, 255, cv2.THRESH_BINARY)

            
            keypoints = detector.detect(blur)
            cv2.drawKeypoints(eye_frame, keypoints, eye_frame, (0, 255, 255), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
           #cv2.imshow('blobs', blobs)
              
    cv2.imshow('output', input)
