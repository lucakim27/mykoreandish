export function getUserIdFromPath() {
    const pathParts = window.location.pathname.split('/');
    return pathParts[pathParts.length - 1];
}

export function getDishOrIngredientName() {
  const path = window.location.pathname;
  const segments = path.split('/').filter(Boolean);
  const encodedDishName = segments[segments.length - 1];

  return decodeURIComponent(encodedDishName);
}