let currentSlide = 0; // Глобальная переменная для хранения текущего слайда

function moveSlide(direction) {
    const descriptions = document.querySelectorAll('.slide-description');
    const images = document.querySelectorAll('.slide-image');

    if (descriptions.length === 0 || images.length === 0) {
        console.error('No slides found');
        return;
    }

    // Убрать активные классы
    descriptions[currentSlide].classList.remove('active');
    images[currentSlide].classList.remove('active');

    // Вычислить новый индекс
    currentSlide = (currentSlide + direction + descriptions.length) % descriptions.length;

    // Добавить активные классы
    descriptions[currentSlide].classList.add('active');
    images[currentSlide].classList.add('active');
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('.prev_cabin').addEventListener('click', function () {
        moveSlide(-1);
    });

    document.querySelector('.next_cabin').addEventListener('click', function () {
        moveSlide(1);
    });
});
