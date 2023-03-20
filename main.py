import webbrowser
from tkinter import Toplevel
import tkinter as tk
import subprocess
import os
import time
from detectors.feature_detector import *
from detectors.blink_detector import *
from detectors.keypoint_detector import *
from mouse_control import *
import pyautogui
import threading

capture = cv2.VideoCapture(0)
screen_x, screen_y = pyautogui.size()
pyautogui.FAILSAFE = False



#CALIBRATION PROCESS
start_time = time.time()
keypoints = []
x_min = 10000
x_max = 0
y_min = 10000
y_max = 0

while ((time.time() - start_time) < 15):
    _, input = capture.read()  # used _ to ignore the boolean returned by .read()
    input = cv2.flip(input, 1)
    eye_frames = detect_eyes(input)

    if eye_frames is not None:
        left_keypoint = find_keypoints(eye_frames[0])
        right_keypoint = find_keypoints(eye_frames[1])
        print(left_keypoint, right_keypoint)
        if left_keypoint and right_keypoint:
            avg_x = (left_keypoint[0].pt[0] + right_keypoint[0].pt[0]) / 2
            avg_y = (left_keypoint[0].pt[1] + right_keypoint[0].pt[1]) / 2

            print(avg_x, avg_y)
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
                    
print(x_min, x_max, y_min, y_max)



def open_browser():
    webbrowser.open("https://www.google.ca/?client=safari")


def open_file():
    path = "/Users/chris/Documents/"
    if os.path.exists(path):
        subprocess.call(["open", path])


window = tk.Tk()

window.geometry("1230x720")
btn_browser = tk.Button(master=window, width=50,
                        height=25, text="Web Browser", command=open_browser)
btn_browser.grid(row=0, column=0, sticky="nsew")
btn_file = tk.Button(master=window, width=50,
                     height=25, text="File Browser", command=open_file)
btn_file.grid(row=0, column=1, sticky="nsew")


blink_count = 0

average_x = []
average_y = []
count = 0


#MAIN LOOP
while (1):
    window.update()
    _, input = capture.read()  # used _ to ignore the boolean returned by .read()
    input = cv2.flip(input, 1)
    blink_count_new = blink_count
    eye_frames = detect_eyes(input)

    if eye_frames is not None:
        blink_count += ear_detector(input)
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

                del keypoints[:] 

                x = avg_keypoint[0]
                y = avg_keypoint[1]

                #standardizing x and y coordinates to the size of the screen
                x_move = (x - x_min) * (screen_x / (x_max - x_min))
                y_move = (y - y_min) * (screen_y / (y_max - y_min))

                print('moving to: ', x_move, y)
                if x_move < 0:
                    x_move = 0
                elif x_move > screen_x:
                    x_move = screen_x
                if y_move < 0:
                    y_move = 0
                elif y_move > screen_y:
                    y_move = screen_y

                pyautogui.moveTo(x_move, y_move, 0.5)

    # print('count: ', count)
    if count > 20:
        count = 0
    else:
        count += 1

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

capture.release()
cv2.destroyAllWindows()