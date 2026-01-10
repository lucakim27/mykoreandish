import { getCurrentUser } from "../api/usersApi.js";
import { getDishInstance, getDishAggregates, getSimilarDishes } from "../api/dishesApi.js";
import { isDishFavorite } from "../api/favoritesApi.js";
import { getAllDietaries } from "../api/dietariesApi.js";
import { getAllIngredients } from "../api/ingredientsApi.js";
import { getPriceInfo, getAllLocations } from "../api/pricesApi.js";
import { getNote } from "../api/notesApi.js";
import { getDishOrIngredientName } from "../utils/url.js";
import { initFavoriteButton, renderDishDetails, renderDietaries, renderTastes, renderReviewFormContainer, renderUserNote, renderSimilarDishes, renderFavoriteButton, renderPriceInfo, renderIngredients } from "../render/foodRender.js";
import { bindFavoriteButton } from "../events/buttonEvents.js";
import { textareaEventBinding } from "../events/textareaEvent.js";

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const user = await getCurrentUser();
    const dish = await getDishInstance(getDishOrIngredientName());
    const [
        aggregates,
        dietaries,
        ingredients,
        favorite,
        similarDishes,
        locations,
        priceInfo,
        note
    ] = await Promise.all([
      getDishAggregates(dish.dish_name),
      getAllDietaries(),
      getAllIngredients(),
      user?.user ? isDishFavorite(dish.dish_name, user.user.google_id) : Promise.resolve([]),
      getSimilarDishes(dish.dish_name),
      getAllLocations(),
      getPriceInfo(dish.dish_name),
      user?.user ? getNote(dish.dish_name, user.user.google_id) : Promise.resolve([])
    ]);

    renderDishDetails(dish);
    const dietaryMap = aggregates?.dietary_distribution ?? {};
    const dietaryArray = Object.entries(dietaryMap).map(
      ([dietary_name, count]) => ({ dietary_name, count })
    );
    renderDietaries(dietaryArray);
    const ingredientMap = aggregates?.ingredient_distribution ?? {};
    const ingredientArray = Object.entries(ingredientMap).map(
      ([ingredient_name, count]) => ({ ingredient_name, count })
    );
    renderIngredients(ingredientArray);
    renderFavoriteButton(favorite.is_dish_favorite, dish.dish_name, user?.user ? user.user.google_id : null);
    renderSimilarDishes(similarDishes);
    renderPriceInfo(priceInfo);
    renderTastes(aggregates);
    renderUserNote(note.content);
    renderReviewFormContainer(dish.dish_name, dietaries, ingredients, locations, user?.user ? user.user.google_id : null);
    initFavoriteButton(favorite.is_dish_favorite);
    bindFavoriteButton();
    textareaEventBinding(dish.dish_name, user?.user ? user.user.google_id : null);

  } catch (err) {
    console.error(err);
  }
});
