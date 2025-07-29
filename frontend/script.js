async function submitQuery() {
  const queryInput = document.getElementById("user-query");
  const query = queryInput.value.trim();

  if (!query) {
    alert("Please enter a query!");
    return;
  }

  try {
    const response = await fetch("/api/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    const result = await response.json();

    if (response.ok) {
      alert("✅ Products fetched successfully!");
      loadProducts(); // Load products after success
    } else {
      alert("❌ " + (result.error || "Something went wrong."));
    }
  } catch (error) {
    alert("Error occurred: " + error.message);
  }
}

async function loadProducts() {
  const container = document.getElementById("products-container");
  container.innerHTML = ""; // Clear previous results

  try {
    const response = await fetch("/api/products");
    const products = await response.json();

    if (!Array.isArray(products) || products.length === 0) {
      container.innerHTML = "<p>No products found.</p>";
      return;
    }

    products.forEach((product) => {
      const card = document.createElement("div");
      card.className = "product-card";

      card.innerHTML = `
        <img src="${product.image}" alt="${product.title}" />
        <h3>${product.title}</h3>
        <p>Price: ₹${product.price}</p>
        <a href="${
          product.url
        }" target="_blank" class="amazon-link">View on Amazon</a><br/><br/>
        <button class="add-cart-btn" onclick="addToCart('${encodeURIComponent(
          product.url
        )}')">🛒 Add to Cart</button>
      `;

      container.appendChild(card);
    });
  } catch (err) {
    container.innerHTML = `<p>Error loading products: ${err.message}</p>`;
  }
}

async function addToCart(encodedUrl) {
  const url = decodeURIComponent(encodedUrl);

  try {
    const response = await fetch(`/api/add_to_cart`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }), // ✅ Send in body
    });

    const data = await response.json();

    if (response.ok) {
      alert("✅ " + data.message);
    } else {
      alert("❌ " + (data.detail || "Failed to add to cart."));
    }
  } catch (err) {
    alert("Error: " + err.message);
  }
}

window.onload = loadProducts;
