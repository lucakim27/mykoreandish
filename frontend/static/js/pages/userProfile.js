import { getUserProfile } from "../api/usersApi.js";
import { renderUserProfile } from "../render/userProfileRender.js";
import { getUserIdFromPath } from "../utils/url.js";

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const user_id = getUserIdFromPath();

    const [user] = await Promise.all([
      getUserProfile(user_id)
    ]);

    renderUserProfile(user.user);

  } catch (err) {
    console.error(err);
  }
});
