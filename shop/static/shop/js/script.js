document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const resultsContainer = document.getElementById("resultsContainer");

    const historyBox = document.createElement("div");
    historyBox.id = "searchHistoryBox";
    historyBox.style.border = "1px solid #ccc";
    historyBox.style.background = "#fff";
    historyBox.style.position = "absolute";
    historyBox.style.zIndex = "10";
    historyBox.style.width = searchInput.offsetWidth + "px";
    historyBox.style.display = "none";
    historyBox.style.maxHeight = "150px";
    historyBox.style.overflowY = "auto";
    document.body.appendChild(historyBox);

    const inputRect = searchInput.getBoundingClientRect();
    historyBox.style.top = inputRect.bottom + window.scrollY + "px";
    historyBox.style.left = inputRect.left + "px";

    function saveSearchHistory(query) {
        if (!query.trim()) return;
        let history = JSON.parse(localStorage.getItem("searchHistory") || "[]");
        if (!history.includes(query)) {
            history.unshift(query);
            if (history.length > 5) history = history.slice(0, 5);
            localStorage.setItem("searchHistory", JSON.stringify(history));
        }
    }

    function showSearchHistory() {
        let history = JSON.parse(localStorage.getItem("searchHistory") || "[]");
        if (history.length === 0) return;

        historyBox.innerHTML = "";
        history.forEach(item => {
            const div = document.createElement("div");
            div.style.padding = "8px";
            div.style.cursor = "pointer";
            div.textContent = item;
            div.onclick = () => {
                searchInput.value = item;
                triggerSearch(item);
                historyBox.style.display = "none";
            };
            historyBox.appendChild(div);
        });
        historyBox.style.display = "block";
    }

    function triggerSearch(customQuery = null) {
    const query = customQuery !== null ? customQuery : searchInput.value;
    const brands = [...document.querySelectorAll('input[name="brand"]:checked')].map(el => el.value);
    const categories = [...document.querySelectorAll('input[name="category"]:checked')].map(el => el.value);
    const materials = [...document.querySelectorAll('input[name="material"]:checked')].map(el => el.value);
    const minPrice = document.getElementById("minPrice") ? document.getElementById("minPrice").value : '';
    const maxPrice = document.getElementById("maxPrice") ? document.getElementById("maxPrice").value : '';
    const inStock = document.getElementById("inStock") && document.getElementById("inStock").checked ? '1' : '';
    const sortBy = document.getElementById("sortSelect") ? document.getElementById("sortSelect").value : '';

    console.log("🔍 Price Filter: ", { minPrice, maxPrice });  // ✅ Add this line

    const params = new URLSearchParams();
    if (query) params.append('q', query);
    brands.forEach(brand => params.append('brand', brand));
    categories.forEach(category => params.append('category', category));
    materials.forEach(material => params.append('material', material));
    if (minPrice) params.append('min_price', minPrice);
    if (maxPrice) params.append('max_price', maxPrice);
    if (inStock) params.append('in_stock', inStock);
    if (sortBy) params.append('sort_by', sortBy);

    fetch(`/shop/products/?${params.toString()}`, {
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {
        resultsContainer.innerHTML = data.html;
        saveSearchHistory(query);
    });
}

    searchInput.addEventListener("keyup", function () {
        const query = searchInput.value;
        if (!query) return;
        triggerSearch(query);
        historyBox.style.display = "none";
    });

    searchInput.addEventListener("focus", function () {
        if (!searchInput.value.trim()) {
            showSearchHistory();
        }
    });

    document.addEventListener("click", function (e) {
        if (!historyBox.contains(e.target) && e.target !== searchInput) {
            historyBox.style.display = "none";
        }
    });

    // 🛒 Trigger search when any filter checkbox or price changes
    document.querySelectorAll('input[type="checkbox"]').forEach(input => {
        input.addEventListener("change", function () {
            triggerSearch();
        });
    });

    document.querySelectorAll('input[type="number"]').forEach(input => {
        input.addEventListener("input", function () {
            triggerSearch();
        });
    });


    // 🛒 NEW: Trigger search when sort option changes
    const sortSelect = document.getElementById("sortSelect");
    if (sortSelect) {
        sortSelect.addEventListener("change", function () {
            triggerSearch();
        });
    }
});
