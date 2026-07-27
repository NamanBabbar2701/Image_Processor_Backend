import cv2
import mediapipe as mp
import numpy as np


class FaceMeshDetector:

    def __init__(self):

        self.mp_face_mesh = mp.solutions.face_mesh

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.7
        )

        self.drawer = mp.solutions.drawing_utils
        self.styles = mp.solutions.drawing_styles

    def detect(self, image):

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return None

        face = results.multi_face_landmarks[0]

        h, w = image.shape[:2]

        points = [
            (lm.x * w, lm.y * h)
            for lm in face.landmark
        ]

        

        return {
            "landmarks": face,
            "points": points,
            "width": w,
            "height": h
        }

    def draw(self, image, data):

        output = image.copy()

        face = data["landmarks"]
        points = data["points"]

        self.drawer.draw_landmarks(
            output,
            face,
            self.mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=self.styles.get_default_face_mesh_tesselation_style()
        )
        
        # Key landmarks
        left_eye = tuple(map(int,points[33]))
        right_eye = tuple(map(int,points[263]))
        nose = tuple(map(int,points[1]))
        mouth = tuple(map(int,points[13]))
        chin = tuple(map(int,points[152]))

        # Draw large circles
        cv2.circle(output, left_eye, 10, (255,0,0), -1)
        cv2.circle(output, right_eye, 10, (255,0,0), -1)
        cv2.circle(output, nose, 10, (0,0,255), -1)
        cv2.circle(output, mouth, 10, (0,255,255), -1)
        cv2.circle(output, chin, 10, (255,255,0), -1)

        for idx in [1, 33, 263, 13, 152]:
            pt = tuple(map(int , points[idx]))
            cv2.putText(
                output,
                str(idx),
                (pt[0] + 5 , pt[1] - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                1
            )
        
        return output
    
    def draw_points(
        self,
        image,
        points
    ):

        debug = image.copy()

        for x, y in points:

            cv2.circle(
                debug,
                (int(x), int(y)),
                1,
                (0, 255, 0),
                -1
            )

        return debug