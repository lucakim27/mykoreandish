export async function getUserHistory(user_id) {
    const res = await fetch(`/api/histories/get_user_history/${user_id}`);
    if (!res.ok) throw new Error("Failed to fetch user history");
    return res.json();
}

export async function getHistoryMeta() {
    const res = await fetch(`/api/histories/get_history_meta`);
    if (!res.ok) throw new Error("Failed to fetch history meta");
    return res.json();
}