export async function getAllCountries() {
  const res = await fetch("/api/countries/");
  if (!res.ok) throw new Error("Failed to fetch dish aggregates");
  return res.json();
}
