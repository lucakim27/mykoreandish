import { 
    renderNutrientContainer,
    renderNote,
    renderNutrients,
    renderDishes,
    renderIngredientDetail,
    renderFavoriteButton
} from "../render/ingredientRender.js";
import { getCurrentUser } from "../api/usersApi.js";
import { 
    getIngredientInstance,
    getDishesByIngredient,
    isIngredientFavorite
} from "../api/ingredientsApi.js";
import { getDishOrIngredientName } from "../utils/url.js";
import { getAllNutrients, getIngredientNutrients } from "../api/nutrientsApi.js";
import { getNote } from "../api/notesApi.js";

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const user = await getCurrentUser();
    const ingredient = await getIngredientInstance(getDishOrIngredientName());
    const [
        dishes,
        AllNutrients,
        isFavorite,
        note,
        nutrients
    ] = await Promise.all([
        getDishesByIngredient(ingredient.ingredient),
        getAllNutrients(),
        isIngredientFavorite(ingredient.ingredient, user.user.google_id),
        getNote(ingredient.ingredient, user.user.google_id),
        getIngredientNutrients(ingredient.ingredient)
    ]);

    renderNutrientContainer(ingredient, AllNutrients, user.user.google_id)
    renderNote(note, user.user.google_id, ingredient.ingredient)
    renderNutrients(nutrients)
    renderDishes(dishes)
    renderIngredientDetail(ingredient)
    renderFavoriteButton(isFavorite.is_ingredient_favorite, ingredient.ingredient, user.user.google_id)
    
  } catch (err) {
    console.error(err);
  }
});
