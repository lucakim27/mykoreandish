import { addNote, getNote, updateNote, deleteNote } from "../api/notesApi.js";
import { showToast } from "../utils/toaster.js";

export function textareaEventBinding(name, user_id) {
    if (!name) return;

    const textarea = document.getElementById("note-textarea");
    const statusIndicator = document.getElementById("note-status")
    let saveTimeout;
    
    textarea.addEventListener("input", function () {
        statusIndicator.style.backgroundColor = "#f48f36ff";
        clearTimeout(saveTimeout);
        
        saveTimeout = setTimeout(async () => {
            if (!user_id) {
                showToast(`Login to save ${name} to your personal note`, "warning");
                statusIndicator.style.backgroundColor = "#e53935";
                return;
            }
            
            let result;
            let note = {};

            try {
                try {
                    note = await getNote(name);
                } catch (_) {
                    note = {};
                }
                const isEmptyNote = Object.keys(note).length === 0;
                const hasText = textarea.value.trim() !== "";

                if (isEmptyNote && hasText) {
                    result = await addNote(name, textarea.value);
                } 
                else if (!isEmptyNote && hasText) {
                    result = await updateNote(name, textarea.value);
                } 
                else if (!isEmptyNote && !hasText) {
                    result = await deleteNote(name);
                }

                if (result == 204) {
                    statusIndicator.style.backgroundColor = "#4CAF50";
                }
            } catch (err) {
                statusIndicator.style.backgroundColor = "#e53935";
            }
        }, 3000);
    });
}
