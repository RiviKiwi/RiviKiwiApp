/* Местоположение */
function toggleCityMenu() {
    const dropdown = document.getElementById('cityDropdown');
    dropdown.classList.toggle('show');
}

function selectCity(cityName) {
    document.querySelector('.current-city').innerText = cityName;
    document.getElementById('cityDropdown').classList.remove('show');
}

window.onclick = function(event) {
    if (!event.target.closest('.location-wrapper')) {
      const dropdown = document.getElementById('cityDropdown');
      if (dropdown.classList.contains('show')) {
        dropdown.classList.remove('show');
      }
    }
}

/* Категории товаров */
document.addEventListener('DOMContentLoaded', () => {
  const navContainer = document.querySelector('.categories-container');
  navContainer.addEventListener('click', (event) => {
    const clickedLink = event.target.closest('.cat-link');
    
    if (clickedLink) {
      event.preventDefault();
      document.querySelectorAll('.cat-link').forEach(link => link.classList.remove('active'));
      clickedLink.classList.add('active');
    }
  });
  
});
/* Сортировка товаров */
function toggleSortMenu() {
    document.getElementById('sortDropdown').classList.toggle('show');
}

function selectSort(sortName) {
    document.getElementById('currentSort').innerText = sortName;
    document.getElementById('sortDropdown').classList.remove('show');
    console.log("Выбрана сортировка:", sortName);
}

window.onclick = function(event) {
    if (!event.target.closest('.location-wrapper')) {
        const cityDrop = document.getElementById('cityDropdown');
        if (cityDrop && cityDrop.classList.contains('show')) {
            cityDrop.classList.remove('show');
        }
    }
    if (!event.target.closest('.sort-button') && !event.target.closest('.sort-dropdown')) {
        const sortDrop = document.getElementById('sortDropdown');
        if (sortDrop && sortDrop.classList.contains('show')) {
            sortDrop.classList.remove('show');
        }
    }
}
