export async function getCurrentUser() {
  const res = await fetch("/api/users/me");
  if (!res.ok) throw new Error("Failed to fetch user");
  return res.json();
}

export async function getTotalUsers() {
  const res = await fetch("/api/users/get_total_users");
  if (!res.ok) throw new Error("Failed to fetch total users");
  return res.json();
}

export async function getAllUsers() {
  const res = await fetch("/api/users/get_all_users");
  if (!res.ok) throw new Error("Failed to fetch all users");
  return res.json();
}

export async function getUserProfile(user_id) {
  const res = await fetch(`/api/users/get_user/${user_id}`);
  if (!res.ok) throw new Error("Failed to fetch user profile");
  return res.json();
}

export async function updateDietaryPreference(user_id) {
  const res = await fetch(`/api/users/update_dietary_preference/${user_id}`);
  if (!res.ok) throw new Error("Failed to fetch user profile");
  return res.json();
}