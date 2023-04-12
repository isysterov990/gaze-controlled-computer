import time

import cv2
import dlib
import numpy as np
import pyautogui
from imutils import face_utils

from gui.calibration import adjust_eye_tracking

pyautogui.FAILSAFE = False
screen_width, screen_height = pyautogui.size()

left_eye_roi = [(36, 37, 38, 39, 40, 41)]
right_eye_roi = [(42, 43, 44, 45, 46, 47)]
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def mouth_aspect_ratio(mouth):
    A = np.linalg.norm(mouth[2] - mouth[10])
    B = np.linalg.norm(mouth[4] - mouth[8])
    C = np.linalg.norm(mouth[0] - mouth[6])
    mar = (A + B ) / (2.0 * C)
    return mar

def track_eyes(calibration_points):
    EYE_AR_THRESH = 0.3
    MOUTH_AR_THRESH = 0.8
    EYE_AR_CONSEC_FRAMES = 3
    MOUTH_AR_CONSEC_FRAMES = 5
    COUNTER_EYE = 0
    COUNTER_MOUTH = 0
    KEEP_TRACKING = True
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("./models/shape_predictor_68_face_landmarks.dat")
    left_eye_offset, right_eye_offset = adjust_eye_tracking(calibration_points)
    while True:

        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)
            left_eye_landmarks = [landmarks.part(i) for i in left_eye_roi[0]]
            right_eye_landmarks = [landmarks.part(i) for i in right_eye_roi[0]]
            # Calculate the center of the left and right eyes
            left_eye_center = np.mean([np.array([p.x, p.y]) for p in left_eye_landmarks], axis=0)
            right_eye_center = np.mean([np.array([p.x, p.y]) for p in right_eye_landmarks], axis=0)
            left_eye_position = left_eye_center + left_eye_offset
            right_eye_position = right_eye_center + right_eye_offset
            gaze_position = ((left_eye_position[0] + right_eye_position[0]) // 2,
                             (left_eye_position[1] + right_eye_position[1]) // 2)
            gaze_position = (int(gaze_position[0]), int(gaze_position[1]))



            mouse_speed = 50
            movement_range = 10000
            landmarks = face_utils.shape_to_np(landmarks)

            if KEEP_TRACKING:
                # Move the mouse based on the eye tracking
                mouse_x = int(gaze_position[0] / 640 * screen_width)
                mouse_y = int(gaze_position[1] / 480 * screen_height)
                mouse_x_offset = (mouse_x - screen_width / 2) / (screen_width / 2) * movement_range
                mouse_y_offset = (mouse_y - screen_height / 2) / (screen_height / 2) * movement_range
                if left_eye_center[0] < right_eye_center[0]:
                    mouse_x_offset *= -1
                pyautogui.moveTo(screen_width / 2 + mouse_x_offset, screen_height / 2 + mouse_y_offset,
                                 duration=mouse_speed / 1000)

                # Eye Detection
                left_eye = landmarks[lStart:lEnd]
                right_eye = landmarks[rStart:rEnd]
                left_ear = eye_aspect_ratio(left_eye)
                right_ear = eye_aspect_ratio(right_eye)
                # Compute the average eye aspect ratio
                ear = (left_ear + right_ear) / 2.0
                if ear < EYE_AR_THRESH:
                    COUNTER_EYE += 1
                else:
                    if COUNTER_EYE >= EYE_AR_CONSEC_FRAMES:
                        pyautogui.click()
                    COUNTER_EYE = 0

            # Mouth Detection
            mouth = landmarks[mStart:mEnd]
            mar = mouth_aspect_ratio(mouth)
            if mar > MOUTH_AR_THRESH:
                COUNTER_MOUTH +=1
            else:
                if COUNTER_MOUTH >= MOUTH_AR_CONSEC_FRAMES:
                    if KEEP_TRACKING:
                        KEEP_TRACKING = False
                        time.sleep(2)
                    else:
                        KEEP_TRACKING = True
                        time.sleep(2)
                COUNTER_MOUTH = 0
