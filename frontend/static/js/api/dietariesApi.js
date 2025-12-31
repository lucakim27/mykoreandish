export async function getAllDietaries() {
  const res = await fetch("/api/dietaries/get_all_dietaries");
  if (!res.ok) throw new Error("Failed to fetch dietaries");
  return res.json();
}
