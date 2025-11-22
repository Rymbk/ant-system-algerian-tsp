"""
Distance calculation utilities
"""
import numpy as np


def calculate_euclidean_distance(city1, city2):
    """
    Calculate Euclidean distance between two cities based on coordinates.
    
    Args:
        city1 (dict): First city with 'lat' and 'lon' keys
        city2 (dict): Second city with 'lat' and 'lon' keys
    
    Returns:
        float: Euclidean distance between the two cities
    """
    lat_diff = city1['lat'] - city2['lat']
    lon_diff = city1['lon'] - city2['lon']
    return np.sqrt(lat_diff**2 + lon_diff**2)


def build_distance_matrix(cities):
    """
    Build a distance matrix for all cities.
    
    Args:
        cities (list): List of city dictionaries with 'lat' and 'lon' keys
    
    Returns:
        numpy.ndarray: 2D distance matrix where element [i][j] represents
                      the distance between city i and city j
    """
    n = len(cities)
    matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = calculate_euclidean_distance(cities[i], cities[j])
    
    return matrix