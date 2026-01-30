const imageInput = document.getElementById('images_id');
const preview = document.getElementById('imagePreview');

imageInput.addEventListener('change', () => {
  preview.innerHTML = '';

  Array.from(imageInput.files).forEach(file => {
    const reader = new FileReader();

    reader.onload = e => {
      const img = document.createElement('img');
      img.src = e.target.result;
      preview.appendChild(img);
    };

    reader.readAsDataURL(file);
  });
});