import { getTopIngredients } from "../api/ingredientsApi.js";
import { getTopDishes } from "../api/dishesApi.js";
import { renderRankingList } from "../render/rankingRender.js";

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const [topIngredients, topDishes] = await Promise.all([
      getTopIngredients(),
      getTopDishes()
    ]);

    renderRankingList(
      document.getElementById("top-dishes"),
      topDishes,
      "dishes"
    );

    renderRankingList(
      document.getElementById("top-ingredients"),
      topIngredients,
      "ingredients"
    );

  } catch (err) {
    console.error(err);
  }
});
