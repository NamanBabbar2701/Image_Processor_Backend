import cv2
import numpy as np

from app.processor.config import (
    ENABLE_SHARPENING,
    SHARPEN_SIGMA,
    SHARPEN_AMOUNT,
    SHARPEN_THRESHOLD
)


class ImageEnhancer:

    def sharpen(
        self,
        image
    ):

        if not ENABLE_SHARPENING:
            return image

        blurred = cv2.GaussianBlur(
            image,
            (0, 0),
            SHARPEN_SIGMA
        )

        sharpened = cv2.addWeighted(
            image,
            1 + SHARPEN_AMOUNT,
            blurred,
            -SHARPEN_AMOUNT,
            0
        )

        # Prevent sharpening of very smooth regions
        low_contrast = np.abs(
            image.astype(np.int16) -
            blurred.astype(np.int16)
        ) < SHARPEN_THRESHOLD

        np.copyto(
            sharpened,
            image,
            where=low_contrast
        )

        return sharpened