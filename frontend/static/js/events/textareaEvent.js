import { addNote } from "../api/notesApi.js";

export function textareaEventBinding(name, user_id) {
    if (!name || !user_id) return;

    const textarea = document.getElementById("note-textarea");
    let saveTimeout;

    textarea.addEventListener("input", function () {
        document.getElementById("note-status").style.backgroundColor = "#f48f36ff";
        clearTimeout(saveTimeout);

        saveTimeout = setTimeout(async () => {
            try {
                const result = await addNote(name, user_id, textarea.value);
                document.getElementById("note-status").style.backgroundColor = "#4CAF50";
            } catch (err) {
                document.getElementById("note-status").style.backgroundColor = "#e53935";
            }
        }, 3000);
    });
}
