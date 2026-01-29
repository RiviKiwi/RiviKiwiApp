const passwordFields = document.querySelectorAll('.password-field');

passwordFields.forEach(field => {
  const passwordInput = field.querySelector('input');
  const eyeIcon = field.querySelector('.eye img');
  
  if (passwordInput && eyeIcon) {
    // Сохраняем изначальные пути к изображениям
    const closedEyePath = eyeIcon.src;
    const openedEyePath = closedEyePath.replace('closed-eye.svg', 'opened-eye.svg');

    eyeIcon.addEventListener('click', () => {
      const isHidden = passwordInput.type === 'password';
      
      passwordInput.type = isHidden ? 'text' : 'password';
      eyeIcon.src = isHidden ? openedEyePath : closedEyePath;
    });
  }
});
