import { getTotalReviews } from "../api/reviewsApi.js";
import { getAllDishes } from "../api/dishesApi.js";
import { getAllIngredients } from "../api/ingredientsApi.js";
import { getCurrentUser, getTotalUsers } from "../api/usersApi.js";
import { bindSearchEvents } from "../events/searchEvents.js";

document.addEventListener("DOMContentLoaded", async () => {
  const searchInput = document.getElementById("search-input");
  const searchResults = document.getElementById("search-results");

  const searchItems = [];

  try {
    const [
      totalReviews,
      dishes,
      ingredients,
      user,
      totalUsers
    ] = await Promise.all([
      getTotalReviews(),
      getAllDishes(),
      getAllIngredients(),
      getCurrentUser(),
      getTotalUsers()
    ]);

    document.getElementById("total_users").textContent =
      totalUsers.total_users;
    document.getElementById("total_reviews").textContent =
      totalReviews.total_reviews;

    dishes.forEach(dish => {
      searchItems.push({
        name: dish.dish_name,
        koreanName: dish.korean_name,
        type: "dish",
        url: `/dishes/${dish.dish_name}`
      });
    });

    ingredients.forEach(ingredient => {
      searchItems.push({
        name: ingredient.ingredient,
        koreanName: ingredient.korean_name,
        type: "ingredient",
        url: `/ingredients/${ingredient.ingredient}`
      });
    });

    bindSearchEvents(searchInput, searchResults, searchItems);

  } catch (err) {
    console.error(err);
  }
});
