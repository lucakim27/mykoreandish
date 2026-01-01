export function renderFavorites(favorites) {
    const favoritesContainer = document.getElementById("favorite-btn");

    for (const favorite of favorites) {
        favoritesContainer.innerHTML += `
        {% if dish.dish_name in favorites %}
            <form action="/favorite/delete/dish/{{ dish.dish_name }}" method="POST">
                <button class="favorite-btn" type="submit">
                    <i class="fa-solid fa-heart" style="color: #d72638;"></i>
                </button>
            </form>
            {% else %}
            <form action="/favorite/add/dish/{{ dish.dish_name }}" method="POST">
                <button class="favorite-btn" type="submit">
                    <i class="fa-regular fa-heart"></i>
                </button>
            </form>
        {% endif %}
        `;
    }
}