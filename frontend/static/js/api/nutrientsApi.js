export async function getAllNutrients() {
  const res = await fetch(`/api/nutrients/`);
  if (!res.ok) throw new Error("Failed to fetch all nutrients");
  return res.json();
}

export async function getIngredientNutrients(ingredient_name) {
  const res = await fetch(`/api/nutrients/${ingredient_name}`);
  if (!res.ok) throw new Error("Failed to fetch all nutrients");
  return res.json();
}