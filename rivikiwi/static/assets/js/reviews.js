const tabs = document.querySelectorAll(".tab");
const reviews = document.querySelectorAll(".review-card");

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    // активная вкладка
    tabs.forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");

    const selected = tab.dataset.tab;

    reviews.forEach((review) => {
      if (selected === "my") {
        // показываем только мои отзывы
        review.style.display = review.classList.contains("my-review")
          ? "block"
          : "none";
      } else {
        // показываем все
        review.style.display = "block";
      }
    });
  });
});

const stars = document.querySelectorAll(".rating-select .star");
const ratingInput = document.getElementById("ratingValue");

stars.forEach((star) => {
  star.addEventListener("click", () => {
    const value = parseInt(star.dataset.value);
    ratingInput.value = value;

    stars.forEach((s) => {
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
    const editRatingInput = editForm.querySelector('input[name="rating"]');
    const actions = card.querySelector('.review-actions');
    
    // Получаем текущий рейтинг из отображения
    const ratingElement = card.querySelector('.review-meta');
    const ratingMatch = ratingElement.textContent.match(/(\d+(\.\d+)?)/);
    const currentRating = ratingMatch ? parseFloat(ratingMatch[1]) : 0;
    
    // Заполняем форму текущими значениями
    editTextarea.value = textElement.textContent.trim();
    editRatingInput.value = currentRating;
    
    // Устанавливаем активные звезды
    const editStars = editForm.querySelectorAll('.star');
    editStars.forEach(star => {
      const starValue = parseInt(star.dataset.value);
      star.classList.toggle('active', starValue <= currentRating);
    });
    
    // Показываем форму, скрываем текст и кнопки
    textElement.style.display = 'none';
    actions.style.display = 'none';
    editForm.style.display = 'block';
    
    // Добавляем обработчики для звезд в форме редактирования
    editStars.forEach(star => {
      star.addEventListener('click', () => {
        const value = parseInt(star.dataset.value);
        editRatingInput.value = value;
        
        editStars.forEach(s => {
          const sValue = parseInt(s.dataset.value);
          s.classList.toggle('active', sValue <= value);
        });
      });
    });
    
    // Кнопка Отмена
    const cancelBtn = editForm.querySelector('.cancel-btn');
    cancelBtn.addEventListener('click', () => {
      // Скрываем форму, показываем текст и кнопки
      editForm.style.display = 'none';
      textElement.style.display = '';
      actions.style.display = '';
    });
  });
});
