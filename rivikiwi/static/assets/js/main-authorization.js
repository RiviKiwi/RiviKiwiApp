const passwordFields = document.querySelectorAll('.password-field');

passwordFields.forEach(field => {
  const passwordInput = field.querySelector('input');
  const eyeIcon = field.querySelector('.eye img');
  const avatarIcon = document.querySelector('.avatar img');
  
  if (passwordInput && eyeIcon && avatarIcon) {
    // Сохраняем изначальные пути к изображениям
    const closedEyePath = eyeIcon.src;
    const openedEyePath = closedEyePath.replace('closed-eye.svg', 'opened-eye.svg');
    const birdLogPath = avatarIcon.src;
    const birdOpenPath = birdLogPath.replace('bird-log.png', 'bird-open-svg.svg');

    eyeIcon.addEventListener('click', () => {
      const isHidden = passwordInput.type === 'password';
      
      passwordInput.type = isHidden ? 'text' : 'password';
      eyeIcon.src = isHidden ? openedEyePath : closedEyePath;
      avatarIcon.src = isHidden ? birdOpenPath : birdLogPath;
    });
  }
});