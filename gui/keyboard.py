from tkinter import Tk, Frame, Button, Label
from tkinter.font import Font as font
import pyautogui
import time
from gui.tracker import *

#GLOBAL VARIABLES
gaze_direction = 'middle' #default middle
selected_button_index = 31
selected_button = None

def create_keyboard():
    root = Tk()
    screen_x = root.winfo_screenwidth()
    screen_y = root.winfo_screenheight()
    WINDOW_WIDTH = round(0.8 * screen_x)
    WINDOW_HEIGHT = round(0.37 * screen_y)
    MAIN_COL = '#000000'
    ACCENT_COL = '#2596BE'
    
    #GLOBAL VARIABLES
    global gaze_direction
    global selected_button
    global selected_button_index


    root.title("Accessible Keyboard")
    root.geometry(f"{WINDOW_WIDTH - 145}x{WINDOW_HEIGHT + 10}+250+590")
    root.configure(bg=MAIN_COL)
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.8)
    root.resizable(False, False)

    row1 = ['Esc', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', 'Backspace']
    row2 = ['Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']']
    row3 = ['CapsLock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', 'Enter', '\\']
    row4 = ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '↑', '=']
    row5 = ['Ctrl', 'Win', 'Alt', ' ', 'Alt', 'Fn', '←', '↓', '→']
    rows = [row1, row2, row3, row4, row5]
    allButtons = []

    width50 = [' ']


    def track_direction():
        global gaze_direction
        if (gaze_direction == 'Left'):
            selectFrame_left()
            gaze_direction = 'Middle'
        elif (gaze_direction == 'Right'):
            selectFrame_right()
            gaze_direction = 'Middle'
        elif (gaze_direction == 'Up'):
            selectFrame_up()
            gaze_direction = 'Middle'
        elif (gaze_direction == 'Down'):
            selectFrame_down()
            gaze_direction = 'Middle'
            
    def on_enter(button):
        button.configure(bg=ACCENT_COL, fg='#000')

        if btnLabels[button]:
            btnLabels[button].configure(bg='#ccc', fg='#666')

    def on_leave(button):
        button.configure(bg='#333', fg='#fff')

        if btnLabels[button]:
            btnLabels[button].configure(bg='#333', fg='#fff')

    def selectFrame_right():  # move selected key right
        global selected_button
        global selected_button_index
        if (selected_button_index <= 59):
            on_leave(selected_button)
            selected_button = allButtons[selected_button_index + 1]
            selected_button_index += 1
            on_enter(selected_button)

    def selectFrame_left():  # move selected key left
        global selected_button
        global selected_button_index
        if (selected_button_index >= 1):
            on_leave(selected_button)
            selected_button = allButtons[selected_button_index - 1]
            selected_button_index -= 1
            on_enter(selected_button)

    def selectFrame_up():  # move selected key up
        global selected_button
        global selected_button_index
        if (selected_button_index >= 13):
            on_leave(selected_button)
            if (selected_button_index == 55):  # adjust for spacebar
                selected_button = allButtons[44]
                selected_button_index = 44
            elif (selected_button_index >= 56 and selected_button_index <= 60):  # adjust for spacebar
                selected_button = allButtons[selected_button_index - 9]
                selected_button_index -= 9
            else:
                selected_button = allButtons[selected_button_index - 13]
                selected_button_index -= 13
            on_enter(selected_button)

    def selectFrame_down():  # move selected key down
        global selected_button
        global selected_button_index
        if (selected_button_index <= 51):
            on_leave(selected_button)
            if (selected_button_index >= 43 and selected_button_index <= 46):  # adjust for spacebar
                selected_button = allButtons[55]
                selected_button_index = 55
            elif (selected_button_index >= 47 and selected_button_index <= 51):  # adjust for spacebar
                selected_button = allButtons[selected_button_index + 9]
                selected_button_index += 9
            else:
                selected_button = allButtons[selected_button_index + 13]
                selected_button_index += 13
            on_enter(selected_button)

    def handleClick():
        if btnLabels[selected_button]:
            key = selected_button.cget('text')
            if key == 'Esc':
                prev_win.activate()
                pyautogui.press('esc')
                pyautogui.getWindowsWithTitle('Accessible Keyboard')[0].activate()
            elif key == 'Backspace':
                prev_win.activate()
                pyautogui.press('backspace')
                pyautogui.getWindowsWithTitle('Accessible Keyboard')[0].activate()
            elif key == 'Tab':
                prev_win.activate()
                pyautogui.press('tab')
                pyautogui.getWindowsWithTitle('Accessible Keyboard')[0].activate()
            elif key == 'CapsLock':
                prev_win.activate()
                pyautogui.press('capslock')
                pyautogui.getWindowsWithTitle('Accessible Keyboard')[0].activate()
            elif key == 'Enter':
                prev_win.activate()
                pyautogui.press('enter')
                pyautogui.getWindowsWithTitle('Accessible Keyboard')[0].activate()
            elif key == '←':
                prev_win.activate()
                pyautogui.press('left')
                pyautogui.getWindowsWithTitle('Accessible Keyboard')[0].activate()
            elif key == '→':
                prev_win.activate()
                pyautogui.press('right')
                pyautogui.getWindowsWithTitle('Accessible Keyboard')[0].activate()
            elif key == '↑':
                prev_win.activate()
                pyautogui.press('up')
                pyautogui.getWindowsWithTitle('Accessible Keyboard')[0].activate()
            elif key == '↓':
                prev_win.activate()
                pyautogui.press('down')
                pyautogui.getWindowsWithTitle('Accessible Keyboard')[0].activate()
            elif key == 'Win':
                prev_win.activate()
                pyautogui.press('win')
                pyautogui.getWindowsWithTitle('Accessible Keyboard')[0].activate()
            elif key == 'Shift':
                prev_win.activate()
                pyautogui.press('shift')
                pyautogui.getWindowsWithTitle('Accessible Keyboard')[0].activate()
            elif key == 'Ctrl':
                prev_win.activate()
                pyautogui.press('ctrl')
                pyautogui.getWindowsWithTitle('Accessible Keyboard')[0].activate()
            elif key == 'Alt':
                prev_win.activate()
                pyautogui.press('alt')
                pyautogui.getWindowsWithTitle('Accessible Keyboard')[0].activate()
            elif key == 'Fn':
                prev_win.activate()
                pyautogui.press('fn')
                pyautogui.getWindowsWithTitle('Accessible Keyboard')[0].activate()
            else:
                btnLabels[selected_button].configure(bg=ACCENT_COL, fg='#000')
                prev_win.activate()
                pyautogui.typewrite(key)
                pyautogui.getWindowsWithTitle('Accessible Keyboard')[0].activate()

    btnLabels = {}

    Y = 2.5

    for r in rows:
        X = 5
        for i in r:
            btnWidth = 0.0688 * WINDOW_WIDTH
            btnHeight = 0.2 * WINDOW_HEIGHT

            padx = round(btnWidth / 9)
            pady = round(btnHeight / 10)

            frame = Frame(root, highlightbackground=MAIN_COL, highlightthickness=4)

            anchor = 'c'
            label = Label()

            btn = Button(frame, activebackground=ACCENT_COL, text=i, bg='#333', fg='#fff', relief='flat', padx=padx,
                         pady=pady, borderwidth=0, anchor=anchor, font=font(size=11), takefocus=False)

            if i in width50:
                btnWidth *= 5

            btn.place(x=0, y=0, width=btnWidth, height=btnHeight)
            frame.place(x=X, y=Y, width=btnWidth, height=btnHeight)
            X += btnWidth

            btnLabels[btn] = label
            allButtons.append(btn)
        Y += btnHeight

    selected_button = allButtons[selected_button_index]
    on_enter(selected_button)

    while True:
        root.update_idletasks()
        temp_win = pyautogui.getActiveWindow()
        if (temp_win != None):
            if (temp_win.title != "Accessible Keyboard"):
                prev_win = temp_win
        print("GETTING GAZE\n\n\n")
        gaze_direction = get_direction()
        print(gaze_direction)
        print("\n\n\nGETTING GAZE\n\n\n")
        track_direction()
        time.sleep(0.1)
        root.update()


def main():
    create_keyboard()


if __name__ == '__main__':
    main()