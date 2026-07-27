import numpy as np

from app.processor.config import *


class CropPlanner:

    # def plan(
    #     self,
    #     analysis,
    #     image_width,
    #     image_height
    # ):

    #     head_width = analysis["head_width"]
    #     head_height = analysis["head_height"]

    #     head_left = analysis["head_left"]
    #     head_top = analysis["head_top"]

    #     center_x = analysis["center_x"]
    #     center_y = analysis["center_y"]

    #     # -----------------------------------
    #     # Crop Size
    #     # -----------------------------------

    #     crop_height = head_height / HEAD_HEIGHT_RATIO
    #     crop_width = crop_height * ASPECT_RATIO

    #     minimum_width = head_width / HEAD_WIDTH_RATIO

    #     if crop_width < minimum_width:
    #         crop_width = minimum_width
    #         crop_height = crop_width / ASPECT_RATIO

    #     # -----------------------------------
    #     # Horizontal Position
    #     # -----------------------------------

    #     horizontal_margin = crop_width - head_width

    #     x1 = head_left - horizontal_margin / 2

    #     # -----------------------------------
    #     # Vertical Position
    #     # -----------------------------------

    #     top_margin = crop_height * TOP_MARGIN_RATIO

    #     y1 = head_top - top_margin

    #     x2 = x1 + crop_width
    #     y2 = y1 + crop_height

    #     # -----------------------------------
    #     # Keep Crop Inside Image
    #     # -----------------------------------

    #     if x1 < 0:
    #         x2 -= x1
    #         x1 = 0

    #     if y1 < 0:
    #         y2 -= y1
    #         y1 = 0

    #     if x2 > image_width:
    #         shift = x2 - image_width
    #         x1 -= shift
    #         x2 = image_width

    #     if y2 > image_height:
    #         shift = y2 - image_height
    #         y1 -= shift
    #         y2 = image_height

    #     x1 = max(0, x1)
    #     y1 = max(0, y1)

    #     return {

    #         "x1": x1,
    #         "y1": y1,
    #         "x2": x2,
    #         "y2": y2,

    #         "width": x2 - x1,
    #         "height": y2 - y1,

    #         "center_x": center_x,
    #         "center_y": center_y,

    #         "top_margin": top_margin
    #     }
    
    def plan(
        self,
        analysis,
        image_width,
        image_height
    ):
        
        head_width = analysis["head_width"]
        head_height = analysis["head_height"]
        
        center_x = analysis["center_x"]
        
        eye_y = analysis["eye_center"][1]
        
        
        # --------------------------
        # Crop Size
        # --------------------------
        
        crop_height = head_height / HEAD_HEIGHT_RATIO
        crop_width = crop_height * ASPECT_RATIO
        
        minimum_width = head_width / HEAD_WIDTH_RATIO
        
        if crop_width < minimum_width:
            crop_width = minimum_width
            crop_height = crop_width / ASPECT_RATIO
            
        # --------------------------
        # Position
        # --------------------------
        
        x1 = center_x - crop_width / 2
        
        y1 = eye_y - crop_height * EYE_LINE_RATIO
        
        x2 = x1 + crop_width
        y2 = y1 + crop_height
        
        # --------------------------
        # Keep inside image
        # --------------------------
        
        if x1 < 0:
            x2 -= x1
            x1 = 0
        
        if y1 < 0:
            y2 -= y1
            
        if x2 > image_width:
            shift = x2 - image_width
            x1 -= shift
            x2 = image_width
            
        if y2 > image_height:
            shift = y2 - image_height
            y1 -= shift
            y2 = image_height
            
        x1 = max(0, x1)
        y1 = max(0, y1)
        
        return {
            
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            
            "width": crop_width,
            "height": crop_height,
            
             "center_x": center_x,
             "center_y": analysis["center_y"]
        }