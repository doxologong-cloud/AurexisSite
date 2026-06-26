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

// Animated Counter
function animateCounter(id, start, end, duration) {
    let obj = document.getElementById(id);
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start).toLocaleString();
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Start counter when visible
const observer = new IntersectionObserver((entries) => {
    if(entries[0].isIntersecting) {
        animateCounter("dl-counter", 8000, 8421, 2000);
        observer.disconnect();
    }
});
observer.observe(document.getElementById("dl-counter"));

