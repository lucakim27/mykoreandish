import { 
    renderNutrientContainer,
    renderUserNote,
    renderNutrients,
    renderDishes,
    renderIngredientDetail,
    renderFavoriteButton
} from "../render/ingredientRender.js";
import { getCurrentUser } from "../api/usersApi.js";
import { getIngredientInstance } from "../api/ingredientsApi.js";
import { getDishesByIngredient } from "../api/dishesApi.js";
import { getDishOrIngredientName } from "../utils/url.js";
import { getAllNutrients, getIngredientNutrients } from "../api/nutrientsApi.js";
import { getNote } from "../api/notesApi.js";
import { bindFavoriteButton, bindAddButton } from "../events/buttonEvents.js";
import { isFavorite } from "../api/favoritesApi.js";
import { textareaEventBinding } from "../events/textareaEvent.js";
import { getAllCountries } from "../api/countriesApi.js";

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const user = await getCurrentUser();
    const ingredient = await getIngredientInstance(getDishOrIngredientName());
    const [
        dishes,
        AllNutrients,
        favoriteResult,
        note,
        nutrients,
        countries
    ] = await Promise.all([
        getDishesByIngredient(ingredient.ingredient),
        getAllNutrients(),
        user ? isFavorite(ingredient.ingredient, user.google_id) : Promise.resolve([]),
        user ? getNote(ingredient.ingredient) : Promise.resolve([]),
        getIngredientNutrients(ingredient.ingredient),
        getAllCountries()
    ]);

    renderNutrientContainer(ingredient, AllNutrients, user ? user.google_id : null)
    renderUserNote(note.content);
    renderNutrients(nutrients)
    renderDishes(dishes)
    renderIngredientDetail(ingredient)
    renderFavoriteButton(favoriteResult.is_favorite, ingredient.ingredient, user ? user.google_id : null)
    bindFavoriteButton();
    textareaEventBinding(ingredient.ingredient, user ? user.google_id : null);
    bindAddButton(countries)

  } catch (err) {
    console.error(err);
  }
});
