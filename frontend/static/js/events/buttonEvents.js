import { showToast } from "../utils/toaster.js";
import { deleteHistoryByType } from "../api/historyApi.js";

export function bindDietaryDelete() {
  document.addEventListener("click", async (event) => {
    const button = event.target.closest(".delete-btn");
    if (!button || button.disabled) return;

    const { historyId, type } = button.dataset;
    button.disabled = true;

    try {
      await deleteHistoryByType(type, historyId);
      showToast("History deleted successfully", "success");
      button.closest(".history-item")?.remove();
    } catch (err) {
      showToast("Failed to delete history", "error");
      console.error(err);
      button.disabled = false;
    }
  });
}

export function bindFavoriteButton() {
  document.addEventListener("click", async (e) => {
    const btn = e.target.closest(".favorite-btn");
    if (!btn) return;

    const { dish, user, favorite } = btn.dataset;
    const isFavorite = favorite === "true";

    const url = `/api/favorites/${dish}/${user}`;
    const method = isFavorite ? "DELETE" : "POST";

    btn.disabled = true;

    const res = await fetch(url, { method });

    if (!res.ok) {
      showToast("Failed to update favorite status", "error");
      btn.disabled = false;
      return;
    } else {
      showToast(`Dish ${isFavorite ? "removed from" : "added to"} favorites`, "success");
      btn.dataset.favorite = (!isFavorite).toString();
      const icon = btn.querySelector("i");
      icon.classList.toggle("fa-solid", !isFavorite);
      icon.classList.toggle("fa-regular", isFavorite);
      icon.style.color = !isFavorite ? "#d72638" : "";
      btn.disabled = false;
    }

  });
}