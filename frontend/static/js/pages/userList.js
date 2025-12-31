import { getAllUsers } from "../api/usersApi.js";
import { renderUserList } from "../render/userListRender.js";

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const [allUsers] = await Promise.all([
      getAllUsers()
    ]);

    renderUserList(allUsers.users);

  } catch (err) {
    console.error(err);
  }
});
