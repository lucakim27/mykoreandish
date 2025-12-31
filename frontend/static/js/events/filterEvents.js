import { getDishesByDietary, getDishesByIngredient, getDishesByAspect } from "../api/dishesApi.js";
import { renderAllDishes } from "../render/foodListRender.js";

export function filterDishes() {
  const input = document.getElementById("search-input").value.toLowerCase();
  const foodItems = document.querySelectorAll(".food-item");

  foodItems.forEach(item => {
    const dishName = item.querySelector("h3").textContent.toLowerCase();
    const description = item.querySelector("p").textContent.toLowerCase();

    item.style.display =
      dishName.includes(input) || description.includes(input)
        ? ""
        : "none";
  });
}

export function showFilterOptions() {
  const optionIds = [
    "ingredient",
    "dietary",
    "spiciness",
    "sweetness",
    "sourness",
    "texture",
    "temperature",
    "healthiness",
    "rating"
  ];

  optionIds.forEach(id => {
    document.getElementById(`${id}-options`).style.display = "none";
  });

  const selected = optionIds.find(
    id => document.getElementById(`filter-${id}`).checked
  );
  
  if (selected) {
    document.getElementById(`${selected}-options`).style.display = "block";
  }
}

export function toggleFilterOptions() {
  const container = document.querySelector(".filter-container");
  container.style.display =
    container.style.display === "none" ? "block" : "none";
}

export function bindFilterEvents() {
  document
    .querySelectorAll('input[name="filter"]')
    .forEach(input => {
      input.addEventListener("change", showFilterOptions);
    });
}

export function filterOptionEvents(favoriteDishes) {
    const filterByOption = document.querySelectorAll(".filter-options select");
    filterByOption.forEach(select => {
        select.addEventListener("change", async () => {
            if (select.value === "") {
                return;
            }
            if (select.name == "dietary") {
                const [FilteredDishes] = await Promise.all([
                  getDishesByDietary(select.value)
                ]);
                renderAllDishes(FilteredDishes, favoriteDishes);
                return;
            } else if (select.name == "ingredient") {
                const [FilteredDishes] = await Promise.all([
                  getDishesByIngredient(select.value)
                ]);
                renderAllDishes(FilteredDishes, favoriteDishes);
                return;
            } else {
                const [FilteredDishes] = await Promise.all([
                  getDishesByAspect(select.name, select.value)
                ]);
                renderAllDishes(FilteredDishes, favoriteDishes);
                return;
            }
        });
    });
}

export function setupFoodListEvents() {
    const searchInput = document.getElementById("search-input");
    if (searchInput) {
        searchInput.addEventListener("input", filterDishes);
    }

    const filterToggleBtn = document.getElementById("filter-toggle-btn");
    if (filterToggleBtn) {
        filterToggleBtn.addEventListener("click", toggleFilterOptions);
    }
}
