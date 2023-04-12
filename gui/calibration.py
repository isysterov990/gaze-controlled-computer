import statistics
import time

import dlib

from detectors.feature_detector import *
from detectors.keypoint_detector import *


def calibrate():
    keypoints = []
    calibration_points = []

    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    i = 0
    while (i < 4):
        _, input = capture.read()  # used _ to ignore the boolean returned by .read()
        input = cv2.flip(input, 1)
        eye_frames = detect_eyes(input)

        if eye_frames is not None:
            left_keypoint = find_keypoints(eye_frames[0])
            right_keypoint = find_keypoints(eye_frames[1])
            if left_keypoint and right_keypoint:
                avg_x = (left_keypoint[0].pt[0] + right_keypoint[0].pt[0]) / 2
                avg_y = (left_keypoint[0].pt[1] + right_keypoint[0].pt[1]) / 2

                keypoints.append([avg_x, avg_y])
                # print(keypoint[0].pt[0], keypoint[0].pt[1])
                if len(keypoints) == 100:
                    x_values = [kp[0] for kp in keypoints[:100]]
                    y_values = [kp[1] for kp in keypoints[:100]]

                    avg_x = statistics.mean(x_values)
                    avg_y = statistics.mean(y_values)

                    print(f"Average x: {round(avg_x, 2)}")
                    print(f"Average y: {round(avg_y, 2)}\n")

                    calibration_points.append([avg_x, avg_y])

                    del keypoints[:]
                    i += 1
                    time.sleep(2)

        # k = cv2.waitKey(30) & 0xff
        # if k == 27:
        #     break

    capture.release()
    return calibration_points


circle_positions = [(100, 100), (1720, 100), (1720, 880), (100, 880)]
reference_points = [(250, 250), (670, 250), (250, 600), (670, 600)]
# Define the regions of interest for each eye
left_eye_roi = [(36, 37, 38, 39, 40, 41)]
right_eye_roi = [(42, 43, 44, 45, 46, 47)]
circle_radius = 50


def get_gaze_point():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # Initialize the dlib face detector and facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("./models/shape_predictor_68_face_landmarks.dat")
    max_x = 640
    min_x = 0
    max_y = 480
    min_y = 0
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        # Extract the left and right eye landmarks
        left_eye_landmarks = [landmarks.part(i) for i in left_eye_roi[0]]
        right_eye_landmarks = [landmarks.part(i) for i in right_eye_roi[0]]
        left_eye_center = np.mean([np.array([p.x, p.y]) for p in left_eye_landmarks], axis=0)
        right_eye_center = np.mean([np.array([p.x, p.y]) for p in right_eye_landmarks], axis=0)
        gaze_point = ((left_eye_center[0] + right_eye_center[0]) / 2, (left_eye_center[1] + right_eye_center[1]) / 2)
        gaze_point = (int(gaze_point[0]), int(gaze_point[1]))
        # Ensure that the gaze point is within the bounds
        if gaze_point[0] > max_x:
            gaze_point = (max_x, gaze_point[1])
        elif gaze_point[0] < min_x:
            gaze_point = (min_x, gaze_point[1])
        if gaze_point[1] > max_y:
            gaze_point = (gaze_point[0], max_y)
        elif gaze_point[1] < min_y:
            gaze_point = (gaze_point[0], min_y)

        return gaze_point


def adjust_eye_tracking(calibration_points):
    left_eye_sums = np.zeros(2)
    right_eye_sums = np.zeros(2)
    calibration_points = [p for p in calibration_points if p is not None]
    for i, (left_eye_point, right_eye_point) in enumerate(calibration_points):
        if left_eye_point and right_eye_point is not None:
            left_eye_sums += np.array(left_eye_point)
            right_eye_sums += np.array(right_eye_point)
    left_eye_means = left_eye_sums / len(calibration_points)
    right_eye_means = right_eye_sums / len(calibration_points)
    left_eye_offset = np.array([reference_points[0][0], reference_points[0][1]]) - left_eye_means
    right_eye_offset = np.array([reference_points[0][0], reference_points[0][1]]) - right_eye_means
    return left_eye_offset, right_eye_offset
