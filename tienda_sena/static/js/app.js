
const starRating = document.querySelector('.star-rating');
const ratingValue = document.getElementById('rating-value');
starRating.addEventListener('change', function(e) {
    ratingValue.textContent = e.target.value;
});
