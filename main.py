import webbrowser
from tkinter import Toplevel
import tkinter as tk

import subprocess
import os

from detectors.feature_detector import *
from detectors.blink_detector import *
from detectors.keypoint_detector import *
from mouse_control import *
import pyautogui
import threading

capture = cv2.VideoCapture(0)

screen_x, screen_y = pyautogui.size()


# def create_gui():
# sg.window
# sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()


# top.geometry("1920x1080")
# top.title("toplevel")
# btn = tk.Button(top, text="test")


# def increase():
#     value = int(lbl_value["text"])
#     lbl_value["text"] = f"{value + 1}"


def open_browser():
    webbrowser.open("https://www.google.ca/?client=safari")
    # value = int(lbl_value["text"])
    # lbl_value["text"] = f"{value - 1}"


def open_file():
    path = "/Users/chris/Documents/"
    if os.path.exists(path):
        subprocess.call(["open", path])


# def gui():
window = tk.Tk()
# window = tk.Toplevel()
window.geometry("1230x720")
btn_browser = tk.Button(master=window, width=50,
                        height=25, text="Web Browser", command=open_browser)
btn_browser.grid(row=0, column=0, sticky="nsew")
btn_file = tk.Button(master=window, width=50,
                     height=25, text="File Browser", command=open_file)
btn_file.grid(row=0, column=1, sticky="nsew")

# window.mainloop()

# lbl_value = tk.Label(master=window, text="0")
# lbl_value.grid(row=0, column=1)
#
# btn_increase = tk.Button(master=window, text="+", command=increase)
# btn_increase.grid(row=0, column=2, sticky="nsew")

# window.mainloop()

# def handle_click(event):
#     print("The button was clicked!")
#
#
# button = tk.Button(
#     top,
#     text="Click me!",
#     width=25,
#     height=5,
#     bg="blue",
#     fg="yellow",
# )
#
# button.bind("<Button-1>", handle_click)
#
# top.mainloop()

# layout = [
#     [psg.Text('Select a file', font=('Arial Bold', 20), expand_x=True, justification='center')],
#     [psg.Input(enable_events=True, key='-IN-', font=('Arial Bold', 12), expand_x=True), psg.FileBrowse()]
# ]
# window = psg.Window('FileChooser Demo', layout,
#                     size=(715, 100))
# while True:
#     event, values = window.read()
#     if event == psg.WIN_CLOSED or event == 'Exit':
#         break
# window.close()


# create_gui()

# def run():
blink_count = 0

average_x = []
average_y = []
count = 0

# thread = threading.Thread(target=gui)
# thread.start()


while 1:
    window.update()
    _, input = capture.read()  # used _ to ignore the boolean returned by .read()
    input = cv2.flip(input, 1)
    blink_count_new = blink_count
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
        blink_count += ear_detector(input)
        keypoints = find_keypoints(eye_frames)
        if keypoints:
            x = keypoints[0].pt[0]
            y = keypoints[0].pt[1]
            if count == 20:
                move_mouse(average_x, average_y)
                # print('keypoint: ', keypoints[0].pt[0], keypoints[0].pt[1])

                # print('keypoint: ', x, y)
                # pyautogui.moveTo(x, y, 1)

            else:
                average_x.append(x)
                average_y.append(y)

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

# y = threading.Thread(target=run())
# x = threading.Thread(target=create_gui())
# x.start()
# y.start()

# top = Toplevel()
# top.geometry("1920x1080")
# top.title("toplevel")
# btn = tk.Button(top, text="test")
#
# wd = tk.Tk()
#
# print("opened window")
# # create_gui()
# print("Blocked")

#
# y.join()
# x.join()
