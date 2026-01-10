import { getAllDishes } from "../api/dishesApi.js";
import { getFavoriteDishes } from "../api/favoritesApi.js";
import { getCurrentUser } from "../api/usersApi.js";
import { renderAllDishes } from "../render/foodListRender.js";
import { bindFilterEvents, setupFoodListEvents, filterOptionEvents } from "../events/filterEvents.js";
import { renderDietaries } from "../render/dietariesRender.js";
import { renderIngredients } from "../render/IngredientsRender.js";
import { getAllDietaries } from "../api/dietariesApi.js";
import { getAllIngredients } from "../api/ingredientsApi.js";

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const user = await getCurrentUser();
    const [allDishes, favoriteDishes, allIngredients, allDietaries] = await Promise.all([
      getAllDishes(),
      user?.user ? getFavoriteDishes(user.user.google_id) : Promise.resolve([]),
      getAllIngredients(),
      getAllDietaries()
    ]);

    renderAllDishes(allDishes, favoriteDishes);
    renderDietaries(allDietaries);
    renderIngredients(allIngredients);

    setupFoodListEvents();
    bindFilterEvents();
    filterOptionEvents(favoriteDishes);

  } catch (err) {
    console.error(err);
  }
});
