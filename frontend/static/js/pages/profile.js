import { getCurrentUser } from "../api/usersApi.js";
import { renderProfile } from "../render/profileRender.js";
import { getAllDietaries } from "../api/dietariesApi.js";
import { bindDietaryPreferenceButton } from "../events/selectEvents.js"

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const [
      user,
      dietaries
    ] = await Promise.all([
      getCurrentUser(),
      getAllDietaries()
    ]);
    
    renderProfile(dietaries, user);
    bindDietaryPreferenceButton();

  } catch (err) {
    console.error(err);
  }
});
