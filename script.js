document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById('dust-container');
    
    // Создаем пыль и искры от стройки
    for(let i = 0; i < 60; i++) {
        let dust = document.createElement('div');
        dust.className = 'dust';
        
        // Случайный размер, позиция и скорость
        const size = Math.random() * 8 + 2;
        dust.style.width = size + 'px';
        dust.style.height = size + 'px';
        
        dust.style.left = Math.random() * 100 + 'vw';
        dust.style.top = Math.random() * 100 + 'vh';
        
        dust.style.animationDuration = (Math.random() * 5 + 3) + 's';
        dust.style.animationDelay = (Math.random() * 5) + 's';
        
        // Иногда пыль превращается в золотые строительные искры
        if (Math.random() > 0.7) {
            dust.style.background = 'rgba(255, 215, 0, 0.8)';
            dust.style.boxShadow = '0 0 10px #ff8c00';
            dust.style.filter = 'none';
            dust.style.animationDuration = (Math.random() * 2 + 1) + 's'; // Искры летят быстрее
        }
        
        container.appendChild(dust);
    }
    
    // Эффект "сотрясания" камеры при ударе киркой
    setInterval(() => {
        document.body.style.transform = "translate(2px, 2px)";
        setTimeout(() => {
            document.body.style.transform = "none";
        }, 50);
    }, 2000); // Синхронизировано с анимацией hammerImpact (2s)
});
