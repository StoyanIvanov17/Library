let selectedRating = 1;

const stars = document.querySelectorAll('.star');
const reviewForm = document.getElementById('review-form');
const submitButton = document.getElementById('submit-review-btn');
const reviewList = document.getElementById('reviews-list');

function updateStarDisplay() {
    stars.forEach(star => {
        if (parseInt(star.dataset.value) <= selectedRating) {
            star.classList.add('selected');
        } else {
            star.classList.remove('selected');
        }
    });
}

// Add click event listeners to each star to select rating
stars.forEach(star => {
    star.addEventListener('click', function() {
        selectedRating = this.dataset.value;
        updateStarDisplay();
    });
});

// Handle review form submission
submitButton.addEventListener('click', function(event) {
    event.preventDefault();

    const formData = new FormData(reviewForm);
    const itemId = this.getAttribute('data-item-id');
    const itemSlug = this.getAttribute('data-item-slug');
    const csrfToken = this.getAttribute('data-csrf-token');
    formData.append('rating', selectedRating);

    fetch(`/collections/${itemId}/${itemSlug}/detail/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const newReview = document.createElement('div');
            newReview.classList.add('review-item');
            newReview.innerHTML = `
                <div class="review-rating">Rating: ${selectedRating}/5</div>
                <p class="review-comment">${data.review_text}</p>
                <p class="review-user">Posted by ${data.username} on ${data.created_at}</p>
            `;
            reviewList.prepend(newReview);

            reviewForm.reset();
            selectedRating = 1;
            updateStarDisplay();
        } else {
            alert('Failed to submit review: ' + JSON.stringify(data.errors));
        }
    })
    .catch(error => console.error('Error:', error));
});