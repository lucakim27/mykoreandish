export function renderIngredients(ingredients) {
    const ingredientsContainer = document.getElementById("ingredient-select");

    for (const ingredient of ingredients) {
        ingredientsContainer.innerHTML += `
        <option value="${ingredient.ingredient}">${ingredient.ingredient.replaceAll("_", " ")}</option>
        `;
    }
}
