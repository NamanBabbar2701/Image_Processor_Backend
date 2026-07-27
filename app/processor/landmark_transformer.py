import numpy as np


class LandmarkTransformer:

    def transform(
        self,
        points,
        matrix
    ):

        transformed = []

        for x, y in points:

            p = np.array(
                [x, y, 1.0],
                dtype=float
            )

            new = matrix @ p

            transformed.append(
                (
                    float(new[0]),
                    float(new[1])
                )
            )

        return transformed