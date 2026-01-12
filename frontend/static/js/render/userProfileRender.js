import { timeAgo } from "../utils/timeAgo.js";

export function renderUserProfile(user) {
  const user_name_element = document.getElementById("name");
  user_name_element.innerText = user.name;

  const user_email_element = document.getElementById("email");
  user_email_element.innerText = `Email: ${user.email ? user.email : "N/A"}`;

  const user_admin_element = document.getElementById("admin");
  user_admin_element.innerText = `Admin: ${user.admin ? "Yes" : "No"}`;

  const dietary_preferences_element = document.getElementById("dietary_preferences");
  dietary_preferences_element.innerText = `Dietary preference: ${user.dietary_preference ? user.dietary_preference : "Not selected"}`;


  const user_created_at_element = document.getElementById("created_at");
  user_created_at_element.innerText = `Joined on: ${user.created_at}`;

  const last_login_element = document.getElementById("last_login");
  last_login_element.innerText = `Last login: ${user.last_login}`;
}

export function renderUserHistory(history) {
  if (!Array.isArray(history) || history.length === 0) return;

  const grouped = {};

  history.forEach((entry) => {
    const dish = entry.dish_name;
    if (!dish) return;

    if (!grouped[dish]) grouped[dish] = [];
    grouped[dish].push(entry);
  });

  const container = document.querySelector(".about-us-container");

  const existing = document.getElementById("user-history");
  if (existing) existing.remove();

  const historySection = document.createElement("div");
  historySection.id = "user-history";

  Object.entries(grouped).forEach(([dishName, entries]) => {
    const card = document.createElement("div");
    card.className = "history-card";

    entries.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    const linesHtml = entries
      .map((entry) => {
        const time = timeAgo(entry.timestamp);

        if ("rating" in entry) {
          return `
            <div class="history-line">
              <span class="history-text">
                Rating: ${entry.rating},
                Healthiness: ${entry.healthiness},
                Spiciness: ${entry.spiciness},
                Texture: ${entry.texture},
                Sourness: ${entry.sourness},
                Sweetness: ${entry.sweetness},
                Temperature: ${entry.temperature}
              </span>
              <span class="history-time">${time}</span>
            </div>
          `;
        }

        if (entry.country || entry.state || entry.price) {
          const location = [entry.state, entry.country]
            .filter(Boolean)
            .join(", ");
          const price = entry.price ? `$${entry.price}` : "";
          const text = [location, price].filter(Boolean).join(": ");

          return `
                <div class="history-line">
                <span class="history-text">${text}</span>
                <span class="history-time">${time}</span>
                </div>
            `;
        }

        if (entry.ingredient) {
          return `
            <div class="history-line">
            <span class="history-text">Ingredient: ${entry.ingredient}</span>
            <span class="history-time">${time}</span>
            </div>
        `;
        }

        if (entry.dietary) {
          return `
            <div class="history-line">
            <span class="history-text">Dietary: ${entry.dietary}</span>
            <span class="history-time">${time}</span>
            </div>
        `;
        }
      })
      .join("");

    card.innerHTML = `
      <h3>${dishName}</h3>
      ${linesHtml}
    `;

    historySection.appendChild(card);
  });

  container.appendChild(historySection);
}
