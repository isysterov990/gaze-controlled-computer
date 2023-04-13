import subprocess
import os
import webbrowser
import tkinter as tk
from gui.keyboard import create_keyboard


def open_browser():
    webbrowser.open("https://www.google.ca/?client=safari")
    # value = int(lbl_value["text"])
    # lbl_value["text"] = f"{value - 1}"


def open_email():
    webbrowser.open("https://www.google.com/gmail/about/")


def open_file():
    path = "/Users/chris/Documents/"
    if os.path.exists(path):
        subprocess.call(["open", path])


def open_keyboard():
    create_keyboard()


def change_button(btn, choice):
    if choice == "Browser":
        btn.config(text="Open Browser", command=open_browser)
    elif choice == "Files":
        btn.config(text="Open File Explorer", command=open_file)


def get_quadrant(x_coord, y_coord):
    x1, y1 = 0, 0
    x2, y2 = 1470, 956
    x3, y3 = 0, 956
    x4, y4 = 1470, 0

    slope2 = (y2 - y1) / (x2 - x1)
    slope1 = (y4 - y3) / (x4 - x3)

    intercept1 = 956  # y1 - (slope1 * x1)
    intercept2 = 0  # y3 - (slope2 * x3)

    x_intersection = 1470 / 2

    if x_coord <= x_intersection and y_coord < (slope1 * x_coord + intercept1) and y_coord < (
            slope2 * x_coord + intercept2):
        return 1
    elif x_coord <= x_intersection and (slope1 * x_coord + intercept1) > y_coord > (
            slope2 * x_coord + intercept2):
        return 2
    elif x_coord <= x_intersection and y_coord > (slope1 * x_coord + intercept1) and y_coord > (
            slope2 * x_coord + intercept2):
        return 3
    elif x_coord > x_intersection and y_coord > (slope2 * x_coord + intercept2) and y_coord > (
            slope1 * x_coord + intercept1):
        return 4
    elif x_coord > x_intersection and (slope2 * x_coord + intercept2) > y_coord > (
            slope1 * x_coord + intercept1):
        return 5
    elif x_coord > x_intersection and y_coord < (slope2 * x_coord + intercept2) and y_coord < (
            slope1 * x_coord + intercept1):
        return 6


def click_handler(event):
    if get_quadrant(event.x, event.y) == 1:
        open_browser()
    elif get_quadrant(event.x, event.y) == 6:
        open_browser()
    elif get_quadrant(event.x, event.y) == 5:
        open_file()
    elif get_quadrant(event.x, event.y) == 3:
        open_email()
    elif get_quadrant(event.x, event.y) == 4:
        open_email()
    elif get_quadrant(event.x, event.y) == 2:
        open_keyboard()

    print("Clicked at ({}, {})".format(event.x, event.y))


def create_gui(x, y):
    print(x, y)
    overlay = tk.Toplevel()
    overlay.overrideredirect(True)
    overlay.wm_attributes("-topmost", True)
    overlay.attributes("-alpha", 0.8)
    overlay.geometry("{}x{}+0+0".format(x, y))

    canvas = tk.Canvas(
        overlay,
        # bg="white",
        height=y,
        width=x,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.pack()

    line1 = canvas.create_line(0, 0, x, y, fill="black")
    line2 = canvas.create_line(0, y, x, 0, fill="black")

    canvas.bind("<Button-1>", click_handler)
    canvas.place(relx=0.5, rely=0.5, anchor='center')

    north_label = tk.Label(overlay, text="Open Browser", font=("Arial", 20))
    south_label = tk.Label(overlay, text="Open Email", font=("Arial", 20))
    east_label = tk.Label(overlay, text="Open File Explorer", font=("Arial", 20))
    west_label = tk.Label(overlay, text="Open Keyboard", font=("Arial", 20))

    north_label.place(x=x / 2, y=y / 4, anchor="center")
    south_label.place(x=x / 2, y=y * 3 / 4, anchor="center")
    east_label.place(x=x * 3 / 4, y=y / 2, anchor="center")
    west_label.place(x=x / 4, y=y / 2, anchor="center")

    return overlay
