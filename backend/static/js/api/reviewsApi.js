export async function getTotalReviews() {
  const res = await fetch("/api/reviews/get_total_reviews");
  if (!res.ok) throw new Error("Failed to fetch total reviews");
  return res.json();
}