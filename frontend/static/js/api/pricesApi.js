export async function getAllLocations() {
  const res = await fetch("/api/prices/get_all_locations");
  if (!res.ok) throw new Error("Failed to fetch dish aggregates");
  return res.json();
}

export async function getPriceInfo(dish_name) {
  const res = await fetch(`/api/prices/get_price_info/${dish_name}`);
  if (!res.ok) throw new Error("Failed to fetch price info");
  return res.json();
}