export async function getSimilarTasteDishes(dish_name) {
  const res = await fetch(`/api/tastes/similar/${dish_name}`);
  if (!res.ok) throw new Error("Failed to fetch similar taste dishes");
  return res.json();
}