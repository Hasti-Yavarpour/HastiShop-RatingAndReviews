function toggleRatingForm(productId) {
    const form = document.getElementById(`rating-form-${productId}`);
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function submitReview(productId) {
    const rating = document.getElementById(`rating-value-${productId}`).value;
    const comment = document.getElementById(`comment-${productId}`).value;

    if (rating < 1 || rating > 5) {
        alert("Please select a star rating.");
        return;
    }

    fetch(`/shop/api/products/${productId}/reviews/submit/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rating, comment })
    })
        .then(res => res.json())
        .then(data => {
            alert(data.message || 'Review submitted!');

            // Refresh updated UI
            loadAverageRating(productId);
            loadReviews(productId);
            loadRatingDistribution(productId);

            // Reset form
            document.getElementById(`comment-${productId}`).value = "";
            document.getElementById(`rating-value-${productId}`).value = 0;

            const stars = document.querySelectorAll(`#stars-${productId} .star`);
            stars.forEach(s => s.classList.remove('selected'));

            document.getElementById(`rating-form-${productId}`).style.display = "none";
        });
}

function loadAverageRating(productId) {
    fetch(`/shop/api/products/${productId}/average-rating/`)
        .then(res => res.json())
        .then(data => {
            const avg = data.average;
            const count = data.count;

            const badge = document.querySelector(`#avg-rating-${productId}`);
            if (badge) {
                badge.innerHTML = `
                    <span style="font-size: 16px; color: gold;">&#9733;</span>
                    <strong>${avg}</strong> out of 5 (${count} review${count === 1 ? '' : 's'})
                `;
            }
        });
}

function loadReviews(productId) {
    fetch(`/shop/api/products/${productId}/reviews/`)
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById(`latest-reviews-${productId}`);
            container.innerHTML = "";
            data.reviews.forEach(r => {
                container.innerHTML += `<p>⭐ ${r.rating} - ${r.comment || ''} <i>(${r.time_ago})</i></p>`;
            });
        });
}

function loadRatingDistribution(productId) {
    fetch(`/shop/api/products/${productId}/rating-distribution/`)
        .then(res => res.json())
        .then(data => {
            const { distribution, counts, total, average } = data;
            const container = document.getElementById(`rating-distribution-${productId}`);
            container.innerHTML = `
                <div class="rating-summary">
                    <div class="rating-average-stars">
                        <span style="font-size: 20px; color: gold;">&#9733;</span>
                        <strong>${average}</strong> out of 5
                    </div>
                    <div class="rating-total">
                        ${total} customer rating${total === 1 ? '' : 's'}
                    </div>
                </div>
            `;

            for (let star = 5; star >= 1; star--) {
                const percent = Math.round(distribution[star]) || 0;
                const count = counts[star] || 0;

                container.innerHTML += `
                    <div class="rating-bar-row">
                        <span class="rating-label">${'★'.repeat(star)}</span>
                        <div class="rating-bar">
                            <div class="rating-bar-fill" style="width: ${percent}%;"></div>
                        </div>
                        <span class="rating-count">${percent}% (${count})</span>
                    </div>
                `;
            }
        });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.product-card').forEach(card => {
        const productId = card.dataset.productId;

        loadAverageRating(productId);
        loadReviews(productId);
        loadRatingDistribution(productId);

        const starsContainer = document.getElementById(`stars-${productId}`);
        const hiddenInput = document.getElementById(`rating-value-${productId}`);
        if (starsContainer && hiddenInput) {
            const stars = starsContainer.querySelectorAll('.star');

            stars.forEach((star, index) => {
                const rating = index + 1;

                star.addEventListener('mouseenter', () => {
                    stars.forEach((s, i) => {
                        s.classList.toggle('hovered', i < rating);
                    });
                });

                star.addEventListener('mouseleave', () => {
                    stars.forEach(s => s.classList.remove('hovered'));
                });

                star.addEventListener('click', () => {
                    hiddenInput.value = rating;

                    stars.forEach((s, i) => {
                        s.classList.toggle('selected', i < rating);
                    });
                });
            });
        }
    });
});
