from gui.gui import *
from gui.main_menu_GUI import *
import pyautogui

calibration_points = []
screen_x, screen_y = pyautogui.size()

overlay = create_gui(screen_x, screen_y)
overlay.mainloop()
# open_main_menu()





