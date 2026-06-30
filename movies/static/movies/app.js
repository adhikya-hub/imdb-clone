function initFavoriteButtons() {
  document.querySelectorAll(".favorite-form").forEach((form) => {
    form.addEventListener("submit", async function (e) {
      e.preventDefault();

      const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
      });

      if (!response.ok) return;

      const data = await response.json();

      const icon = form.querySelector("i");

      if (data.favorite) {
        icon.classList.remove("bi-heart", "text-white");
        icon.classList.add("bi-heart-fill", "text-warning");
      } else {
        icon.classList.remove("bi-heart-fill", "text-warning");
        icon.classList.add("bi-heart", "text-white");
      }
    });
  });
}

function initWatchlistButtons() {
  document.querySelectorAll(".watchlist-form").forEach((form) => {
    form.addEventListener("submit", async function (e) {
      e.preventDefault();

      const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
      });

      if (!response.ok) return;

      const data = await response.json();

      const icon = form.querySelector("i");

      if (data.watchlist) {
        icon.classList.remove("bi-bookmark", "text-white");
        icon.classList.add("bi-bookmark-fill", "text-warning");
      } else {
        icon.classList.remove("bi-bookmark-fill", "text-warning");
        icon.classList.add("bi-bookmark", "text-white");
      }
    });
  });
}

function initRatingButtons() {
  const form = document.querySelector(".rating-form");

  if (!form) return;

  const stars = form.querySelectorAll(".star");
  const input = form.querySelector("#rating-value");
  const button = form.querySelector("#rate-btn");

  function paint(rating) {
    stars.forEach((star) => {
      if (Number(star.dataset.rating) <= Number(rating)) {
        star.classList.remove("bi-star");
        star.classList.add("bi-star-fill", "active");
      } else {
        star.classList.remove("bi-star-fill", "active");
        star.classList.add("bi-star");
      }
    });
  }

  paint(input.value);

  button.disabled = !input.value;

  stars.forEach((star) => {
    star.addEventListener("mouseenter", () => {
      paint(star.dataset.rating);
    });

    star.addEventListener("click", () => {
      input.value = star.dataset.rating;
      button.disabled = false;
      paint(input.value);
    });
  });

  form.querySelector(".rating-stars").addEventListener("mouseleave", () => {
    paint(input.value);
  });

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const response = await fetch(form.action, {
      method: "POST",
      body: new FormData(form),
    });

    if (!response.ok) return;

    const data = await response.json();

    // Update IMDb rating
    document.getElementById("vote-average").textContent =
      data.vote_average.toFixed(1);

    document.getElementById("vote-count").textContent = data.vote_count;

    // Update "Your Rating"
    document.getElementById("your-rating").innerHTML = `
      <span class="text-warning">
        ★ ${data.rating}
      </span>
      <small class="text-secondary">/10</small>
    `;

    // Update modal
    document.getElementById("current-rating").innerHTML = `★ ${data.rating}/10`;

    document
      .getElementById("remove-rating-container")
      .classList.remove("d-none");

    // Keep hidden input in sync
    input.value = data.rating;

    // Keep stars selected
    paint(data.rating);

    // Disable button until user changes rating again
    button.disabled = true;

    // Close modal
    bootstrap.Modal.getInstance(document.getElementById("ratingModal")).hide();
  });

  // Reset button when modal is opened again
  document
    .getElementById("ratingModal")
    .addEventListener("shown.bs.modal", () => {
      paint(input.value);
      button.disabled = !input.value;
    });
}

function initRemoveRatingButton() {
  const form = document.querySelector(".remove-rating-form");

  if (!form) return;

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const response = await fetch(form.action, {
      method: "POST",
      body: new FormData(form),
    });

    if (!response.ok) return;

    const data = await response.json();

    document.getElementById("vote-average").textContent =
      data.vote_average.toFixed(1);

    document.getElementById("vote-count").textContent = data.vote_count;

    document.getElementById("your-rating").innerHTML = "☆ Rate";

    document.getElementById("rating-value").value = "";

    document.getElementById("rate-btn").disabled = true;

    document.querySelectorAll(".star").forEach((star) => {
      star.classList.remove("bi-star-fill", "active");
      star.classList.add("bi-star");
    });

    document.getElementById("remove-rating-container").classList.add("d-none");

    document.getElementById("current-rating").innerHTML = "";

    bootstrap.Modal.getInstance(document.getElementById("ratingModal")).hide();
  });
}
document.addEventListener("DOMContentLoaded", () => {
  initFavoriteButtons();
  initWatchlistButtons();
  initRatingButtons();
  initRemoveRatingButton();
});
