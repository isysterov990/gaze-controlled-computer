import numpy as np


def compute_ear(eye):

    """
    Computes Eye Aspect Ratio (EAR) given eye landmarks.
    We input a list of 2D coordinates representing the eye landmarks
    The function returns The computed Eye Aspect Ratio (EAR)
    """
    return (np.linalg.norm(eye[1] - eye[5]) + np.linalg.norm(eye[2] - eye[4])) / (
                    2 * np.linalg.norm(eye[0] - eye[3]))

