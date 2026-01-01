import { renderAuth } from "../render/authRender.js";
import { getCurrentUser } from "../api/usersApi.js";

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const user = await getCurrentUser();

    renderAuth(user.user);

  } catch (err) {
    console.error(err);
  }
});
