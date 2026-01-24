import { showToast } from "../utils/toaster.js";

export function bindDietaryPreferenceButton() {
  document.addEventListener("change", async (event) => {
    const select = event.target.closest(".dietary_preference");
    if (!select || select.disabled) return;

    const formData = new FormData();
    formData.append("dietary_preference", select.value);

    try {
      const res = await fetch("/api/users/dietary", {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      if (!res.ok) {
        throw new Error(`Request failed: ${res.status}`);
      }

      showToast("Dietary preference updated", "success");
    } catch (err) {
      console.error(err);
      showToast("Failed to update dietary preference", "error");
    }
  });
}
