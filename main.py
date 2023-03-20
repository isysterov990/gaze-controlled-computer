from detectors.feature_detector import *
from detectors.blink_detector import *
from detectors.keypoint_detector import *
from mouse_control import *
import pyautogui
import time

pyautogui.FAILSAFE = False
start_time = time.time()
capture = cv2.VideoCapture(0)
blink_count = 0

average_x = []
average_y = []
count = 0

x_min = 10000
x_max = 0
y_min = 10000
y_max = 0

keypoints = []
i = 0
current_position = []

#calibration
while ((time.time() - start_time) < 15):
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

            if len(keypoints) == 2:
                avg_keypoint = 2 * [0]  # avgs per column
                nelem = float(2)
                for col in range(2):
                    for row in range(2):
                        avg_keypoint[col] += keypoints[row][col]
                    avg_keypoint[col] /= nelem
                print('avg: ', avg_keypoint)

                del keypoints[:]

                x = avg_keypoint[0]
                y = avg_keypoint[1]

                if x < x_min:
                    x_min = x
                elif x > x_max:
                    x_max = x
                if y < y_min:
                    y_min = y
                elif y > y_max:
                    y_max = y

# center_point = 2*[0] # avgs per column
# nelem = float(10)
# for col in range(2):
#     for row in range(10):
#         center_point[col] += initial_keypoints[row][col]
#     center_point[col] /= nelem
# print('center_point: ', center_point)
#
# current_position = center_point
# pyautogui.moveTo(960, 540)
# current_mouse_position = [pyautogui.position()[0]][pyautogui.position()[1]]
print(x_min, x_max, y_min, y_max)
while (1):
    _, input = capture.read()  # used _ to ignore the boolean returned by .read()
    input = cv2.flip(input, 1)

    # grayscale = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
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
        left_keypoint = find_keypoints(eye_frames[0])
        right_keypoint = find_keypoints(eye_frames[1])
        if left_keypoint and right_keypoint:
            avg_x = (left_keypoint[0].pt[0] + right_keypoint[0].pt[0]) / 2
            avg_y = (left_keypoint[0].pt[1] + right_keypoint[0].pt[1]) / 2

            keypoints.append([avg_x, avg_y])
            if len(keypoints) == 8:
                avg_keypoint = 2*[0] # avgs per column
                nelem = float(8)
                for col in range(2):
                    for row in range(8):
                        avg_keypoint[col] += keypoints[row][col]
                    avg_keypoint[col] /= nelem
                print('avg: ', avg_keypoint)

                #current_keypoint = avg_keypoint

                del keypoints[:] 

                x = avg_keypoint[0]
                y = avg_keypoint[1]
                # if count == 20:
                # move_mouse(average_x, average_y)

                #standardizing x and y coordinates to the size of the screen
                x_move = (x - x_min) * (2560 / (x_max - x_min))
                y_move = (y - y_min) * (1440 / (y_max - y_min))

                print('moving to: ', x_move, y)
                if x_move < 0:
                    x_move = 0
                elif x_move > 2560:
                    x_move = 2560
                if y_move < 0:
                    y_move = 0
                elif y_move > 1440:
                    y_move = 1440

                pyautogui.moveTo(x_move, y_move, 0.5)

    #         else:
    #             average_x.append(x)
    #             average_y.append(y)

    # print('count: ', count)
    # if count > 20:
    #     count = 0
    # else:
    #     count += 1

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

capture.release()
cv2.destroyAllWindows()
