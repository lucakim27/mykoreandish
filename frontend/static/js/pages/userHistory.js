import { getUserHistory, getHistoryMeta } from "../api/historyApi.js";
import { renderUserHistory } from "../render/userHistoryRender.js";
import { getCurrentUser } from "../api/usersApi.js";
import { bindDietaryDelete } from "../events/buttonEvents.js";

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const user = await getCurrentUser();

    const [historyRes, metaRes] = await Promise.all([
      getUserHistory(user.user.google_id),
      getHistoryMeta()
    ]);

    renderUserHistory(historyRes.history, metaRes);
    bindDietaryDelete();
    
  } catch (err) {
    console.error(err);
  }
});
