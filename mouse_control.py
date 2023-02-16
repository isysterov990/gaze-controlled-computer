import pyautogui

def move_mouse(x, y):
    # implement mouse movement
    pyautogui.moveTo(x, y, 1) 
        # commented out for now as this is not effecient and leads to delays
    # if keypoints:
    #     x, y = keypoints[0].pt
    #     pyautogui.FAILSAFE=False
    #     # determine the direction by comparing the x, y coordinates of the keypoints
    #     if x > w_1 / 2:
    #         print("Eyes are facing right")
    #         pyautogui.moveRel(-25, 0)
    #     elif x < w_1 / 2:
    #         print("Eyes are facing left")
    #         pyautogui.moveRel(25, 0)
    #     if y > h_1 / 2:
    #         print("Eyes are facing down")
    #         pyautogui.moveRel(0, 25)
    #     elif y < h_1 / 2:
    #         print("Eyes are facing up")
    #         pyautogui.moveRel(0, -25)
    
