from detectors.feature_detector import *
from detectors.blink_detector import *
from detectors.keypoint_detector import *
from mouse_control import *

capture = cv2.VideoCapture(0)
blink_count=0
while(1):
    _, input = capture.read() #used _ to ignore the boolean returned by .read()
    #grayscale = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
    # rects = detector(grayscale, 0)
    # if len(rects) > 0:
    #     rect = rects[0]
    # else:
    #     cv2.imshow("Frame", input)
    #     k = cv2.waitKey(30) & 0xFF
    #     continue
    # blink_count += ear_detector(input,grayscale,rect)
    # print("blink_count", blink_count)
    eye_frames = detect_eyes(input)
    
    if eye_frames is not None:
        keypoints = find_keypoints(eye_frames)
        if keypoints:
            print('keypoint: ', keypoints[0].pt[0], keypoints[0].pt[1])

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

capture.release()
cv2.destroyAllWindows()