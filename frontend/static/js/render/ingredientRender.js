export function renderFavoriteButton(isFavorite, ingredient_name, user_id) {
    const favoriteButtonContainer = document.getElementById("favorite-btn");
    
    favoriteButtonContainer.innerHTML = `
    <button
      class="favorite-btn"
      data-dish="${ingredient_name}"
      data-user="${user_id}"
      data-favorite="${isFavorite}"
      aria-label="Toggle favorite"
    >
      <i class="${isFavorite ? "fa-solid" : "fa-regular"} fa-heart"
         style="${isFavorite ? "color:#d72638" : ""}">
      </i>
    </button>
  `;
}    

export function renderIngredientDetail(ingredient) {
    const ingredientKoreanNameElement = document.getElementById("ingredient_korean_name");
    const ingredientDetailElement = document.getElementById("ingredient_detail");
    
    ingredientKoreanNameElement.innerHTML = ingredient.korean_name;
    ingredientDetailElement.innerHTML = `<b>${ingredient.ingredient.replaceAll("_", " ")}</b>, ${ingredient.description}`;
}

export function renderDishes(dishes) {
    const dishesContainer = document.getElementById("dishes-element");
    if (!Array.isArray(dishes) || dishes.length === 0) {
        dishesContainer.innerHTML = "<p>No dishes information available for this ingredient.</p>";
        return;
    }
    dishesContainer.innerHTML = dishes.map(dish => `
        <a href="/dishes/${ dish.dish_name }" class="ingredient-tag">
            <b>${ dish.dish_name }</b>
        </a>
    `).join("");
}

export function renderNutrients(nutrients) {
    const nutrientsContainer = document.getElementById("nutrient-container");
    if (nutrients.length === 0) {
        nutrientsContainer.innerHTML = "<p>No nutrients information available for this ingredient.</p>";
    } else {
        nutrientsContainer.innerHTML = nutrients.map(nutrient => `
            <span class="dietary-tag">
                ${ nutrient.nutrient } ${ nutrient.count } (reviews)
            </span>
        `).join("");
    }
}

export function renderUserNote(note_content) {
    const noteContainer = document.getElementById("note-element");
    const noteTitle = document.getElementById("note-title");

    const existing = document.getElementById("note-status");
    if (existing) existing.remove();

    const statusIndicator = document.createElement("span");
    statusIndicator.id = "note-status";
    statusIndicator.style.cssText = `
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-left: 8px;
        background-color: #4CAF50;
    `;

    noteTitle.appendChild(statusIndicator);

    noteContainer.innerHTML = `
        <form>
            <textarea
                name="note_content"
                placeholder="I had this at the shop across the street last Tuesday."
                class="memo-input"
                id="note-textarea"
            >${note_content ?? ''}</textarea>
        </form>
    `;
}

export function renderNutrientContainer(ingredient, nutrients, user_id) {
    const ingredientFormContainer = document.getElementById("review-form-container");
    ingredientFormContainer.innerHTML = `
        <div class="modal-content">
            <form
                method="POST"
                action="/api/nutrients/${ingredient.ingredient}/${user_id}"
                onsubmit="disableButton()"
            >
                <label for="nutrient"><b>Nutrient:</b></label>
                <select id="nutrient" name="nutrient" required>
                    ${nutrients.sort().map(nutrient => `<option value="${nutrient.nutrient}">${nutrient.nutrient}</option>`).join('')}
                </select>
                <button type="submit" id="submitButton" class="button submit-button">
                    Submit nutrient review
                </button>
            </form>
        </div>
    `
}