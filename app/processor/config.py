# =====================================================
# OUTPUT SETTINGS
# =====================================================

# Passport Photo Size
OUTPUT_WIDTH = 413
OUTPUT_HEIGHT = 531

# Aspect Ratio (413 × 531)
ASPECT_RATIO = OUTPUT_WIDTH / OUTPUT_HEIGHT


# =====================================================
# PORTRAIT COMPOSITION
# =====================================================

# Whole head should occupy approximately 75% of image height
HEAD_HEIGHT_RATIO = 0.75

# Whole head should occupy approximately 68% of image width
HEAD_WIDTH_RATIO = 0.68

# Space above hair
TOP_MARGIN_RATIO = 0.15

# Eyes should lie around 40% from top
EYE_LINE_RATIO = 0.40


# =====================================================
# FACE ESTIMATION
# =====================================================

# Estimate complete head from eye-to-chin distance
HEAD_HEIGHT_MULTIPLIER = 1.70

# Extra width added for hair
HEAD_SIDE_MARGIN = 0.18


# =====================================================
# FACE CENTER ESTIMATION
# =====================================================

CENTER_EYE_WEIGHT = 0.80
CENTER_NOSE_WEIGHT = 0.20


# =====================================================
# FACE ALIGNMENT
# =====================================================

# Ignore tiny rotations
MIN_ROTATION_ANGLE = 1

# Clamp large rotations
MAX_ROTATION_ANGLE = 10


# =====================================================
# VALIDATION
# =====================================================

CENTER_TOLERANCE = 5
EYE_TOLERANCE = 6
VALIDATION_CORRECTION_FACTOR = 0.8

# Maximum crop correction in pixels
MAX_CORRECTION = 15


# =====================================================
# IMAGE
# =====================================================

PADDING_COLOR = (255, 255, 255)


# =====================================================
# DEBUG
# =====================================================

DEBUG = True

# ------------------------------------
# Image Enhancement
# ------------------------------------

ENABLE_SHARPENING = True

SHARPEN_SIGMA = 1.2

SHARPEN_AMOUNT = 1.3

SHARPEN_THRESHOLD = 3