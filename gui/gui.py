import subprocess
import os
import sys
import time
import webbrowser
import tkinter as tk

import pyautogui


# from gui.keyboard import create_keyboard


def open_browser():
    webbrowser.open("https://www.google.com")


def open_email():
    webbrowser.open("https://mail.google.com/mail/u/0/?tab=wm#inbox?compose=new")


def open_file():
    try:
        subprocess.Popen("explorer")
        return
    except OSError:
        pass


def open_keyboard():
    try:
        cmd_path = "C:\\WINDOWS\\system32\\osk.exe"
        subprocess.Popen([cmd_path], shell=True)

        return
    except OSError:
        pass


def show_desktop():
    pyautogui.hotkey("win", "d")


def change_button(btn, choice):
    if choice == "Browser":
        btn.config(text="Open Browser", command=open_browser)
    elif choice == "Files":
        btn.config(text="Open File Explorer", command=open_file)


def get_quadrant(x_coord, y_coord, x, y):
    x1, y1 = 0, 0
    x2, y2 = x, y
    x3, y3 = 0, y
    x4, y4 = x, 0

    slope2 = (y2 - y1) / (x2 - x1)
    slope1 = (y4 - y3) / (x4 - x3)

    intercept1 = y  # y1 - (slope1 * x1)
    intercept2 = 0  # y3 - (slope2 * x3)

    x_intersection = x / 2

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


class Gui:
    def __init__(self, x, y):
        print(x, y)
        self.overlay = tk.Tk()
        self.overlay.overrideredirect(True)
        self.overlay.wm_attributes("-topmost", True)
        self.overlay.attributes("-alpha", 0.8)
        self.overlay.geometry("{}x{}+0+0".format(x, y))
        self.x = x
        self.y = y

        canvas = tk.Canvas(
            self.overlay,
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

        canvas.bind("<Button-1>", self.click_handler)
        canvas.place(relx=0.5, rely=0.5, anchor='center')

        north_label = tk.Label(self.overlay, text="Open Browser", font=("Arial", 20))
        south_label = tk.Label(self.overlay, text="Open Email", font=("Arial", 20))
        east_label = tk.Label(self.overlay, text="Open File Explorer", font=("Arial", 20))
        west_label = tk.Label(self.overlay, text="Open On Screen Keyboard", font=("Arial", 20))

        north_label.place(x=x / 2, y=y / 4, anchor="center")
        south_label.place(x=x / 2, y=y * 3 / 4, anchor="center")
        east_label.place(x=x * 3 / 4, y=y / 2, anchor="center")
        west_label.place(x=x / 4, y=y / 2, anchor="center")

        self.overlay.mainloop()

    def click_handler(self, event):
        if get_quadrant(event.x, event.y, self.x, self.y) == 1:
            open_browser()
            self.overlay.destroy()
        elif get_quadrant(event.x, event.y, self.x, self.y) == 6:
            open_browser()
            self.overlay.destroy()
        elif get_quadrant(event.x, event.y, self.x, self.y) == 5:
            open_file()
            self.overlay.destroy()
        elif get_quadrant(event.x, event.y, self.x, self.y) == 3:
            open_email()
            self.overlay.destroy()
        elif get_quadrant(event.x, event.y, self.x, self.y) == 4:
            open_email()
            self.overlay.destroy()
        elif get_quadrant(event.x, event.y, self.x, self.y) == 2:
            open_keyboard()
            self.overlay.destroy()

        print("Clicked at ({}, {})".format(event.x, event.y))
