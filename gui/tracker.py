import cv2
import dlib
import numpy as np
import pyautogui
from imutils import face_utils
from scipy.spatial import distance as dist

from gui.calibration import adjust_eye_tracking

left_eye_roi = [(36, 37, 38, 39, 40, 41)]
right_eye_roi = [(42, 43, 44, 45, 46, 47)]
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


def track_eyes(calibration_points):
    EYE_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 3
    TOTAL = 0
    COUNTER = 0
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("./models/shape_predictor_68_face_landmarks.dat")
    left_eye_offset, right_eye_offset = adjust_eye_tracking(calibration_points)
    while True:
        ret, frame = cap.read()
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
            # Define the screen resolution
            screen_width, screen_height = pyautogui.size()
            # Define the mouse speed
            mouse_speed = 50
            movement_range = 10000
            # Move the mouse based on the eye tracking
            mouse_x = int(gaze_position[0] / 640 * screen_width)
            mouse_y = int(gaze_position[1] / 480 * screen_height)
            mouse_x_offset = (mouse_x - screen_width / 2) / (screen_width / 2) * movement_range
            mouse_y_offset = (mouse_y - screen_height / 2) / (screen_height / 2) * movement_range
            if left_eye_center[0] < right_eye_center[0]:
                mouse_x_offset *= -1
            pyautogui.FAILSAFE = False
            pyautogui.moveTo(screen_width / 2 + mouse_x_offset, screen_height / 2 + mouse_y_offset,
                             duration=mouse_speed / 1000)

            landmarks = face_utils.shape_to_np(landmarks)
            left_eye = landmarks[lStart:lEnd]
            right_eye = landmarks[rStart:rEnd]
            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)

            # Compute the average eye aspect ratio
            ear = (left_ear + right_ear) / 2.0
            if ear < EYE_AR_THRESH:
                COUNTER += 1
            else:
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    pyautogui.click()
                COUNTER = 0
