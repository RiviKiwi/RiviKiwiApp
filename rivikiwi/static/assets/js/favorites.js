function toggleFavorite(btn, event) {
    event.preventDefault();
    event.stopPropagation();

    btn.classList.toggle('favorite-product');
}