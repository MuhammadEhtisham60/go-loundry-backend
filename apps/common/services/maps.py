import math
from typing import Tuple


class MapsService:
    """
    Services for map utilities including distance calculations
    and GPS verification.
    """

    @staticmethod
    def calculate_distance(
        lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """
        Calculates the Haversine distance in kilometers between two GPS coordinates.
        """
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(
            math.radians, [float(lat1), float(lon1), float(lat2), float(lon2)]
        )

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))
        r = 6371.0  # Radius of earth in kilometers.
        
        return round(c * r, 2)
