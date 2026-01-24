export async function isFavorite(name) {
  const res = await fetch(`/api/favorites/${name}`);
  if (!res.ok) throw new Error("Failed to fetch favorite status");
  return res.json();
}

export async function getFavoriteDishes() {
  const res = await fetch(`/api/favorites`);
  if (!res.ok) throw new Error("Failed to fetch favoriate dishes");
  return res.json();
}