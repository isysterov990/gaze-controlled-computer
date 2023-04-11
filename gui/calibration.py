from tkinter import Tk, Button, Canvas, PhotoImage

import time
import cv2
import statistics
from detectors.feature_detector import *
from detectors.keypoint_detector import *

def calibrate():
    keypoints = []
    calibration_points = []

    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
    i = 0
    while (i < 4):
        _, input = capture.read()  # used _ to ignore the boolean returned by .read()
        input = cv2.flip(input, 1)
        eye_frames = detect_eyes(input)

        if eye_frames is not None:
            left_keypoint = find_keypoints(eye_frames[0])
            right_keypoint = find_keypoints(eye_frames[1])
            if left_keypoint and right_keypoint:
                avg_x = (left_keypoint[0].pt[0] + right_keypoint[0].pt[0]) / 2
                avg_y = (left_keypoint[0].pt[1] + right_keypoint[0].pt[1]) / 2

                keypoints.append([avg_x, avg_y])
                #print(keypoint[0].pt[0], keypoint[0].pt[1])
                if len(keypoints) == 100:
                    x_values = [kp[0] for kp in keypoints[:100]]
                    y_values = [kp[1] for kp in keypoints[:100]]

                    avg_x = statistics.mean(x_values)
                    avg_y = statistics.mean(y_values)

                    print(f"Average x: {round(avg_x, 2)}")
                    print(f"Average y: {round(avg_y, 2)}\n")

                    calibration_points.append([avg_x, avg_y])

                    del keypoints[:] 
                    i+=1
                    time.sleep(2)

        # k = cv2.waitKey(30) & 0xff
        # if k == 27:
        #     break

    capture.release()
    return calibration_points
