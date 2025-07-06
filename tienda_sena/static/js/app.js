
// Función para cambiar imagen principal del producto
function changeMainImage(url) {
    document.getElementById('mainImage').src = url;
}

// Sistema de calificación con estrellas
document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star-rating');
    const ratingContainer = document.querySelector('.rating-stars');
    let currentRating = 0;
    
    // Verificar si los elementos existen en la página
    if (!stars.length || !ratingContainer) {
        console.log('Elementos de calificación no encontrados en esta página');
        return;
    }
    
    stars.forEach((star, index) => {
        star.addEventListener('click', function() {
            currentRating = index + 1;
            updateStars();
            console.log('Calificación seleccionada:', currentRating);
        });
        
        star.addEventListener('mouseenter', function() {
            highlightStars(index + 1);
        });
    });
    
    ratingContainer.addEventListener('mouseleave', function() {
        updateStars();
    });
    
    function updateStars() {
        stars.forEach((star, index) => {
            if (index < currentRating) {
                star.classList.remove('far');
                star.classList.add('fas');
                star.style.color = '#ffc107';
            } else {
                star.classList.remove('fas');
                star.classList.add('far');
                star.style.color = '#dee2e6';
            }
        });
    }
    
    function highlightStars(rating) {
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.remove('far');
                star.classList.add('fas');
                star.style.color = '#ffc107';
            } else {
                star.classList.remove('fas');
                star.classList.add('far');
                star.style.color = '#dee2e6';
            }
        });
    }
    
    console.log('Sistema de calificación inicializado correctamente');
});
