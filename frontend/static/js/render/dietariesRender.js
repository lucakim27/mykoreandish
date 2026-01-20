export function renderDietaries(dietaries) {
    const dietariesContainer = document.getElementById("dietary-select");

    for (const dietary of dietaries) {
        dietariesContainer.innerHTML += `
        <option value="${dietary}">${dietary.replaceAll("_", " ")}</option>
        `;
    }
}
