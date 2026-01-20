import { resolveHistoryType } from "../utils/historyType.js";

export function renderUserHistory(history, meta) {
  const container = document.getElementById("price_history");
  container.innerHTML = "";

  if (!history || history.length === 0) {
    container.innerHTML = "<p>No history available.</p>";
    return;
  }

  history
    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
    .forEach(item => {
      const li = renderHistoryItem(item, meta);
      container.appendChild(li);
    });
}

export function renderHistoryItem(item, meta) {
  const li = document.createElement("li");

  const type = resolveHistoryType(item);

  li.classList.add("history-item");
  li.dataset.historyId = item.id;

  li.innerHTML = `
    <div class="price-point">
      ${renderDeleteButton(item, type)}
      <span class="price">
        ${item.nutrient ? item.ingredient : item.dish_name}
      </span>
      <span class="timestamp">(${item.timestamp})</span>
    </div>
    <br />
    ${renderUpdateSection(item, meta)}
  `;

  return li;
}

export function renderDeleteButton(item, type) {
  return `
    <button
      class="close delete-btn"
      data-history-id="${item.id}"
      data-type="${type}"
      aria-label="Delete"
    >
      &times;
    </button>
  `;
}

export function renderUpdateSection(item, meta) {
  if (item.spiciness !== undefined) {
    return renderRatingForm(item);
  } else if (item.dietary !== undefined) {
    return renderDietaryForm(item, meta);
  } else if (item.ingredient && item.dish_name) {
    return renderIngredientForm(item, meta);
  } else if (item.nutrient !== undefined) {
    return renderNutrientForm(item, meta);
  } else if (item.price !== undefined) {
    return renderPriceForm(item, meta);
  }
  return "";
}

function renderRatingForm(item) {
  return `
    <form method="POST" action="/api/tastes/" style="display:inline;">
      <input type="hidden" name="history_id" value="${item.id}">
      <label for="spiciness"><b>Spiciness:</b></label>
      <select id="spiciness-${item.id}" name="spiciness">
        <option value="0" ${item.spiciness === 0 ? "selected" : ""}>Not at all spicy</option>
        <option value="1" ${item.spiciness === 1 ? "selected" : ""}>A little spicy</option>
        <option value="2" ${item.spiciness === 2 ? "selected" : ""}>Mildly spicy</option>
        <option value="3" ${item.spiciness === 3 ? "selected" : ""}>Moderately spicy</option>
        <option value="4" ${item.spiciness === 4 ? "selected" : ""}>Very spicy</option>
        <option value="5" ${item.spiciness === 5 ? "selected" : ""}>Extremely spicy</option>
      </select>
      <label for="sourness"><b>Sourness:</b></label>
      <select id="sourness-${item.id}" name="sourness">
        <option value="0" ${item.sourness === 0 ? "selected" : ""}>Not at all sour</option>
        <option value="1" ${item.sourness === 1 ? "selected" : ""}>A little sour</option>
        <option value="2" ${item.sourness === 2 ? "selected" : ""}>Mildly sour</option>
        <option value="3" ${item.sourness === 3 ? "selected" : ""}>Moderately sour</option>
        <option value="4" ${item.sourness === 4 ? "selected" : ""}>Very sour</option>
        <option value="5" ${item.sourness === 5 ? "selected" : ""}>Extremely sour</option>
      </select>
      <label for="healthiness"><b>Healthiness:</b></label>
      <select id="healthiness-${item.id}" name="healthiness">
        <option value="0" ${item.healthiness === 0 ? "selected" : ""}>Not at all healthy</option>
        <option value="1" ${item.healthiness === 1 ? "selected" : ""}>A little healthy</option>
        <option value="2" ${item.healthiness === 2 ? "selected" : ""}>Mildly healthy</option>
        <option value="3" ${item.healthiness === 3 ? "selected" : ""}>Moderately healthy</option>
        <option value="4" ${item.healthiness === 4 ? "selected" : ""}>Very healthy</option>
        <option value="5" ${item.healthiness === 5 ? "selected" : ""}>Extremely healthy</option>
      </select>
      <label for="temperature"><b>Temperature:</b></label>
      <select id="temperature-${item.id}" name="temperature">
        <option value="0" ${item.temperature === 0 ? "selected" : ""}>Cold</option>
        <option value="1" ${item.temperature === 1 ? "selected" : ""}>Cool</option>
        <option value="2" ${item.temperature === 2 ? "selected" : ""}>Room Temperature</option>
        <option value="3" ${item.temperature === 3 ? "selected" : ""}>Warm</option>
        <option value="4" ${item.temperature === 4 ? "selected" : ""}>Hot</option>
        <option value="5" ${item.temperature === 5 ? "selected" : ""}>Very Hot</option>
      </select>
      <label for="texture"><b>Texture:</b></label>
      <select id="texture-${item.id}" name="texture">
        <option value="0" ${item.texture === 0 ? "selected" : ""}>Smooth</option>
        <option value="1" ${item.texture === 1 ? "selected" : ""}>Crumbly</option>
        <option value="2" ${item.texture === 2 ? "selected" : ""}>Chewy</option>
        <option value="3" ${item.texture === 3 ? "selected" : ""}>Crispy</option>
        <option value="4" ${item.texture === 4 ? "selected" : ""}>Hard</option>
        <option value="5" ${item.texture === 5 ? "selected" : ""}>Very Hard</option>
      </select>
      <label for="sweetness"><b>Sweetness:</b></label>
      <select id="sweetness-${item.id}" name="sweetness">
        <option value="0" ${item.sweetness === 0 ? "selected" : ""}>Not sweet at all</option>
        <option value="1" ${item.sweetness === 1 ? "selected" : ""}>Barely sweet</option>
        <option value="2" ${item.sweetness === 2 ? "selected" : ""}>Mildly sweet</option>
        <option value="3" ${item.sweetness === 3 ? "selected" : ""}>Moderately sweet</option>
        <option value="4" ${item.sweetness === 4 ? "selected" : ""}>Very sweet</option>
        <option value="5" ${item.sweetness === 5 ? "selected" : ""}>Extremely sweet</option>
      </select>
      <label for="rating"><b>Rating:</b></label>
      <select id="rating-${item.id}" name="rating">
        <option value="0" ${item.rating === 0 ? "selected" : ""}>Terrible</option>
        <option value="1" ${item.rating === 1 ? "selected" : ""}>Bad</option>
        <option value="2" ${item.rating === 2 ? "selected" : ""}>Below Average</option>
        <option value="3" ${item.rating === 3 ? "selected" : ""}>Average</option>
        <option value="4" ${item.rating === 4 ? "selected" : ""}>Good</option>
        <option value="5" ${item.rating === 5 ? "selected" : ""}>Excellent</option>
      </select>
      <button type="submit" class="button update-button">Update</button>
    </form>
  `;
}

function renderDietaryForm(item, meta) {
  const options = meta.dietaries.map(d => `
    <option value="${d}" ${item.dietary === d ? "selected" : ""}>${d}</option>
  `).join("");
  return `
    <form method="POST" action="/api/dietaries/" style="display:inline;">
      <input type="hidden" name="history_id" value="${item.id}">
      <label for="dietary"><b>Dietary:</b></label>
      <select class="form-select" id="dietary" name="dietary">${options}</select>
      <button type="submit" class="button update-button">Update</button>
    </form>
  `;
}

function renderIngredientForm(item, meta) {
  const options = meta.ingredients.map(i => `
    <option value="${i.ingredient}" ${item.ingredient === i.ingredient ? "selected" : ""}>${i.ingredient}</option>
  `).join("");
  return `
    <form method="POST" action="/api/ingredients/${item.id}/${item.ingredient}/${item.dish_name}" style="display:inline;">
      <input type="hidden" name="history_id" value="${item.id}">
      <label for="ingredient"><b>Ingredient:</b></label>
      <select class="form-select" id="ingredient" name="ingredient">${options}</select>
      <button type="submit" class="button update-button">Update</button>
    </form>
  `;
}

function renderNutrientForm(item, meta) {
  const options = meta.nutrients.map(n => `
    <option value="${n.nutrient}" ${item.nutrient === n.nutrient ? "selected" : ""}>${n.nutrient}</option>
  `).join("");
  return `
    <form method="POST" action="/api/nutrients/update_nutrient_review" style="display:inline;">
      <input type="hidden" name="history_id" value="${item.id}">
      <label for="nutrient"><b>Nutrient:</b></label>
      <select class="form-select" id="nutrient" name="nutrient">${options}</select>
      <button type="submit" class="button update-button">Update</button>
    </form>
  `;
}

function renderPriceForm(item, meta) {
  const countryOptions = Object.keys(meta.countries)
  .sort()
  .map(c => `
    <option value="${c}" ${item.country === c ? "selected" : ""}>${c}</option>
  `)
  .join("");
  return `
    <form method="POST" action="/api/prices/update_price_review" style="display:inline;">
      <input type="hidden" name="history_id" value="${item.id}">
      <label for="country"><b>Country:</b></label>
      <select class="form-select" id="historyCountry-${item.id}" name="country">${countryOptions}</select>
      <label for="price"><b>Price:</b></label>
      <input type="number" step="0.01" min="0" placeholder="34.50" name="price" value="${item.price}" required>
      <button type="submit" class="button update-button">Update</button>
    </form>
  `;
}
