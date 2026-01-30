const tabs = document.querySelectorAll('.tab');
const reviews = document.querySelectorAll('.review-card');

tabs.forEach(tab => {
  tab.addEventListener('click', () => {

    // активная вкладка
    tabs.forEach(t => t.classList.remove('active'));
    tab.classList.add('active');

    const selected = tab.dataset.tab;

    reviews.forEach(review => {
      if (selected === 'my') {
        // показываем только мои отзывы
        review.style.display = review.classList.contains('my-review')
          ? 'block'
          : 'none';
      } else {
        // показываем все
        review.style.display = 'block';
      }
    });
  });
});

const stars = document.querySelectorAll('.rating-select .star');
const ratingInput = document.getElementById('ratingValue');

stars.forEach(star => {
  star.addEventListener('click', () => {
    const value = parseInt(star.dataset.value);
    ratingInput.value = value;

    stars.forEach(s => {
      s.classList.toggle(
        'active',
        parseInt(s.dataset.value) <= value
      );
    });
  });
});
