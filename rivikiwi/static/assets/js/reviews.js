const tabs = document.querySelectorAll(".tab");
const reviews = document.querySelectorAll(".review-card");

// Вкладки
tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");

    const selected = tab.dataset.tab;

    reviews.forEach((review) => {
      if (selected === "my") {
        review.style.display = review.classList.contains("my-review")
          ? "block"
          : "none";
      } else {
        review.style.display = "block";
      }
    });
  });
});

// ЗВЕЗДЫ В ФОРМЕ ДОБАВЛЕНИЯ
const addStars = document.querySelectorAll('.write-review-card .add-star');
const ratingInput = document.getElementById('ratingValue');

addStars.forEach((star) => {
  star.addEventListener("click", () => {
    const value = parseInt(star.dataset.value);
    ratingInput.value = value;

    // Обновляем только звезды добавления
    addStars.forEach((s) => {
      s.classList.toggle("active", parseInt(s.dataset.value) <= value);
    });
  });
});

/* ================= EDIT REVIEW ================= */
document.querySelectorAll('.edit-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const card = btn.closest('.review-card');
    const textElement = card.querySelector('.review-text');
    const editForm = card.querySelector('.edit-review-form');
    const editTextarea = editForm.querySelector('.edit-textarea');
    const editRatingInput = editForm.querySelector('.edit-rating-input');
    const actions = card.querySelector('.review-actions');
    
    // Получаем текущий рейтинг
    const ratingElement = card.querySelector('.review-meta');
    const ratingMatch = ratingElement.textContent.match(/(\d+(\.\d+)?)/);
    const currentRating = ratingMatch ? parseFloat(ratingMatch[1]) : 0;

    // Заполняем форму
    editTextarea.value = textElement.textContent.trim();
    editRatingInput.value = currentRating;

    // Обновляем звезды редактирования в этой карточке
    const editStars = editForm.querySelectorAll('.edit-star');
    editStars.forEach(star => {
      const starValue = parseInt(star.dataset.value);
      star.classList.toggle('active', starValue <= currentRating);
    });

    // Показываем форму, скрываем текст и кнопки
    textElement.style.display = 'none';
    actions.style.display = 'none';
    editForm.style.display = 'block';
  });
});

// ОБРАБОТКА ЗВЕЗД РЕДАКТИРОВАНИЯ (делегирование)
document.addEventListener('click', function(e) {
  // Клик на звезду редактирования
  if (e.target.classList.contains('edit-star')) {
    const editForm = e.target.closest('.edit-review-form');
    const star = e.target;
    const value = parseInt(star.dataset.value);
    const editRatingInput = editForm.querySelector('.edit-rating-input');
    
    // Обновляем значение
    editRatingInput.value = value;
    
    // Обновляем все звезды редактирования в этой форме
    const editStars = editForm.querySelectorAll('.edit-star');
    editStars.forEach(s => {
      s.classList.toggle('active', parseInt(s.dataset.value) <= value);
    });
  }
  
  // Кнопка "Отмена" в форме редактирования
  if (e.target.classList.contains('cancel-btn')) {
    e.preventDefault();
    const editForm = e.target.closest('.edit-review-form');
    const card = editForm.closest('.review-card');
    const textElement = card.querySelector('.review-text');
    const actions = card.querySelector('.review-actions');
    
    editForm.style.display = 'none';
    textElement.style.display = '';
    actions.style.display = '';
  }
});