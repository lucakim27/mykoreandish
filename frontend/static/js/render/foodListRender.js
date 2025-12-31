export function renderAllDishes(allDishes, favoriteDishes) {
    const container = document.getElementById("food-list");
    container.innerHTML = "";
    
    allDishes.forEach(dish => {
        const li = document.createElement("li");
        li.className = "food-item";
        
        const form = document.createElement("form");
        form.action = `/dishes/${dish.dish_name}`;
        form.method = "GET";
        form.className = "food-box";
        
        const imageWrapper = document.createElement("div");
        imageWrapper.className = "dish-image-wrapper";
        if (dish.image_url) {
            const img = document.createElement("img");
            img.src = dish.image_url;
            img.alt = dish.korean_name;
            img.className = "dish-image";
            imageWrapper.appendChild(img);
        }
        
        const favBtn = document.createElement("button");
        favBtn.type = "button";
        favBtn.className = "favorite-btn";
        favBtn.innerHTML = favoriteDishes.includes(dish.dish_name) 
            ? '<i class="fa-solid fa-heart" style="color: #d72638"></i>' 
            : '<i class="fa-regular fa-heart"></i>';
        
        const h3 = document.createElement("h3");
        h3.textContent = dish.korean_name;
        
        const p = document.createElement("p");
        p.innerHTML = `<b>${dish.dish_name}</b>, ${dish.description}`;
        
        const indicator = document.createElement("div");
        indicator.className = "click-indicator";
        indicator.innerHTML = "<span>Click to view details</span>";
        
        const submitBtn = document.createElement("button");
        submitBtn.type = "submit";
        submitBtn.className = "hidden-submit-btn";
        
        form.appendChild(imageWrapper);
        form.appendChild(favBtn);
        form.appendChild(h3);
        form.appendChild(p);
        form.appendChild(indicator);
        form.appendChild(submitBtn);
        
        li.appendChild(form);
        container.appendChild(li);
    });
}