from .vector import TASTE_KEYS

MAX_DISTANCE = len(TASTE_KEYS)

def taste_distance(target, candidate):
    distance = 0.0

    for i in range(len(TASTE_KEYS)):
        distance += abs(target[i] - candidate[i])

    return distance / MAX_DISTANCE