import { showToast } from "../utils/toaster.js";
import { deleteHistoryByType } from "../api/historyApi.js";
import { getDishAggregates } from "../api/dishesApi.js";
import { renderDietaries } from "../render/foodRender.js";
import { renderIngredients } from "../render/foodRender.js";
import { getPriceInfo } from "../api/pricesApi.js";
import { renderPriceInfo } from "../render/foodRender.js";
import { renderTastes } from "../render/foodRender.js";

export function bindDeleteButton() {
  document.addEventListener("click", async (event) => {
    const button = event.target.closest(".delete-btn");
    if (!button || button.disabled) return;

    const { historyId, type } = button.dataset;
    button.disabled = true;

    try {
      await deleteHistoryByType(type, historyId);
      showToast("History deleted successfully", "success");
      button.closest(".history-item")?.remove();
    } catch (err) {
      showToast("Failed to delete history", "error");
      console.error(err);
      button.disabled = false;
    }
  });
}

export function bindFavoriteButton() {
  document.addEventListener("click", async (e) => {
    const btn = e.target.closest(".favorite-btn");
    if (!btn) return;

    const { dish, user, favorite } = btn.dataset;
    const isFavorite = favorite === "true";

    const url = `/api/favorites/${dish}/${user}`;
    const method = isFavorite ? "DELETE" : "POST";

    btn.disabled = true;

    const res = await fetch(url, { method });

    if (!res.ok) {
      showToast("Failed to update favorite status", "error");
      btn.disabled = false;
      return;
    } else {
      showToast(`Dish ${isFavorite ? "removed from" : "added to"} favorites`, "success");
      btn.dataset.favorite = (!isFavorite).toString();
      const icon = btn.querySelector("i");
      icon.classList.toggle("fa-solid", !isFavorite);
      icon.classList.toggle("fa-regular", isFavorite);
      icon.style.color = !isFavorite ? "#d72638" : "";
      btn.disabled = false;
    }

  });
}

export function bindAddButton(countries) {
  document.addEventListener("click", async (e) => {
    const btn = e.target.closest(".add-btn");
    if (!btn) return;

    const dish_name = btn.dataset.dish;
    const type = btn.dataset.type;

    let api = null;
    let content = null;
    if (type == "dietary") {
      api = `/api/dietaries/${dish_name}`;
      content = { dietary: document.getElementById("dietary").value };
    } else if (type == "ingredient") {
      api = `/api/ingredients/${dish_name}`;
      content = { ingredient: document.getElementById("ingredient").value };
    } else if (type == "price") {
      api = `/api/prices/${dish_name}`;
      content = { 
        price: document.getElementById("price").value,
        country: document.getElementById("country").value
      };
    } else if (type == "taste") {
      api = `/api/tastes/${dish_name}`;
      const spiciness = document.getElementById("spiciness").value;
      const sweetness = document.getElementById("sweetness").value;
      const temperature = document.getElementById("temperature").value;
      const healthiness = document.getElementById("healthiness").value;
      const sourness = document.getElementById("sourness").value;
      const texture = document.getElementById("texture").value;
      const rating = document.getElementById("rating").value;
      content = {
        spiciness: spiciness,
        sweetness: sweetness,
        temperature: temperature,
        healthiness: healthiness,
        sourness: sourness,
        texture: texture,
        rating: rating
      };
    }

    btn.disabled = true;

    try {
      const res = await fetch(
        api,
        {
          method: "POST",
          body: JSON.stringify(content),
          headers: {
            "Content-Type": "application/json"
          },
          credentials: "include",
        }
      );

      if (!res.ok) {
        throw new Error(`Request failed: ${res.status}`);
      }

      if (type === "dietary") {
        const aggregates = await getDishAggregates(dish_name);
        const dietaryMap = aggregates?.dietary_distribution ?? {};
        const dietaryArray = Object.entries(dietaryMap).map(
          ([dietary_name, count]) => ({ dietary_name, count })
        );
        renderDietaries(dietaryArray);
      } else if (type === "ingredient") {
        const aggregates = await getDishAggregates(dish_name);
        const ingredientMap = aggregates?.ingredient_distribution ?? {};
        const ingredientArray = Object.entries(ingredientMap).map(
          ([ingredient_name, count]) => ({ ingredient_name, count })
        );
        renderIngredients(ingredientArray);
      } else if (type === "price") {
        const priceInfo = await getPriceInfo(dish_name);
        renderPriceInfo(priceInfo, countries)
      } else if (type === "taste") {
        const aggregates = await getDishAggregates(dish_name);
        renderTastes(aggregates);
      }
      btn.textContent = "Saved";
      showToast("Review added successfully", "success");
    } catch (err) {
      console.error(err);
      btn.disabled = false;
      showToast("Failed to add review", "error");
    }
  });
}