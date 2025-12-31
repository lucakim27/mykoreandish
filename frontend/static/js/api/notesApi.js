export async function getNote(name, user_id) {
  const res = await fetch(`/api/notes/get_note/${name}/${user_id}`);
  if (!res.ok) throw new Error("Failed to fetch note");
  return res.json();
}
