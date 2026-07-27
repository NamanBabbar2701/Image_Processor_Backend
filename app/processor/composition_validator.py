from app.processor.config import (
    OUTPUT_WIDTH,
    OUTPUT_HEIGHT,
    EYE_LINE_RATIO,
    CENTER_TOLERANCE,
    EYE_TOLERANCE,
    MAX_CORRECTION
)


class CompositionValidator:

    def __init__(self):

        self.target_center_x = OUTPUT_WIDTH / 2
        self.target_eye_y = OUTPUT_HEIGHT * EYE_LINE_RATIO

    def validate(self, analysis):

        actual_center_x = analysis["center_x"]
        actual_eye_y = analysis["eye_center"][1]

        # ----------------------------
        # Horizontal Error
        # ----------------------------

        dx = self.target_center_x - actual_center_x

        # ----------------------------
        # Vertical Error
        # ----------------------------

        dy = self.target_eye_y - actual_eye_y

        # ----------------------------
        # Ignore Tiny Errors
        # ----------------------------

        if abs(dx) < CENTER_TOLERANCE:
            dx = 0

        if abs(dy) < EYE_TOLERANCE:
            dy = 0

        # ----------------------------
        # Clamp Large Corrections
        # ----------------------------

        dx = max(
            -MAX_CORRECTION,
            min(MAX_CORRECTION, dx)
        )

        dy = max(
            -MAX_CORRECTION,
            min(MAX_CORRECTION, dy)
        )

        return {

            "dx": int(round(dx)),
            "dy": int(round(dy)),

            "needs_correction":

                dx != 0 or dy != 0
        }