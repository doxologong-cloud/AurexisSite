// Анимация часов HUD
function updateClock() {
    const now = new Date();
    // Добавляем искусственные "миллисекунды" для создания эффекта быстрых вычислений
    const ms = String(Math.floor(Math.random() * 99)).padStart(2, '0'); 
    
    const timeString = 
        String(now.getHours()).padStart(2, '0') + ':' +
        String(now.getMinutes()).padStart(2, '0') + ':' +
        String(now.getSeconds()).padStart(2, '0') + ':' + 
        ms;
        
    document.getElementById('clock').textContent = timeString;
    requestAnimationFrame(updateClock);
}
updateClock();

// Эффект печатной машинки
const phrases = [
    "УСТАНОВКА СВЯЗИ СО ВРЕМЕНЕМ...",
    "АНАЛИЗ ВЕРОЯТНОСТЕЙ...",
    "РАСПАКОВКА ДАННЫХ ИЗ 2077 ГОДА.",
    "БУДУЩЕЕ УЖЕ ЗДЕСЬ."
];

const typeWriterElement = document.getElementById('typewriter');
let phraseIndex = 0;
let charIndex = 0;
let isDeleting = false;

function typeWriter() {
    const currentPhrase = phrases[phraseIndex];
    
    if (isDeleting) {
        typeWriterElement.textContent = currentPhrase.substring(0, charIndex - 1);
        charIndex--;
    } else {
        typeWriterElement.textContent = currentPhrase.substring(0, charIndex + 1);
        charIndex++;
    }

    let typeSpeed = 50; // Скорость печати
    if (isDeleting) { typeSpeed /= 2; } // Удаляем быстрее

    if (!isDeleting && charIndex === currentPhrase.length) {
        // Пауза перед удалением
        typeSpeed = 2000;
        if (phraseIndex === phrases.length - 1) {
            // Если это последняя фраза - оставляем её
            return; 
        }
        isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        phraseIndex++;
        typeSpeed = 500;
    }

    setTimeout(typeWriter, typeSpeed);
}

// Запускаем печать через секунду
setTimeout(typeWriter, 1000);

// Интерактивный глитч-эффект при нажатии кнопки
function triggerGlitch() {
    const wrapper = document.querySelector('.content-wrapper');
    const btn = document.querySelector('.cyber-btn');
    const oldText = btn.innerHTML;
    
    // Визуальный сбой
    wrapper.style.transform = 'translate(' + (Math.random() * 20 - 10) + 'px, ' + (Math.random() * 20 - 10) + 'px) skewX(' + (Math.random() * 10) + 'deg)';
    wrapper.style.filter = 'hue-rotate(' + (Math.random() * 360) + 'deg) contrast(150%)';
    
    btn.innerHTML = "<span>[ СИНХРОНИЗАЦИЯ... ]</span>";
    
    setTimeout(() => {
        wrapper.style.transform = 'none';
        wrapper.style.filter = 'none';
        btn.innerHTML = "<span>[ ПЕРЕДАЧА УСПЕШНА ]</span>";
        btn.style.color = "#ff003c";
        btn.style.borderColor = "#ff003c";
        
        setTimeout(() => {
            btn.innerHTML = oldText;
            btn.style.color = "";
            btn.style.borderColor = "";
        }, 2000);
    }, 150);
}
