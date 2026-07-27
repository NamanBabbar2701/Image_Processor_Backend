import cv2
import numpy as np

from app.processor.config import (
    PADDING_COLOR,
    MAX_ROTATION_ANGLE,
    MIN_ROTATION_ANGLE
)


class FaceAligner:

    def calculate_rotation(self, analysis):

        left_eye = np.array(
            analysis["left_eye"],
            dtype=float
        )

        right_eye = np.array(
            analysis["right_eye"],
            dtype=float
        )

        dx = right_eye[0] - left_eye[0]
        dy = right_eye[1] - left_eye[1]

        angle = np.degrees(
            np.arctan2(dy, dx)
        )

        if abs(angle) < MIN_ROTATION_ANGLE:
            angle = 0

        return max(
            -MAX_ROTATION_ANGLE,
            min(MAX_ROTATION_ANGLE, angle)
        )

    def align(
        self,
        image,
        analysis
    ):

        angle = self.calculate_rotation(
            analysis
        )

        h, w = image.shape[:2]

        center = analysis["eye_center"]

        M = cv2.getRotationMatrix2D(
            center,
            angle,
            1.0
        )

        cos = abs(M[0, 0])
        sin = abs(M[0, 1])

        new_w = int(h * sin + w * cos)
        new_h = int(h * cos + w * sin)

        M[0, 2] += new_w / 2 - center[0]
        M[1, 2] += new_h / 2 - center[1]

        rotated = cv2.warpAffine(
            image,
            M,
            (new_w, new_h),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REPLICATE,
        )
        
        return {
            "image": rotated,
            "matrix":M,
            "width":new_w,
            "height":new_h,
            "angle":angle
        }