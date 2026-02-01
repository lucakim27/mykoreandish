from backend.services.taste_similarity.vector import (
    build_taste_vector,
    normalize_taste_vector,
)
from backend.services.taste_similarity.distance import taste_distance

class TasteSimilarityService:
    def __init__(self, aggregate_manager):
        self.aggregate_manager = aggregate_manager

    def find_similar_dishes(self, dish_name: str, k: int = 5) -> list[dict]:
        target_agg = self.aggregate_manager.get_aggregate_by_dish_name(dish_name)
        target_taste_vector = build_taste_vector(target_agg)
        target_vector = normalize_taste_vector(target_taste_vector)

        scored = []
        candidates = self.aggregate_manager.get_all_aggregates()
        for candidate in candidates:
            if candidate.get("dish_name") == dish_name:
                continue

            candidate_taste_vector = build_taste_vector(candidate)
            candidate_vector = normalize_taste_vector(candidate_taste_vector)
            distance = taste_distance(target_vector, candidate_vector)
            similarity_percentage = round((1.0 - distance) * 100, 2)

            scored.append({
                "dish_name": candidate["dish_name"],
                "similarity_percentage": similarity_percentage,
            })

        scored.sort(key=lambda x: x["similarity_percentage"], reverse=True)
        return scored[:k]