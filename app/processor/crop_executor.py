import cv2

from app.processor.config import OUTPUT_WIDTH, OUTPUT_HEIGHT


class CropExecutor:

    # def execute(
    #     self,
    #     image,
    #     crop
    # ):

    #     h, w = image.shape[:2]

    #     # --------------------------
    #     # Integer Coordinates
    #     # --------------------------

    #     x1 = int(round(crop["x1"]))
    #     y1 = int(round(crop["y1"]))
    #     x2 = int(round(crop["x2"]))
    #     y2 = int(round(crop["y2"]))

    #     # --------------------------
    #     # Clip to Image Bounds
    #     # --------------------------

    #     x1 = max(0, min(x1, w - 1))
    #     y1 = max(0, min(y1, h - 1))

    #     x2 = max(x1 + 1, min(x2, w))
    #     y2 = max(y1 + 1, min(y2, h))

    #     # --------------------------
    #     # Crop
    #     # --------------------------

    #     cropped = image[y1:y2, x1:x2]

    #     if cropped.size == 0:
    #         raise ValueError("Crop produced an empty image.")

    #     crop_h, crop_w = cropped.shape[:2]

    #     interpolation = (
    #         cv2.INTER_AREA
    #         if crop_w > OUTPUT_WIDTH or crop_h > OUTPUT_HEIGHT
    #         else cv2.INTER_CUBIC
    #     )

    #     # --------------------------
    #     # Resize
    #     # --------------------------

    #     return cv2.resize(
    #         cropped,
    #         (OUTPUT_WIDTH, OUTPUT_HEIGHT),
    #         interpolation=interpolation
    #     )
    
    def execute(
        self,
        image,
        crop
    ):
        
        crop_width = float(crop["width"])
        crop_height = float(crop["height"])
        
        center = (
            float(crop["center_x"]),
            float(crop["center_y"])
        )
        
        
        # -----------------------
        # Sub Pixel Crop
        # -----------------------
        
        cropped = cv2.getRectSubPix(
            image,
            (
                int(round(crop_width)),
                int(round(crop_height))
            ),
            center
        )
        
        if cropped is None or cropped.size == 0:
            raise ValueError("Crop produced an empty image")
        
        # --------------------
        # Resize
        # --------------------
        
        interpolation = (
            cv2.INTER_AREA
            if crop_width > OUTPUT_WIDTH or crop_height > OUTPUT_HEIGHT
            else cv2.INTER_CUBIC
        )
        
        final = cv2.resize(
            cropped,
            (OUTPUT_WIDTH, OUTPUT_HEIGHT),
            interpolation=interpolation
        )
        
        return final