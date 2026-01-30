document.addEventListener('DOMContentLoaded', function() {
  const passwordFields = document.querySelectorAll('.password-field');
  
  const avatarIcon = document.querySelector('.avatar img');
  
  passwordFields.forEach(field => {
    const passwordInput = field.querySelector('input[type="password"]');
    const eyeIcon = field.querySelector('.eye img');
    
    if (passwordInput && eyeIcon) {
      eyeIcon.addEventListener('click', function() {
        const isHidden = passwordInput.type === 'password';
        passwordInput.type = isHidden ? 'text' : 'password';
        
        eyeIcon.src = isHidden
          ? '/static/assets/images/icons/opened-eye.svg'
          : '/static/assets/images/icons/closed-eye.svg';

        if (avatarIcon) {
          avatarIcon.src = isHidden
            ? '/static/assets/images/icons/bird-open-svg.svg'
            : '/static/assets/images/icons/bird-log.svg';
        }
      });
    }
  });
});