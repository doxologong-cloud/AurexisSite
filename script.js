// Создаем красивые плавающие частицы на фоне
document.addEventListener("DOMContentLoaded", () => {
    const body = document.body;
    
    for (let i = 0; i < 40; i++) {
        let particle = document.createElement("div");
        particle.className = "particle";
        
        let size = Math.random() * 4 + 2; // от 2px до 6px
        particle.style.width = size + "px";
        particle.style.height = size + "px";
        
        particle.style.left = Math.random() * 100 + "vw";
        particle.style.animationDuration = (Math.random() * 10 + 5) + "s";
        particle.style.animationDelay = (Math.random() * 5) + "s";
        
        // Иногда делаем частицы фиолетовыми
        if (Math.random() > 0.5) {
            particle.style.background = "rgba(76, 29, 149, 0.6)";
            particle.style.boxShadow = "0 0 10px rgba(76, 29, 149, 0.8)";
        }
        
        body.appendChild(particle);
    }
});
