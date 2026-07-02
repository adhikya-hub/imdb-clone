function showToast(message) {
  document.getElementById("toast-message").textContent = message;

  bootstrap.Toast.getOrCreateInstance(
    document.getElementById("app-toast"),
  ).show();
}

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

      if (icon) {
        if (data.favorite) {
          icon.classList.remove("bi-heart", "text-white");
          icon.classList.add("bi-heart-fill", "text-warning");
        } else {
          icon.classList.remove("bi-heart-fill", "text-warning");
          icon.classList.add("bi-heart", "text-white");
        }
      }

      const personId = form.dataset.person;

      if (!data.favorite && personId) {
        const card = document.getElementById(`favorite-${personId}`);

        if (card) {
          card.remove();
        }
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

      const button = form.querySelector("button");
      const icon = form.querySelector("i");

      if (button.classList.contains("watchlist-icn")) {
        if (data.watchlist) {
          icon.classList.remove("bi-bookmark", "text-white");
          icon.classList.add("bi-bookmark-fill", "text-warning");
        } else {
          icon.classList.remove("bi-bookmark-fill", "text-warning");
          icon.classList.add("bi-bookmark", "text-white");
        }
      } else {
        if (data.watchlist) {
          button.classList.remove("btn-outline-warning");
          button.classList.add("btn-warning");

          button.innerHTML = `
            <i class="bi bi-bookmark-fill"></i>
            In Watchlist
          `;
        } else {
          button.classList.remove("btn-warning");
          button.classList.add("btn-outline-warning");

          button.innerHTML = `
            <i class="bi bi-bookmark-plus"></i>
            Add to Watchlist
          `;
        }
      }

      const movieId = form.dataset.movie;

      if (!data.watchlist && movieId) {
        const row = document.getElementById(`movie-${movieId}`);

        if (row) {
          row.remove();
        }

        if (document.querySelectorAll(".list-group-item").length === 0) {
          document
            .getElementById("watchlist-container")
            ?.classList.add("d-none");

          document
            .getElementById("empty-watchlist")
            ?.classList.remove("d-none");
        }
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

// function initReviewVoteButtons() {
//   document.querySelectorAll(".review-vote-form").forEach((form) => {
//     form.addEventListener("submit", async function (e) {
//       e.preventDefault();

//       const response = await fetch(form.action, {
//         method: "POST",
//         body: new FormData(form),
//       });

//       if (!response.ok) return;

//       const data = await response.json();

//       const reviewId = form.dataset.review;

//       document.getElementById(`helpful-${reviewId}`).textContent = data.helpful;

//       document.getElementById(`not-helpful-${reviewId}`).textContent =
//         data.not_helpful;
//     });
//   });
// }
function initReviewVoteButtons() {
  document.querySelectorAll(".review-vote-form").forEach((form) => {
    form.addEventListener("submit", async function (e) {
      e.preventDefault();

      const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
      });

      if (!response.ok) return;

      const data = await response.json();

      const reviewId = form.dataset.review;

      // Update counts
      document.getElementById(`helpful-${reviewId}`).textContent = data.helpful;

      document.getElementById(`not-helpful-${reviewId}`).textContent =
        data.not_helpful;

      // Update icons
      const helpfulIcon = document.getElementById(`helpful-icon-${reviewId}`);

      const notHelpfulIcon = document.getElementById(
        `not-helpful-icon-${reviewId}`,
      );

      if (data.user_vote === 1) {
        helpfulIcon.classList.remove("bi-hand-thumbs-up");
        helpfulIcon.classList.add("bi-hand-thumbs-up-fill");

        notHelpfulIcon.classList.remove("bi-hand-thumbs-down-fill");
        notHelpfulIcon.classList.add("bi-hand-thumbs-down");
      } else {
        notHelpfulIcon.classList.remove("bi-hand-thumbs-down");
        notHelpfulIcon.classList.add("bi-hand-thumbs-down-fill");

        helpfulIcon.classList.remove("bi-hand-thumbs-up-fill");
        helpfulIcon.classList.add("bi-hand-thumbs-up");
      }
    });
  });
}

// function initMovieListsForm() {
//   const form = document.querySelector(".movie-lists-form");

//   if (!form) return;

//   form.addEventListener("submit", async function (e) {
//     e.preventDefault();

//     const response = await fetch(form.action, {
//       method: "POST",
//       body: new FormData(form),
//     });

//     if (!response.ok) return;

//     const data = await response.json();

//     const message = document.getElementById("list-message");

//     message.classList.remove("d-none");

//     message.textContent = `✓ Saved to ${data.saved_to} list${data.saved_to == 1 ? "" : "s"}.`;

//     bootstrap.Modal.getInstance(document.getElementById("listModal")).hide();
//   });
// }
function initMovieListsForm() {
  const form = document.querySelector(".movie-lists-form");

  if (!form) return;

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const response = await fetch(form.action, {
      method: "POST",
      body: new FormData(form),
    });

    if (!response.ok) return;

    await response.json();

    bootstrap.Modal.getOrCreateInstance(
      document.getElementById("listModal"),
    ).hide();
  });
}
function initHistoryButtons() {
  document.querySelectorAll(".history-form").forEach((form) => {
    form.addEventListener("submit", async function (e) {
      e.preventDefault();

      const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
      });

      if (!response.ok) return;

      const data = await response.json();

      if (data.message) {
        showToast(data.message);
        return;
      }

      const button = form.querySelector("button");
      const icon = button.querySelector("i");
      const text = button.querySelector("span");

      if (data.watched) {
        icon.classList.remove("bi-eye");
        icon.classList.add("bi-eye-slash");

        text.textContent = "Watched";
        const watchlistContainer = document.getElementById(
          "watchlist-container",
        );

        if (watchlistContainer && data.watched) {
          const movieId = form.dataset.movie;

          document.getElementById(`movie-${movieId}`)?.remove();

          if (!watchlistContainer.querySelector("[id^='movie-']")) {
            watchlistContainer.classList.add("d-none");

            document
              .getElementById("empty-watchlist")
              ?.classList.remove("d-none");
          }
        }
      } else {
        icon.classList.remove("bi-eye-slash");
        icon.classList.add("bi-eye");

        text.textContent = "Mark as watched";
      }
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initFavoriteButtons();
  initWatchlistButtons();
  initRatingButtons();
  initRemoveRatingButton();
  initReviewVoteButtons();
  initMovieListsForm();
  initHistoryButtons();
});
