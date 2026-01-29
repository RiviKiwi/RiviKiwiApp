const avatarInput = document.getElementById('avatarInput');
const avatarPreview = document.getElementById('avatarPreview');

avatarInput.addEventListener('change', () => {
  const file = avatarInput.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = () => {
    avatarPreview.src = reader.result;
  };
  reader.readAsDataURL(file);
});

document.addEventListener('DOMContentLoaded', () => {
  const editBtn = document.getElementById('editProfileBtn');
  const editWrapper = document.getElementById('profileEditWrapper');

  // если элементов нет — просто выходим (без ошибок)
  if (!editBtn || !editWrapper) return;

  editBtn.addEventListener('click', () => {
    editWrapper.classList.toggle('open');

    editBtn.textContent = editWrapper.classList.contains('open')
      ? 'Скрыть редактирование'
      : 'Редактировать профиль';
  });
});


