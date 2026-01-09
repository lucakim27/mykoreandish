import { showToast } from "../utils/toaster.js";
import { deleteHistoryByType } from "../api/historiesApi.js";

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
