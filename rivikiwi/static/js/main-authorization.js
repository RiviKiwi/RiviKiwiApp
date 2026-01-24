const passwordFields = document.querySelectorAll('.password-field');

passwordFields.forEach(field => {
  const passwordInput = field.querySelector('input');
  const eyeIcon = field.querySelector('.eye img');
  
  if (passwordInput && eyeIcon) {
    eyeIcon.addEventListener('click', () => {
      const isHidden = passwordInput.type === 'password';
      
      passwordInput.type = isHidden ? 'text' : 'password';
      eyeIcon.src = isHidden
        ? '/images/icons/opened-eye.svg'
        : '/images/icons/closed-eye.svg';
    });
  }
});