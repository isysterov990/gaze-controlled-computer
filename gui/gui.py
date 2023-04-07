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


def create_gui(x, y):
    # window = tk.Tk()
    # This will always make window on top
    overlay = tk.Toplevel()
    overlay.overrideredirect(True)
    overlay.wm_attributes("-topmost", True)
    overlay.attributes("-alpha", 0.8)
    overlay.geometry("{}x{}+0+0".format(x, y))

    btn_north = tk.Button(master=overlay, width=50,
                          height=25, text="Open Browser", command=open_browser, bg='white')
    btn_north.configure(highlightthickness=0, highlightbackground=btn_north['bg'])
    btn_north.place(relx=0.5, rely=0.2, anchor='center')

    btn_south = tk.Button(master=overlay, width=50,
                          height=25, text="South", command=open_file)
    btn_south.place(relx=0.5, rely=0.8, anchor='center')

    btn_east = tk.Button(master=overlay, width=50,
                         height=25, text="Open File Explorer", command=open_file)
    btn_east.place(relx=0.8, rely=0.5, anchor='center')

    btn_west = tk.Button(master=overlay, width=50,
                         height=25, text="West", command=open_file)
    # btn_west.config(bg="white", activebackground="white", alpha=1)
    btn_west.place(relx=0.2, rely=0.5, anchor='center')

    # btn_change = tk.Button(master=overlay, width=25,
    #                        height=25, text="change", command=lambda: change_button(btn_north, "files"), bg='white')
    # btn_change.configure(highlightthickness=0, highlightbackground=btn_north['bg'])
    # btn_change.place(relx=0.5, rely=0.5, anchor='center')

    options = ["Browser", "Files"]

    selected_option = tk.StringVar()
    selected_option.set("Select")

    btn_change = tk.OptionMenu(overlay, selected_option, *options,
                               command=lambda choice: change_button(btn_north, choice))
    btn_change.configure(highlightthickness=0, highlightbackground=btn_north['bg'])
    btn_change.place(relx=0.5, rely=0.5, anchor='center')

    return overlay
