export function renderUserProfile(user) {
    const user_name_element = document.getElementById("name");
    user_name_element.innerText = user.name

    const user_email_element = document.getElementById("email");
    user_email_element.innerText = `Email: ${user.email ? user.email : "N/A"}`;

    const user_admin_element = document.getElementById("admin");
    user_admin_element.innerText = `Admin: ${user.admin ? "Yes" : "No"}`;

    const user_created_at_element = document.getElementById("created_at");
    user_created_at_element.innerText = `Joined on: ${user.created_at}`;

    const last_login_element = document.getElementById("last_login");
    last_login_element.innerText = `Last login: ${user.last_login}`;
}