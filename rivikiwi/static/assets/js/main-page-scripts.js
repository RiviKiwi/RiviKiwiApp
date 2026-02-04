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
// document.addEventListener('DOMContentLoaded', () => {
//   const navContainer = document.querySelector('.categories-container');
//   navContainer.addEventListener('click', (event) => {
//     const clickedLink = event.target.closest('.cat-link');
    
//     if (clickedLink) {
//       event.preventDefault();
//       document.querySelectorAll('.cat-link').forEach(link => link.classList.remove('active'));
//       clickedLink.classList.add('active');
//     }
//   });
  
// });

/* Сортировка товаров */
function toggleSortMenu() {
    document.getElementById('sortDropdown').classList.toggle('show');
}

function selectSort(sortName) {
    document.getElementById('currentSort').innerText = sortName;
    document.getElementById('sortDropdown').classList.remove('show');
    console.log("Выбрана сортировка:", sortName);
}
/* Меню профиля в углу */
function showAccountMenu() {
    const dropdown = document.getElementById('accountDropdown');
    dropdown.classList.toggle('show');
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
    window.onclick = function(event) {
    if (!event.target.closest('.account-wrapper')) {
      const dropdown = document.getElementById('accountDropdown');
      if (dropdown.classList.contains('show')) {
        dropdown.classList.remove('show');
      }
    }
}
}

const fromInput = document.getElementById('price-from');
const toInput = document.getElementById('price-to');

fromInput.addEventListener('input', function() {
    toInput.min = this.value;
    
    if (toInput.value && parseFloat(toInput.value) < parseFloat(this.value)) {
        toInput.value = this.value; 
    }
});

function markFavorite(button,event) {
    button.classList.toggle('favorite-product');
    event.preventDefault();
    event.stopPropagation();
    if (button.classList.contains('favorite-product')) {
        console.log("Добавлено в избранное");
    } else {
        console.log("Удалено из избранного");
    }
}

const viewElements = document.querySelectorAll('.product-views p');
const formatter = new Intl.NumberFormat('en-US', {
notation: "compact",
maximumFractionDigits: 1
});

viewElements.forEach(el => {
const originalValue = parseInt(el.textContent.replace(/\s/g, ''));
if (!isNaN(originalValue)) {
    el.textContent = formatter.format(originalValue).toLowerCase(); 
}
});

function submitSortForm(sortValue) {
    const input = document.getElementById('order_by_input');
    input.value = sortValue;
    document.getElementById('sort-form').submit();
}

function selectCityWithSubmit(cityName) {
    document.querySelector('.current-city').innerText = cityName;
    document.getElementById('cityDropdown').classList.remove('show');
    
    // Get all forms that need to be updated
    const forms = ['city-form', 'sort-form'].map(id => document.getElementById(id)).filter(Boolean);
    
    forms.forEach(form => {
        // Get or create the city input
        let cityInput = form.querySelector('input[name="city"]');
        if (!cityInput) {
            cityInput = document.createElement('input');
            cityInput.type = 'hidden';
            cityInput.name = 'city';
            form.appendChild(cityInput);
        }
        
        // Update the city value
        cityInput.value = cityName;
    });

    // Submit the main filter form
    const cityForm = document.getElementById('city-form');
    if (cityForm) {
        cityForm.submit();
    }
}