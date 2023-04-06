import pyautogui

current_x, current_y = pyautogui.position()

kp1_x_min = 100000
kp1_y_min = 100000
kp1_x_max = 0
kp1_y_max = 0
screen_x, screen_y = pyautogui.size()


# screen_x = 1920
# screen_y = 1080

def click_mouse():
    pyautogui.click()


def move_mouse(average_x, average_y):
    pyautogui.FAILSAFE = False
    global kp1_x_min
    global kp1_y_min
    global kp1_x_max
    global kp1_y_max

    if len(average_x) > 0 and len(average_y) > 0:

        avg_x = 0
        for av in average_x:
            avg_x += av
        avg_x /= len(average_x)
        avg_y = 0
        for av in average_y:
            avg_y += av
        avg_y /= len(average_y)
        # print('avg_x: ', avg_x)
        # print('avg_y: ', avg_y)

        # Updating min/max boundaries
        if avg_x < kp1_x_min:
            kp1_x_min = avg_x
        elif avg_x > kp1_x_max:
            kp1_x_max = avg_x

        if avg_y < kp1_y_min:
            kp1_y_min = avg_y
        elif avg_y > kp1_y_max:
            kp1_y_max = avg_y

        # print('x_min: ', kp1_x_min)
        # print('x_max: ', kp1_x_max)
        # print('y_min: ', kp1_y_min)
        # print('y_max: ', kp1_y_max)

        scaled_x = (((avg_x - kp1_x_min) / (kp1_x_max - kp1_x_min)) * screen_x)
        scaled_y = (((avg_y - kp1_y_min) / (kp1_y_max - kp1_y_min)) * screen_y)

        # print('scaled_x: ', scaled_x)
        # print('scaled_y: ', scaled_y)
        pyautogui.moveTo(scaled_x, scaled_y, 0.5)
        # if avg_x > w_1 / 2:
        #     print(f"Eyes are facing right {x} {y}")
        #     pyautogui.moveRel(-30, 0)
        # elif avg_x < w_1 / 2:
        #     print(f"Eyes are facing left {x} {y}")
        #     pyautogui.moveRel(30, 0)
        # if avg_y > h_1 / 1.9:
        #     print(f"Eyes are facing down {x} {y}")
        #     pyautogui.moveRel(0, 30)
        # elif avg_y < h_1 / 1.7:
        #     print(f"Eyes are facing up {x} {y}")
        #     pyautogui.moveRel(0, -30)
        average_x.clear()
        average_y.clear()
