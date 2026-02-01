export async function getNote(name) {
  const res = await fetch(`/api/notes/${name}`);
  if (!res.ok) throw new Error("Failed to fetch note");
  return res.json();
}

export async function addNote(name, note_content) {
    const res = await fetch(`/api/notes/${name}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ note_content })
    });

    if (!res.ok) {
        throw new Error(`Failed to add note (status ${res.status})`);
    }

    console.log(res)

    return res.status
}

export async function updateNote(name, note_content) {
    const res = await fetch(`/api/notes/${name}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ note_content })
    });

    if (!res.ok) {
        throw new Error(`Failed to add note (status ${res.status})`);
    }

    return res.status
}

export async function deleteNote(name) {
    const res = await fetch(`/api/notes/${name}`, {
        method: "DELETE"
    });

    if (!res.ok) {
        throw new Error(`Failed to add note (status ${res.status})`);
    }

    return res.status
}