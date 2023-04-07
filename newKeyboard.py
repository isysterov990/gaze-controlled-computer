from tkinter import Tk, Frame, Button, Label
from tkinter.font import Font as font
import pyautogui
import time

root = Tk()
screen_x = root.winfo_screenwidth()
screen_y = root.winfo_screenheight()
WINDOW_WIDTH = round(screen_x*0.6)
WINDOW_HEIGHT = round(screen_y*0.3)
print(WINDOW_HEIGHT)
MAIN_COL = '#000000'
ACCENT_COL = '#DE5F2C'

root.title("Accessible Keyboard")
root.geometry(f"{WINDOW_WIDTH+10}x{WINDOW_HEIGHT+10}")
root.configure(bg=MAIN_COL)
root.attributes('-topmost', True)
root.attributes('-alpha', 0.8)
root.resizable(False, False)

row1 = ['Esc', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace']
row2 = ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\']
row3 = ['CapsLock', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', 'Enter']
row4 = ['Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Up']
row5 = ['Ctrl', 'Win', 'Alt', ' ', 'Alt', 'Fn', 'Left', 'Down', 'Right']
rows = [row1, row2, row3, row4, row5]

specials = ['Ctrl', 'Alt', 'Shift', 'Win']
nonLetters = specials + ['Esc', 'Tab', 'Del', 'Backspace', 'CapsLock', 'Enter', 'Up', 'Left', 'Down', 'Right']
allButtons = []

width50 = [' ']

def on_enter(e):
    e.widget.configure(bg='#ccc', fg='#000')

    if btnLabels[e.widget]:
        btnLabels[e.widget].configure(bg='#ccc', fg='#666')

def on_leave(e):
    e.widget.configure(bg='#333', fg='#fff')

    if btnLabels[e.widget]:
        btnLabels[e.widget].configure(bg='#333', fg='#fff')

def handleClick(e):
    print(e.widget)
    if btnLabels[e.widget]:
        btnLabels[e.widget].configure(bg=ACCENT_COL, fg='#000')
        key = e.widget.cget('text')
        prev_win.activate()
        pyautogui.typewrite(key)

btnLabels = {}

Y = 2.5

for r in rows:
    X = 5
    for i in r:
        btnWidth = 0.0688*WINDOW_WIDTH
        btnHeight = 0.2*WINDOW_HEIGHT

        padx = round(btnWidth/9)
        pady = round(btnHeight/10)

        frame = Frame(root, highlightbackground=MAIN_COL, highlightthickness=4)

        anchor = 'c'
        label = Label()

        btn = Button(frame, activebackground=ACCENT_COL, text=i, bg='#333', fg='#fff', relief='flat', padx=padx, pady=pady, borderwidth=0, anchor=anchor, font=font(size=12), takefocus=False)

        if i in width50:
            btnWidth *= 5
        
        btn.place(x=0, y=0, width=btnWidth, height=btnHeight)
        frame.place(x=X, y=Y, width=btnWidth, height=btnHeight)
        X += btnWidth

        btn.bind('<Button-1>', handleClick)
        btn.bind('<ButtonRelease-1>', on_enter)
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)

        btnLabels[btn] = label
        allButtons.append(btn)
    Y += btnHeight

while True:
    root.update_idletasks()
    temp_win = pyautogui.getActiveWindow()
    if(temp_win != None):
        if(temp_win.title != "Accessible Keyboard"):
            prev_win = temp_win
            print('in if: ' + str(prev_win))
    time.sleep(0.0001)
    root.update()