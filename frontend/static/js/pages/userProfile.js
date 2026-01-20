import { getUserProfile } from "../api/usersApi.js";
import { renderUserProfile } from "../render/userProfileRender.js";
import { getUserIdFromPath } from "../utils/url.js";
import { getUserHistory } from "../api/historyApi.js";
import { renderUserHistory } from "../render/userProfileRender.js";

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const user_id = getUserIdFromPath();

    const [user, history] = await Promise.all([
      getUserProfile(user_id),
      getUserHistory(user_id)
    ]);

    renderUserProfile(user);
    renderUserHistory(history.history);

  } catch (err) {
    console.error(err);
  }
});
