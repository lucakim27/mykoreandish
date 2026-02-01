import { getMyHistory } from "../api/historyApi.js";
import { renderUserHistory } from "../render/userHistoryRender.js";
import { bindDeleteButton, bindUpdateButton } from "../events/buttonEvents.js";
import { getAllNutrients } from "../api/nutrientsApi.js";
import { getAllDietaries } from "../api/dietariesApi.js";
import { getAllCountries } from "../api/countriesApi.js";
import { getAllIngredients } from "../api/ingredientsApi.js";

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const [
      historyRes,
      allDietaries,
      allIngredients,
      allNutrients,
      allCountries
    ] = await Promise.all([
      getMyHistory(),
      getAllDietaries(),
      getAllIngredients(),
      getAllNutrients(),  
      getAllCountries()
    ]);

    renderUserHistory(historyRes.history, allDietaries, allIngredients, allNutrients, allCountries);
    bindDeleteButton();
    bindUpdateButton();
    
  } catch (err) {
    console.error(err);
  }
});
