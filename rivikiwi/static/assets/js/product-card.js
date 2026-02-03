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