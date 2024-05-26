import numpy as np
from utils.location_utils import CustomerLocation
from utils.vehicle_utils import VehicleType

def calculate_distance(loc1: CustomerLocation, loc2: CustomerLocation) -> float:
    """
    Calculates the Euclidean distance between two locations.

    Args:
    loc1 (CustomerLocation): The first location.
    loc2 (CustomerLocation): The second location.

    Returns:
    float: The Euclidean distance between the two locations.
    """
    return 100 * np.sqrt((loc1.latitude - loc2.latitude) ** 2 + (loc1.longitude - loc2.longitude) ** 2)

def is_symmetric(matrix: np.ndarray) -> bool:
    """
    Checks if a matrix is symmetric.

    Args:
    matrix (np.ndarray): The matrix to check.

    Returns:
    bool: True if the matrix is symmetric, False otherwise.
    """
    return np.array_equal(matrix, matrix.T)
