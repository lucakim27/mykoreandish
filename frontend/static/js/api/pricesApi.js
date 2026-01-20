export async function getPriceInfo(dish_name) {
  const res = await fetch(`/api/prices/${dish_name}`);
  if (!res.ok) throw new Error("Failed to fetch price info");
  return res.json();
}