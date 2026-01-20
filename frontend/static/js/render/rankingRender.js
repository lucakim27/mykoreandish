export function renderRankingList(container, items, basePath) {
  container.innerHTML = items.map((item, index) => `
    <li>
      <a href="/${basePath}/${item.name}">
        ${index + 1}. ${item.name.replaceAll("_", " ")} (${item.korean_name})
      </a>
    </li>
  `).join("");
}
