// script.js

// 1. Инициализация иконок Lucide
lucide.createIcons();

// 2. Логика мобильного меню
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('mobile-menu-btn');
    const menu = document.getElementById('mobile-menu');

    btn.addEventListener('click', () => {
        menu.classList.toggle('hidden');
        
        // Меняем иконку (опционально, для простоты просто переключаем класс)
        if (menu.classList.contains('hidden')) {
            // Меню закрыто
            btn.innerHTML = '<i data-lucide="menu" class="w-6 h-6"></i>';
        } else {
            // Меню открыто
            btn.innerHTML = '<i data-lucide="x" class="w-6 h-6"></i>';
        }
        lucide.createIcons(); // Перерисовываем иконку после смены HTML
    });
});

// 3. Инициализация графика (Chart.js)
const ctx = document.getElementById('statsChart').getContext('2d');

// Градиент для заливки графика
const gradient = ctx.createLinearGradient(0, 0, 0, 300);
gradient.addColorStop(0, 'rgba(132, 204, 22, 0.5)'); // Lime-500
gradient.addColorStop(1, 'rgba(132, 204, 22, 0)');

const statsChart = new Chart(ctx, {
    type: 'line', // Используем line с заливкой вместо Area
    data: {
        labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл'],
        datasets: [{
            label: 'Новые объявления',
            data: [4000, 5500, 8000, 12000, 18000, 25000, 35000],
            borderColor: '#84cc16', // Цвет линии (Lime-500)
            backgroundColor: gradient,
            borderWidth: 3,
            tension: 0.4, // Плавность линий (curved)
            fill: true,
            pointBackgroundColor: '#ffffff',
            pointBorderColor: '#84cc16',
            pointRadius: 4,
            pointHoverRadius: 6
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                backgroundColor: 'rgba(15, 23, 42, 0.9)', // Slate-900
                titleColor: '#fff',
                bodyColor: '#fff',
                padding: 10,
                displayColors: false
            }
        },
        scales: {
            x: {
                grid: {
                    display: false,
                    drawBorder: false
                },
                ticks: {
                    color: '#94a3b8' // Slate-400
                }
            },
            y: {
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)',
                    borderDash: [5, 5]
                },
                ticks: {
                    color: '#94a3b8',
                    callback: function(value) {
                        return value / 1000 + 'k'; // Форматирование 4000 -> 4k
                    }
                },
                border: {
                    display: false
                }
            }
        }
    }
});