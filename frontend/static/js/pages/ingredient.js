import { 
    renderNutrientContainer,
    renderNote,
    renderNutrients,
    renderDishes,
    renderIngredientDetail,
    renderFavoriteButton
} from "../render/ingredientRender.js";
import { getCurrentUser } from "../api/usersApi.js";
import { getIngredientInstance, isIngredientFavorite } from "../api/ingredientsApi.js";
import { getDishesByIngredient } from "../api/dishesApi.js";
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
        user?.user ? isIngredientFavorite(ingredient.ingredient, user.user.google_id) : Promise.resolve([]),
        user?.user ? getNote(ingredient.ingredient, user.user.google_id) : Promise.resolve([]),
        getIngredientNutrients(ingredient.ingredient)
    ]);

    renderNutrientContainer(ingredient, AllNutrients, user?.user ? user.user.google_id : null)
    renderNote(note, user?.user ? user.user.google_id : null, ingredient.ingredient)
    renderNutrients(nutrients)
    renderDishes(dishes)
    renderIngredientDetail(ingredient)
    renderFavoriteButton(isFavorite.is_ingredient_favorite, ingredient.ingredient, user?.user ? user.user.google_id : null)
    
  } catch (err) {
    console.error(err);
  }
});
