export function renderFavoriteButton(isFavorite, ingredient_name, user_id) {
    const favoriteButtonContainer = document.getElementById("favorite-btn");
    if (isFavorite) {
        favoriteButtonContainer.innerHTML = `
            <form
                action="/api/favorites/delete/ingredient/${ingredient_name}/${user_id}"
                method="POST"
            >
                <button class="favorite-btn" type="submit">
                <i class="fa-solid fa-heart" style="color: #d72638"></i>
                </button>
            </form>
        `;
    } else {
        favoriteButtonContainer.innerHTML = `
            <form
                action="/api/favorites/add/ingredient/${ingredient_name}/${user_id}"
                method="POST"
            >
                <button class="favorite-btn" type="submit">
                <i class="fa-regular fa-heart"></i>
                </button>
            </form>
        `;
    }
}    

export function renderIngredientDetail(ingredient) {
    const ingredientKoreanNameElement = document.getElementById("ingredient_korean_name");
    const ingredientDetailElement = document.getElementById("ingredient_detail");
    
    ingredientKoreanNameElement.innerHTML = ingredient.korean_name;
    ingredientDetailElement.innerHTML = `<b>${ingredient.ingredient}</b>, ${ingredient.description}`;
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

export function renderNote(note, user_id, ingredient_name) {
    const notesContainer = document.getElementById("note-element");
    notesContainer.innerHTML = `
        <form action="/api/notes/add/${ingredient_name}/${user_id}" method="POST">
            <textarea name="note_content" placeholder="I had this at the shop across the street last Tuesday." class="memo-input">${ note.content ? note.content : '' }</textarea>
            <button type="submit" class="button save-button select-button">Save note</button>
        </form>
    `
}

export function renderNutrientContainer(ingredient, nutrients, user_id) {
    const ingredientFormContainer = document.getElementById("ingredient-form-container");
    ingredientFormContainer.innerHTML = `
        <div class="modal-content">
            <form
                method="POST"
                action="/api/ingredients/add_nutrient_review/${ingredient.ingredient}/${user_id}"
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