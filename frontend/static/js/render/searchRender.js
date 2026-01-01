export function renderSearchResults(container, items) {
  container.innerHTML = "";

  items.forEach(item => {
    const el = document.createElement("div");
    el.className = "search-result-item";
    el.innerHTML = `
      <div class="result-icon">
        <i class="fas fa-${item.type === "dish" ? "utensils" : "carrot"}"></i>
      </div>
      <div class="result-content">
        <div class="result-name">${item.koreanName}</div>
        <div class="result-subtitle">${item.name}</div>
      </div>
    `;

    el.onclick = () => (window.location.href = item.url);
    container.appendChild(el);
  });

  container.style.display = "block";
}
