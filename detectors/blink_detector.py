# import cv2
# from imutils import face_utils
# from utils import math_utils
# import dlib

# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor("./models/shape_predictor_68_face_landmarks.dat")
# EYE_BLINK_CONSTANT = 0.25
# (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
# (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# def ear_detector(input, grayscale ,rect):
#     blink_count=0
#     landmarks = predictor(grayscale, rect)
#     landmarks = face_utils.shape_to_np(landmarks)
#     leftEyeLandmarks = landmarks[lStart:lEnd]
#     rightEyeLandmarks = landmarks[rStart:rEnd]
#     leftEAR = math_utils.compute_ear(leftEyeLandmarks)
#     rightEAR = math_utils.compute_ear(rightEyeLandmarks)
#     ear = (leftEAR + rightEAR) / 2.0
#     if ear < EYE_BLINK_CONSTANT:
#         cv2.putText(input, "Blink", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
#         blink_count+=1


#     return blink_count