export async function getNote(name, user_id) {
  const res = await fetch(`/api/notes/${name}/${user_id}`);
  if (!res.ok) throw new Error("Failed to fetch note");
  return res.json();
}

export async function addNote(name, user_id, note_content) {
    const res = await fetch(`/api/notes/${name}/${user_id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ note_content })
    });

    if (!res.ok) {
        throw new Error(`Failed to add note (status ${res.status})`);
    }
}