import numpy as np
import cv2
import imutils

parameters = cv2.SimpleBlobDetector_Params()

parameters.filterByColor = False

parameters.minThreshold = 0
parameters.maxThreshold = 100

parameters.filterByArea = True
parameters.minArea = 50
parameters.maxArea = 400

parameters.filterByCircularity = True
parameters.minCircularity = 0.1
parameters.maxCircularity = 1

parameters.filterByInertia = True
parameters.minInertiaRatio = 0.1
parameters.maxInertiaRatio = 1

parameters.filterByConvexity = True
parameters.minConvexity = 0.2
parameters.maxConvexity = 1

detector = cv2.SimpleBlobDetector_create(parameters)

def find_keypoints(eye_frames):
    keypoints = detector.detect(eye_frames)
    return keypoints
    
    
