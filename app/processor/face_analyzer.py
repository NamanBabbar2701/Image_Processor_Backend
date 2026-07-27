import numpy as np
from app.processor.config import (
    HEAD_HEIGHT_MULTIPLIER,
    HEAD_SIDE_MARGIN,
    CENTER_EYE_WEIGHT,
    CENTER_NOSE_WEIGHT
)

# MediaPipe Face Oval
FACE_OVAL = [
    10, 338, 297, 332, 284, 251, 389, 356,
    454, 323, 361, 288, 397, 365, 379, 378,
    400, 377, 152, 148, 176, 149, 150, 136,
    172, 58, 132, 93, 234, 127, 162, 21,
    54, 103, 67, 109
]


class FaceAnalyzer:

    def analyze(self, points):

        # --------------------------------------------------
        # FACE OVAL
        # --------------------------------------------------

        oval = np.array([points[i] for i in FACE_OVAL], dtype=float)

        face_left = np.min(oval[:, 0])
        face_right = np.max(oval[:, 0])

        face_top = np.min(oval[:, 1])
        face_bottom = np.max(oval[:, 1])

        face_width = face_right - face_left
        face_height = face_bottom - face_top

        # --------------------------------------------------
        # LANDMARKS
        # --------------------------------------------------

        left_eye = np.array(points[33], dtype=float)
        right_eye = np.array(points[263], dtype=float)

        eye_center = (left_eye + right_eye) / 2

        eye_distance = np.linalg.norm(
            right_eye - left_eye
        )

        nose = np.array(points[1], dtype=float)

        mouth = np.array(points[13], dtype=float)

        chin = np.array(points[152], dtype=float)

        # --------------------------------------------------
        # HEAD ESTIMATION
        # --------------------------------------------------

        head_left = (
            face_left -
            face_width * HEAD_SIDE_MARGIN
        )

        head_right = (
            face_right +
            face_width * HEAD_SIDE_MARGIN
        )

        head_width = head_right - head_left

        eye_to_chin = np.linalg.norm(
            chin - eye_center
        )

        estimated_head_height = (
            eye_to_chin *
            HEAD_HEIGHT_MULTIPLIER
        )

        head_top = max(
            0.0,
            chin[1] - estimated_head_height
        )

        head_bottom = max(
            head_top,
            chin[1]
        )

        head_height = head_bottom - head_top

        # --------------------------------------------------
        # PORTRAIT CENTER
        # --------------------------------------------------

        eye_center_x = eye_center[0]

        center_x = (
            CENTER_EYE_WEIGHT * eye_center_x +
            CENTER_NOSE_WEIGHT * nose[0]
        )

        center_y = (
            head_top + head_bottom
        ) / 2

        # --------------------------------------------------
        # RETURN
        # --------------------------------------------------

        return {

            # Face
            "face_left": face_left,
            "face_right": face_right,
            "face_top": face_top,
            "face_bottom": face_bottom,
            "face_width": face_width,
            "face_height": face_height,

            # Head
            "head_left": head_left,
            "head_right": head_right,
            "head_top": head_top,
            "head_bottom": head_bottom,
            "head_width": head_width,
            "head_height": head_height,

            "head_box": {
                "left": head_left,
                "top": head_top,
                "right": head_right,
                "bottom": head_bottom
            },

            # Portrait
            "center_x": center_x,
            "center_y": center_y,

            # Eyes
            "eye_center": (
                eye_center[0],
                eye_center[1]
            ),
            "eye_distance": eye_distance,

            # Landmarks
            "left_eye": tuple(left_eye),
            "right_eye": tuple(right_eye),
            "nose": tuple(nose),
            "mouth": tuple(mouth),
            "chin": tuple(chin)
        }