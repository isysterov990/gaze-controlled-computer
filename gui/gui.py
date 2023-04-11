import subprocess
import os
import webbrowser
import tkinter as tk


def open_browser():
    webbrowser.open("https://www.google.ca/?client=safari")
    # value = int(lbl_value["text"])
    # lbl_value["text"] = f"{value - 1}"


def open_file():
    path = "/Users/chris/Documents/"
    if os.path.exists(path):
        subprocess.call(["open", path])


def change_button(btn, choice):
    if choice == "Browser":
        btn.config(text="Open Browser", command=open_browser)
    elif choice == "Files":
        btn.config(text="Open File Explorer", command=open_file)


# def create_gui(x, y):
#     # window = tk.Tk()
#     # This will always make window on top
#     overlay = tk.Toplevel()
#     overlay.overrideredirect(True)
#     overlay.wm_attributes("-topmost", True)
#     overlay.attributes("-alpha", 0.8)
#     overlay.geometry("{}x{}+0+0".format(x, y))
#
#     btn_north = tk.Button(master=overlay, width=50,
#                           height=25, text="Open Browser", command=open_browser, bg='white')
#     btn_north.configure(highlightthickness=0, highlightbackground=btn_north['bg'])
#     btn_north.place(relx=0.5, rely=0.2, anchor='center')
#
#     btn_south = tk.Button(master=overlay, width=50,
#                           height=25, text="South", command=open_file)
#     btn_south.place(relx=0.5, rely=0.8, anchor='center')
#
#     btn_east = tk.Button(master=overlay, width=50,
#                          height=25, text="Open File Explorer", command=open_file)
#     btn_east.place(relx=0.8, rely=0.5, anchor='center')
#
#     btn_west = tk.Button(master=overlay, width=50,
#                          height=25, text="West", command=open_file)
#     # btn_west.config(bg="white", activebackground="white", alpha=1)
#     btn_west.place(relx=0.2, rely=0.5, anchor='center')
#
#     # btn_change = tk.Button(master=overlay, width=25,
#     #                        height=25, text="change", command=lambda: change_button(btn_north, "files"), bg='white')
#     # btn_change.configure(highlightthickness=0, highlightbackground=btn_north['bg'])
#     # btn_change.place(relx=0.5, rely=0.5, anchor='center')
#
#     options = ["Browser", "Files"]
#
#     selected_option = tk.StringVar()
#     selected_option.set("Select")
#
#     btn_change = tk.OptionMenu(overlay, selected_option, *options,
#                                command=lambda choice: change_button(btn_north, choice))
#     btn_change.configure(highlightthickness=0, highlightbackground=btn_north['bg'])
#     btn_change.place(relx=0.5, rely=0.5, anchor='center')
#
#     return overlay

def get_quadrant(x_coord, y_coord):
    x1, y1 = 0, 0
    x2, y2 = 1470, 956
    x3, y3 = 0, 956
    x4, y4 = 1470, 0

    slope2 = (y2 - y1) / (x2 - x1)
    slope1 = (y4 - y3) / (x4 - x3)

    intercept1 = 956  # y1 - (slope1 * x1)
    intercept2 = 0  # y3 - (slope2 * x3)

    x_intersection = 1470/2

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
        print("South")
    elif get_quadrant(event.x, event.y) == 4:
        print("South")
    elif get_quadrant(event.x, event.y) == 2:
        print("West")

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
    south_label = tk.Label(overlay, text="Open File Explorer", font=("Arial", 20))
    east_label = tk.Label(overlay, text="East", font=("Arial", 20))
    west_label = tk.Label(overlay, text="West", font=("Arial", 20))

    north_label.place(x=x / 2, y=y / 4, anchor="center")
    south_label.place(x=x / 2, y=y * 3 / 4, anchor="center")
    east_label.place(x=x * 3 / 4, y=y / 2, anchor="center")
    west_label.place(x=x / 4, y=y / 2, anchor="center")

    return overlay
