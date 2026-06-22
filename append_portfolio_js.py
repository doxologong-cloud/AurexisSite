import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

portfolio_js = """
// ==========================================
// PORTFOLIO 3D TILT
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    // Navigate to portfolio
    document.querySelector('a[href="#portfolio"]')?.addEventListener('click', (e) => {
        e.preventDefault();
        showView('view-portfolio');
    });

    const cards = document.querySelectorAll('.tilt-card');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = ((y - centerY) / centerY) * -10;
            const rotateY = ((x - centerX) / centerX) * 10;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
            card.style.boxShadow = `${-rotateY}px ${rotateX}px 20px rgba(0, 255, 136, 0.2)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
            card.style.boxShadow = 'none';
        });
    });
});
"""

if 'PORTFOLIO 3D TILT' not in text:
    with open('static/script.js', 'a', encoding='utf-8') as f:
        f.write('\n' + portfolio_js)
    print("Added Portfolio JS")
else:
    print("Portfolio JS already exists")
