function changeImage(element) {
    var mainImage = document.getElementById("main-image");
    
    mainImage.src = element.src;

    var thumbnails = document.querySelectorAll(".thumbnail");
    thumbnails.forEach(function(thumb) {
        thumb.classList.remove("active");
    });
    element.classList.add("active");
}

document.addEventListener('DOMContentLoaded', () => {
  const editBtn = document.getElementById('editToggle');
  const editBlock = document.getElementById('productEdit');

  const viewTitle = document.getElementById('viewTitle');
  const viewPrice = document.getElementById('viewPrice');
  const viewDescription = document.getElementById('viewDescription');

  const editTitle = document.getElementById('editTitle');
  const editPrice = document.getElementById('editPrice');
  const editDescription = document.getElementById('editDescription');

  const saveBtn = document.getElementById('saveEdit');
  const cancelBtn = document.getElementById('cancelEdit');

  if (!editBtn || !editBlock) {
    console.error('❌ editToggle или productEdit не найдены');
    return;
  }

  editBtn.addEventListener('click', () => {
    editBlock.classList.toggle('hidden');
    editBlock.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  cancelBtn.addEventListener('click', () => {
    editTitle.value = viewTitle.textContent;
    editPrice.value = parseInt(viewPrice.textContent);
    editDescription.value = viewDescription.textContent.trim();
    editBlock.classList.add('hidden');
  });

  saveBtn.addEventListener('click', () => {
    viewTitle.textContent = editTitle.value;
    viewPrice.textContent = `${editPrice.value} ₽`;
    viewDescription.textContent = editDescription.value;
    editBlock.classList.add('hidden');
  });
});

function togglePhone() {
  const phoneElement = document.getElementById('phoneNumber');
  const button = document.getElementById('showPhoneBtn');
  
  if (phoneElement.classList.contains('show')) {
    phoneElement.classList.remove('show');
    button.textContent = 'Показать телефон';
  } else {
    phoneElement.classList.add('show');
    button.textContent = 'Скрыть телефон';
    
    // Закрытие при клике вне элемента
    setTimeout(() => {
      document.addEventListener('click', function closePhone(e) {
        if (!phoneElement.contains(e.target) && e.target !== button) {
          phoneElement.classList.remove('show');
          button.textContent = 'Показать телефон';
          document.removeEventListener('click', closePhone);
        }
      });
    }, 0);
  }
}