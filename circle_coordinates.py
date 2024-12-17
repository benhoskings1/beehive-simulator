import math
from utils import vec


def get_coordinates(sides, radius, offset=vec(0, 0)):
    angles = []
    coordinates = []
    count = 0
    for side in range(sides):
        base_angle = 2 * math.pi / sides
        angle = base_angle * count
        angles.append(angle)
        count += 1

    for angle in angles:
        coordinate = vec(radius*(1 + math.sin(angle)), radius * (1 - math.cos(angle))) + offset
        coordinates.append(coordinate)

    return coordinates
