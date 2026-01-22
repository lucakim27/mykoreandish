import { getUserHistory, getHistoryMeta } from "../api/historyApi.js";
import { renderUserHistory } from "../render/userHistoryRender.js";
import { getCurrentUser } from "../api/usersApi.js";
import { bindDeleteButton } from "../events/buttonEvents.js";

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const user = await getCurrentUser();

    const [historyRes, metaRes] = await Promise.all([
      getUserHistory(user.google_id),
      getHistoryMeta()
    ]);

    renderUserHistory(historyRes.history, metaRes);
    bindDeleteButton();
    
  } catch (err) {
    console.error(err);
  }
});
