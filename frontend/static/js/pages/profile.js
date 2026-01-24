import { getCurrentUser } from "../api/usersApi.js";
import { renderProfile } from "../render/profileRender.js";
import { getAllDietaries } from "../api/dietariesApi.js";
import { bindDietaryPreferenceButton } from "../events/selectEvents.js"

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const user = await getCurrentUser();
    const [allDietaries] = await Promise.all([
          getAllDietaries()
        ]);
    
    renderProfile(allDietaries, user);
    bindDietaryPreferenceButton();

  } catch (err) {
    console.error(err);
  }
});
