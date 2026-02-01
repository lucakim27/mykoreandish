TASTE_KEYS = [
    "spiciness",
    "sweetness",
    "sourness",
    "healthiness",
    "texture",
    "temperature",
]

TASTE_MIN = 0.0
TASTE_MAX = 5.0

def build_taste_vector(aggregate):
    taste_vector = []
    for key in TASTE_KEYS:
        taste_vector.append(float(aggregate.get(key, 0.0)))
    return taste_vector

def normalize_taste_vector(taste_vector):
    scale = TASTE_MAX - TASTE_MIN
    normalized_vector = []
    for vector in taste_vector:
        normalized_vector.append((vector - TASTE_MIN) / scale)
    return normalized_vector