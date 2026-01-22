export function renderDishDetails(dish) {
    const dishKoreanNameElement = document.getElementById("dish_korean_name");
    const dishDetailElement = document.getElementById("dish_detail");
    
    dishKoreanNameElement.innerHTML = dish.korean_name;
    dishDetailElement.innerHTML = `<b>${dish.dish_name}</b>, ${dish.description}`;
}

export function renderDietaries(dietaries) {
    const dietaryContainer = document.getElementById("dietary-element");
    if (!Array.isArray(dietaries) || dietaries.length === 0) {
        dietaryContainer.innerHTML = "<p>No dietary information available for this dish.</p>";
        return;
    }
    dietaryContainer.innerHTML = dietaries.map(dietary => `
        <div style="display:inline;" class="dietary-tag">
            <input type="hidden" name="dietary" value="${dietary.dietary_name}">
            <button class="ingredient-tag" style="all:unset; display:inline;">
                ${dietary.dietary_name.replaceAll("_", " ")}
                (${dietary.count} ${dietary.count === 1 ? 'review' : 'reviews'})
            </button>
        </div>
    `).join("");
}

export function renderIngredients(ingredients) {
    const ingredientContainer = document.getElementById("ingredient-element");
    if (!Array.isArray(ingredients) || ingredients.length === 0) {
        ingredientContainer.innerHTML = "<p>No ingredient information available for this dish.</p>";
        return;
    }
    ingredientContainer.innerHTML = ingredients.map(ingredient => `
        <a href="/ingredients/${ingredient.ingredient_name}" class="ingredient-tag">
            <b>${ingredient.ingredient_name.replaceAll("_", " ")}</b>
            (${ingredient.count} ${ingredient.count === 1 ? 'review' : 'reviews'})
        </a>
    `).join("");
}

export function renderPriceInfo(priceInfo, countries) {
  const priceContainer = document.getElementById("price-details");

  if (!Array.isArray(priceInfo) || priceInfo.length === 0) {
    priceContainer.innerHTML = "<p style='margin-top: 15px;'>No price information available for this dish.</p>";
    return;
  }

  const sorted = [...priceInfo].sort(
    (a, b) => new Date(b.timestamp) - new Date(a.timestamp)
  );

  priceContainer.innerHTML = `
    <ul style="margin-bottom: 15px;">
      ${sorted.map(entry => `
        <li style="display: flex; justify-content: space-between; align-items: center;">
          <span>${entry.price} ${countries[entry.country]} in ${entry.country}</span>
          <span style="color: gray; font-size: 0.95em;">
            ${entry.timestamp}
          </span>
        </li>
      `).join("")}
    </ul>
  `;
}

export function renderTastes(aggregates) {
    const container = document.getElementById("taste-element");
    if (!container) return;

    const total = aggregates && aggregates.total_reviews ? aggregates.total_reviews : 0;
    const totalText = total === 0 ? '0 Review' : total === 1 ? '1 Review' : `${total} Reviews`;

    const aspects = {
        'Rating':    { value: aggregates?.rating ?? null,      color: '#FFD700' },
        'Texture':   { value: aggregates?.texture ?? null,     color: '#8B4513' },
        'Sourness':  { value: aggregates?.sourness ?? null,    color: '#FFD700' },
        'Spiciness': { value: aggregates?.spiciness ?? null,   color: '#FF4500' },
        'Sweetness': { value: aggregates?.sweetness ?? null,   color: '#FF69B4' },
        'Healthiness': { value: aggregates?.healthiness ?? null, color: '#32CD32' },
        'Temperature': { value: aggregates?.temperature ?? null, color: '#FF6347' }
    };

    let html = `<table class="tastes-table"><thead><tr><th>Total</th><th>${totalText}</th></tr></thead><tbody>`;

    for (const [aspect, data] of Object.entries(aspects)) {
        html += `<tr>
                    <th>
                        <div class="taste-header">
                            <span class="taste-label">${aspect}</span>
                        </div>
                    </th>
                    <td>`;

        if (data.value !== null && data.value !== undefined) {
            html += `<div class="taste-visual-display"><div class="taste-bars">`;
            for (let i = 1; i <= 5; i++) {
                const opacity = data.value >= i ? 1 : (data.value > i - 1 ? (data.value - (i - 1)) : 0.2);
                html += `<div class="taste-bar" style="background-color: ${data.color}; opacity: ${opacity};"></div>`;
            }
            html += `</div></div>`;
        } else {
            html += `<div class="taste-visual-display"><div class="taste-bars">`;
            for (let i = 1; i <= 5; i++) {
                html += `<div class="taste-bar" style="background-color: ${data.color}; opacity: 0.2;"></div>`;
            }
            html += `</div></div>`;
        }

        html += `</td></tr>`;
    }

    html += `</tbody></table>`;
    container.innerHTML = html;
}

export function renderSimilarDishes(similarDishes) {
    const similarDishesContainer = document.getElementById("similar-dishes-element");
    if (!Array.isArray(similarDishes) || similarDishes.length === 0) {
        similarDishesContainer.innerHTML = "<p>No similar dishes found for this dish.</p>";
        return;
    }
    similarDishesContainer.innerHTML = similarDishes.map(dish => `
        <a href="/dishes/${dish.dish_name}" class="similar-dish-card">
            <strong>${dish.korean_name}</strong>
            <small>${dish.dish_name}</small>
            ${dish.shared_ingredients ? `<div class="shared">Shares: ${dish.shared_ingredients.join(', ')}</div>` : ''}
        </a>
    `).join("");
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


export function renderReviewFormContainer(dish_name, dietaries, ingredients, countries, user_id) {
    const reviewFormContainer = document.getElementById("review-form-container");
    reviewFormContainer.innerHTML = `
        <div class="modal-content">
            <div class="review-type-segmented">
                <button type="button" id="seg-dietary" class="segment-btn active" onclick="selectReviewType('dietary')">Dietary</button>
                <button type="button" id="seg-ingredient" class="segment-btn" onclick="selectReviewType('ingredient')">Ingredient</button>
                <button type="button" id="seg-taste" class="segment-btn" onclick="selectReviewType('taste')">Taste</button>
                <button type="button" id="seg-price" class="segment-btn" onclick="selectReviewType('price')">Price</button>
            </div>
            
            <form id="dietaryForm">
                <label for="dietary" style="color: #2c3e50"><b>Dietary:</b></label>
                <select id="dietary" name="dietary" required>
                    ${dietaries.map(dietary => `<option value="${dietary}">${dietary}</option>`).join('')}
                </select>
                <button
                    type="button"
                    id="submitDietaryButton"
                    data-user="${user_id}"
                    data-dish="${dish_name}"
                    data-type="dietary"
                    class="button submit-button add-btn"
                    aria-label="add dietary review"
                >
                    Submit dietary review
                </button>
            </form>
            
            <form id="ingredientForm" style="display:none;">
                <label for="ingredient"><b>Ingredient:</b></label>
                <select id="ingredient" name="ingredient" required>
                    ${ingredients.map(ingredient => `<option value="${ingredient.ingredient}">${ingredient.ingredient.replaceAll("_", " ")}</option>`).join('')}
                </select>
                <button
                    type="button"
                    id="submitIngredientButton"
                    data-user="${user_id}"
                    data-dish="${dish_name}"
                    data-type="ingredient"
                    class="button submit-button add-btn"
                    aria-label="add ingredient review"
                >
                    Submit ingredient review
                </button>
            </form>
            
            <form id="tasteForm"style="display:none;">
                <div class="input-group">
                    <label for="spiciness"><b>Spiciness:</b></label>
                    <select id="spiciness" name="spiciness" required>
                        <option value="0" selected>Not spicy at all</option>
                        <option value="1">A little spicy</option>
                        <option value="2">Mildly spicy</option>
                        <option value="3">Moderately spicy</option>
                        <option value="4">Very spicy</option>
                        <option value="5">Extremely spicy</option>
                    </select>
                    <label for="sweetness"><b>Sweetness:</b></label>
                    <select id="sweetness" name="sweetness" required>
                        <option value="0" selected>Not sweet at all</option>
                        <option value="1">Barely sweet</option>
                        <option value="2">Mildly sweet</option>
                        <option value="3">Moderately sweet</option>
                        <option value="4">Very sweet</option>
                        <option value="5">Extremely sweet</option>
                    </select>
                    <label for="sourness"><b>Sourness:</b></label>
                    <select id="sourness" name="sourness" required>
                        <option value="0" selected>Not sour at all</option>
                        <option value="1">Slightly sour</option>
                        <option value="2">Moderately sour</option>
                        <option value="3">Quite sour</option>
                        <option value="4">Very sour</option>
                        <option value="5">Extremely sour</option>
                    </select>
                    <label for="texture"><b>Texture:</b></label>
                    <select id="texture" name="texture" required>
                        <option value="0" selected>Very Soft</option>
                        <option value="1">Soft</option>
                        <option value="2">Slightly Soft</option>
                        <option value="3">Moderate</option>
                        <option value="4">Slightly Hard</option>
                        <option value="5">Hard</option>
                    </select>
                    <label for="temperature"><b>Temperature:</b></label>
                    <select id="temperature" name="temperature" required>
                        <option value="0" selected>Cold</option>
                        <option value="1">Cool</option>
                        <option value="2">Slightly Cool</option>
                        <option value="3">Warm</option>
                        <option value="4">Hot</option>
                        <option value="5">Very Hot</option>
                    </select>
                    <label for="healthiness"><b>Healthiness:</b></label>
                    <select id="healthiness" name="healthiness" required>
                        <option value="0" selected>Not healthy at all</option>
                        <option value="1">Unhealthy</option>
                        <option value="2">Below average</option>
                        <option value="3">Moderately healthy</option>
                        <option value="4">Healthy</option>
                        <option value="5">Very healthy</option>
                    </select>
                    <label for="rating"><b>Rating:</b></label>
                    <select id="rating" name="rating" required>
                        <option value="0" selected>Terrible</option>
                        <option value="1">Bad</option>
                        <option value="2">Below Average</option>
                        <option value="3">Average</option>
                        <option value="4">Good</option>
                        <option value="5">Excellent</option>
                    </select>
                </div>
                <button
                    type="button"
                    id="submitTasteButton"
                    data-user="${user_id}"
                    data-dish="${dish_name}"
                    data-type="taste"
                    class="button submit-button add-btn"
                    aria-label="add taste review"
                >
                    Submit taste review
                </button>                
            </form>

            <form id="priceForm" style="display:none;">
                <div class="input-group">
                    <label for="country"><b>Country:</b></label>
                    <select id="country" name="country" required>
                        ${Object.keys(countries).map(country => `<option value="${country}">${country}</option>`).join('')}
                    </select><br>
                    <label for="price"><b>Price:</b></label><br>
                    <input id="price" type="number" step="0.01" min="0" placeholder="34.50" name="price" required>
                </div>
                <button
                    type="button"
                    data-user="${user_id}"
                    data-dish="${dish_name}"
                    data-type="price"
                    class="button submit-button add-btn"
                    aria-label="add price review"
                >
                    Submit price review
                </button>         
            </form>
        </div>
    `;
}

export function renderFavoriteButton(isFavorite, dish_name, user_id) {
  const container = document.getElementById("favorite-btn");

  container.innerHTML = `
    <button
      class="favorite-btn"
      data-dish="${dish_name}"
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

export function initFavoriteButton(isFavorite) {
  const btn = document.querySelector(".favorite-btn");
  const icon = btn.querySelector("i");

  btn.dataset.favorite = isFavorite;

  if (isFavorite) {
    icon.classList.remove("fa-regular");
    icon.classList.add("fa-solid");
    icon.style.color = "#d72638";
  }
}