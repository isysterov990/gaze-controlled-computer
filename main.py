import numpy as np
import cv2
import blink_detector
from face_detector import *

capture = cv2.VideoCapture(0)
blink_count=0
while(1):
    _, input = capture.read() #used _ to ignore the boolean returned by .read()
    blink_count += blink_detector.ear_detector(input)
    print("blink_count", blink_count)
    eye_frame = feature_detector(input)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

capture.release()
cv2.destroyAllWindows()