export function renderProfile(dietaries, user) {
    const profileContainer = document.getElementById("profile-container");
    profileContainer.innerHTML = `
        <table>
        <tr>
            <th>Name</th>
            <td>${user.name}</td>
        </tr>
        <tr>
            <th>Email</th>
            <td>${user.email.length === 0 ? "N/A" : user.email}</td>
        </tr>
        <tr>
            <th>Admin</th>
            <td>${user.admin}</td>
        </tr>
        <tr>
            <th>Google ID</th>
            <td>${user.google_id}</td>
        </tr>
        <tr>
            <th>Registered At</th>
            <td>${user.created_at}</td>
        </tr>
        <tr>
            <th>Last Login</th>
            <td>${user.last_login}</td>
        </tr>
        <tr>
            <th>Dietary Preference</th>
            <td>
                <form method="POST" action="/api/users/${user.google_id}">
                    <select name="dietary_preference" onchange="this.form.submit()">
                        <option value="">None</option>
                        ${dietaries.map(dietary => `<option value="${dietary}" ${user.dietary_preference === dietary ? 'selected' : ''}>${dietary}</option>`).join('')}
                    </select>
                </form>
            </td>
        </tr>
    </table>
    `
}