// Add smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Dynamic background effect based on mouse movement
document.addEventListener('mousemove', (e) => {
    const bg = document.querySelector('.background-animation');
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;
    
    // Slight background shift
    document.body.style.background = `radial-gradient(circle at ${mouseX * 100}% ${mouseY * 100}%, #161b22 0%, #0d1117 50%)`;
});
