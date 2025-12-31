export async function getTopDishes() {
  const res = await fetch("/api/dishes/get_top_dishes");
  if (!res.ok) throw new Error("Failed to fetch top dishes");
  return res.json();
}

export async function getAllDishes() {
  const res = await fetch("/api/dishes/get_all_dishes");
  if (!res.ok) throw new Error("Failed to fetch dishes");
  return res.json();
}

export async function getFavoriteDishes(user_id) {
  const res = await fetch(`/api/favorites/get_favorite_dishes/${user_id}`);
  if (!res.ok) throw new Error("Failed to fetch favoriate dishes");
  return res.json();
}

export async function getDishesByDietary(dietary) {
  const res = await fetch(`/api/dishes/get_dishes_by_dietary/${dietary}`);
  if (!res.ok) throw new Error("Failed to fetch filtered dishes");
  return res.json();
}

export async function getDishesByIngredient(ingredient) {
  const res = await fetch(`/api/dishes/get_dishes_by_ingredient/${ingredient}`);
  if (!res.ok) throw new Error("Failed to fetch filtered dishes");
  return res.json();
}

export async function getDishesByAspect(aspect, value) {
  const res = await fetch(`/api/dishes/get_dishes_by_aspect/${aspect}/${value}`);
  if (!res.ok) throw new Error("Failed to fetch filtered dishes");
  return res.json();
}

export async function getDishInstance(dish_name) {
  const res = await fetch(`/api/dishes/get_dish_instance/${dish_name}`);
  if (!res.ok) throw new Error("Failed to fetch dish details");
  return res.json();
}

export async function getDishAggregates(dish_name) {
  const res = await fetch(`/api/dishes/get_dish_aggregates/${dish_name}`);
  if (!res.ok) throw new Error("Failed to fetch dish aggregates");
  return res.json();
}

export async function getSimilarDishes(dish_name) {
  const res = await fetch(`/api/dishes/get_similar_dishes/${dish_name}`);
  if (!res.ok) throw new Error("Failed to fetch similar dishes");
  return res.json();
}

export async function isDishFavorite(dish_name, user_id) {
  const res = await fetch(`/api/favorites/is_dish_favorite/${dish_name}/${user_id}`);
  if (!res.ok) throw new Error("Failed to fetch favorite status");
  return res.json();
}