export function resolveHistoryType(item) {
  if (item.dietary) return "dietary";
  if (item.nutrient) return "nutrient";
  if (item.ingredient) return "ingredient";
  if (item.rating !== undefined || item.healthiness !== undefined) return "taste";
  if (item.price !== undefined) return "price";

  throw new Error("Unknown history item type");
}