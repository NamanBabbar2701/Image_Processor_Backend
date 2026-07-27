import cv2

from app.processor.face_mesh import FaceMeshDetector
from app.processor.face_analyzer import FaceAnalyzer
from app.processor.aligner import FaceAligner
from app.processor.crop_planner import CropPlanner
from app.processor.crop_executor import CropExecutor
from app.processor.composition_validator import CompositionValidator
from app.processor.landmark_transformer import LandmarkTransformer
from app.processor.image_enhancer import ImageEnhancer
from app.processor.config import VALIDATION_CORRECTION_FACTOR, DEBUG


class PortraitProcessor:

    def __init__(self):

        self.detector = FaceMeshDetector()
        self.analyzer = FaceAnalyzer()
        self.aligner = FaceAligner()
        self.planner = CropPlanner()
        self.executor = CropExecutor()
        self.validator = CompositionValidator()
        self.transformer = LandmarkTransformer()
        self.enhancer = ImageEnhancer()
        
    def error_response(
        self,
        status,
        reason
    ):
        
        return {
            "success": False,
            "status": status,
            "reason": reason,
            "final_image": None,
            "debug_image": None
        }

    def process(self, image):
        try:
            # --------------------------
            # Detect
            # --------------------------

            data = self.detector.detect(image)

            if data is None:
                return self.error_response(
                    "No Face",
                    "No Face Detected"
                )

            analysis = self.analyzer.analyze(
                data["points"]
            )

            # --------------------------
            # Align
            # --------------------------

            align_result = self.aligner.align(
                image,
                analysis
            )
            
            aligned = align_result["image"]
            
            matrix = align_result["matrix"]

            # --------------------------
            # Detect Again
            # --------------------------

            rotated_points = self.transformer.transform(
                data["points"],
                matrix
            )
            
            aligned_analysis = self.analyzer.analyze(
                rotated_points
            )
        

            # --------------------------
            # Plan Crop
            # --------------------------
            aligned_height, aligned_width = aligned.shape[:2]
            
            crop = self.planner.plan(
                aligned_analysis,
                image_width=aligned_width,
                image_height=aligned_height
            )

            # --------------------------
            # Execute Crop
            # --------------------------

            final_image = self.executor.execute(
                aligned,
                crop
            )

            # --------------------------
            # Validate
            # --------------------------

            final_data = self.detector.detect(final_image)

            if final_data is not None:

                final_analysis = self.analyzer.analyze(
                    final_data["points"]
                )

                validation = self.validator.validate(
                    final_analysis
                )

                if validation["needs_correction"]:
                    
                    correction_x = round(
                        validation["dx"] * VALIDATION_CORRECTION_FACTOR
                    )
                    
                    correction_y = round(
                        validation["dy"] * VALIDATION_CORRECTION_FACTOR
                    )

                    crop["x1"] -= correction_x
                    crop["x2"] -= correction_x

                    crop["y1"] -= correction_y
                    crop["y2"] -= correction_y
                    
                    for key in ("x1","y1","x2","y2"):
                        crop[key] = int(round(crop[key]))
                        

                    final_image = self.executor.execute(
                        aligned,
                        crop
                    )

                    final_image = self.enhancer.sharpen(
                        final_image
                    )
            # --------------------------
            # Debug Image
            # --------------------------
            
            center_x = int(aligned_analysis["center_x"])
            center_y = int(aligned_analysis["center_y"])
            eye_center = int(aligned_analysis["eye_center"][1])
            
            debug_image = None
            
            if DEBUG:
                
                debug_image = self.detector.draw_points(
                    aligned,
                    rotated_points
                )

                cv2.rectangle(
                    debug_image,
                    (
                        int(crop["x1"]),
                        int(crop["y1"])
                    ),
                    (
                        int(crop["x2"]),
                        int(crop["y2"])
                    ),
                    (0,255,255),
                    3
                )

                cv2.circle(
                    debug_image,
                    (
                        center_x,
                        center_y
                    ),
                    8,
                    (255,0,255),
                    -1
                )

                cv2.line(
                    debug_image,
                    (
                        0,
                        eye_center
                    ),
                    (
                        debug_image.shape[1],
                        eye_center
                    ),
                    (255,255,0),
                    2
                )

            return {
                "success" : True,
                "status" : "Processed",
                "reason" : "",
                "final_image": final_image,
                "debug_image": debug_image        
            }
            
        except Exception as e:
            return self.error_response(
                "Failed",
                str(e)
            ) 