import { renderSearchResults } from "../render/searchRender.js";

export function bindSearchEvents(searchInput, searchResults, searchItems) {
  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase().trim();

    if (!query) {
      searchResults.style.display = "none";
      return;
    }

    const matches = searchItems.filter(item =>
      item.name.toLowerCase().includes(query) ||
      item.koreanName.toLowerCase().includes(query)
    );

    if (matches.length === 0) {
      searchResults.style.display = "none";
      return;
    }

    renderSearchResults(searchResults, matches);
  });

  document.addEventListener("click", e => {
    if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
      searchResults.style.display = "none";
    }
  });

  searchInput.addEventListener("keypress", e => {
    if (e.key === "Enter") {
      const query = searchInput.value.toLowerCase().trim();
      const match = searchItems.find(item =>
        item.name.toLowerCase().includes(query) ||
        item.koreanName.toLowerCase().includes(query)
      );
      if (match) window.location.href = match.url;
    }
  });
}
