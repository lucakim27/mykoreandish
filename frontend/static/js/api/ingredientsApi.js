export async function getTopIngredients() {
  const res = await fetch("/api/ingredients/top");
  if (!res.ok) throw new Error("Failed to fetch top ingredients");
  return res.json();
}

export async function getAllIngredients() {
  const res = await fetch("/api/ingredients/");
  if (!res.ok) throw new Error("Failed to fetch ingredients");
  return res.json();
}

export async function getIngredientInstance(ingredient_name) {
  const res = await fetch(`/api/ingredients/${ingredient_name}`);
  if (!res.ok) throw new Error("Failed to fetch ingredient detail");
  return res.json();
}

export async function getNoteByIngredient(ingredient_name, user_id) {
  const res = await fetch(`/api/favorites/get_ingredient_note/${ingredient_name}/${user_id}`);
  if (!res.ok) throw new Error("Failed to fetch ingredient favorite status");
  return res.json();
}