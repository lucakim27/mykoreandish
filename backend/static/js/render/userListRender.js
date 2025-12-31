export function renderUserList(users) {
  const container = document.querySelector(".popular-dishes-list");
  container.innerHTML = "";

  users.forEach(user => {
    const el = document.createElement("li");
    el.style.display = "flex";
    el.style.alignItems = "center";
    el.style.borderBottom = "1px solid #eee";
    el.innerHTML = `
      <a href="/users/${user.google_id}"
         style="text-decoration:none; flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
        <b id="user_name">${user.name}</b>
      </a>
      <span id="created_at" style="margin-left:auto; font-size: 0.85em; color: grey; white-space:nowrap; padding-left:12px;">
        ${user.created_at}
      </span>
    `;

    container.appendChild(el);
  });
}
