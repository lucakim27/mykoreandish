export async function isDishFavorite(dish_name, user_id) {
  const res = await fetch(`/api/favorites/${dish_name}/${user_id}`);
  if (!res.ok) throw new Error("Failed to fetch favorite status");
  return res.json();
}

export async function getFavoriteDishes(user_id) {
  const res = await fetch(`/api/favorites/${user_id}`);
  if (!res.ok) throw new Error("Failed to fetch favoriate dishes");
  return res.json();
}