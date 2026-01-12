export function renderUserList(users) {
  const container = document.querySelector(".user-list");
  container.innerHTML = "";

  users.forEach(user => {
    const li = document.createElement("li");
    li.className = "user-row";

    li.innerHTML = `
      <a href="/users/${user.google_id}" class="user-link">
        <div class="user-info">
          <div class="user-name">${user.name}</div>
          <div class="user-meta">Registered ${user.created_at}</div>
        </div>
        <div class="user-action">View →</div>
      </a>
    `;

    container.appendChild(li);
  });
}
