export async function getUserHistory() {
    const res = await fetch(`/api/histories/`);
    if (!res.ok) throw new Error("Failed to fetch user history");
    return res.json();
}

const DELETE_ENDPOINTS = {
  dietary:   (id) => `/api/dietaries/${id}`,
  ingredient:(id) => `/api/ingredients/${id}`,
  taste:     (id) => `/api/tastes/${id}`,
  price:     (id) => `/api/prices/${id}`,
  nutrient:  (id) => `/api/nutrients/${id}`,
};

export async function deleteHistoryByType(type, id) {
  const endpoint = DELETE_ENDPOINTS[type];
  if (!endpoint) {
    throw new Error(`Unknown history type: ${type}`);
  }

  const res = await fetch(endpoint(id), {
    method: "DELETE",
  });

  if (!res.ok) {
    throw new Error("Delete failed");
  }
}