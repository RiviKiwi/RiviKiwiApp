const imageInput = document.getElementById('images_id');
const preview = document.getElementById('imagePreview');
const form = document.querySelector('.create-ad-form');

let uploadedFiles = [];

imageInput.addEventListener('change', () => {
  const newFiles = Array.from(imageInput.files);
  
  newFiles.forEach(file => {
    if (!file.type.startsWith('image/')) return;
    uploadedFiles.push(file);

    const reader = new FileReader();
    reader.onload = e => {
      const wrapper = document.createElement('div');
      wrapper.className = 'image-item';

      const img = document.createElement('img');
      img.src = e.target.result;

      const btn = document.createElement('button');
      btn.className = 'remove-btn';
      btn.innerHTML = '&times;';
      btn.type = "button";

      // ЛОГИКА УДАЛЕНИЯ
      btn.onclick = () => {
        wrapper.remove(); 
        uploadedFiles = uploadedFiles.filter(f => f !== file);
        updateInputFiles();
      };

      wrapper.appendChild(img);
      wrapper.appendChild(btn);
      preview.appendChild(wrapper);
    };
    reader.readAsDataURL(file);
  });
  imageInput.value = '';
  updateInputFiles();
});

function updateInputFiles() {
  const dataTransfer = new DataTransfer();
  uploadedFiles.forEach(file => {
    dataTransfer.items.add(file);
  });
  imageInput.files = dataTransfer.files;
}