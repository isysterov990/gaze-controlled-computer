from detectors.face_detector import *
from detectors.blink_detector import *

capture = cv2.VideoCapture(0)
blink_count = 0

average_x = []
average_y = []
count = 0

pyautogui.FAILSAFE = False
screenWidth, screenHeight = pyautogui.size()
print(screenWidth, screenHeight)
pyautogui.moveTo(screenWidth/2, screenHeight/2)

while 1:
    _, input = capture.read()  # used _ to ignore the boolean returned by .read()
    grayscale = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
    rects = detector(grayscale, 0)
    if len(rects) > 0:
        rect = rects[0]
    else:
        cv2.imshow("Frame", input)
        k = cv2.waitKey(30) & 0xFF
        continue
    blink_count += ear_detector(input, grayscale, rect)
    print("blink_count", blink_count)

    eye_frame = feature_detector(input, average_x, average_y, count)
    print(average_x)
    print(count)
    if count > 5:
        count = 0
    else:
        count += 1

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

capture.release()
cv2.destroyAllWindows()
