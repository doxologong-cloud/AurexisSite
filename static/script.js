// AUREX OS v3 SCRIPT

const backgrounds = [
    { id: 'matrix', name: 'МАТРИЦА (АНИМАЦИЯ)', type: 'canvas' },
    { id: 'stars', name: 'КОСМОС (АНИМАЦИЯ)', type: 'canvas' },
    { id: 'video', name: 'ВИДЕО-ФОН', type: 'video', src: '/static/assets/bg_dance.mp4' },
    { id: 'cyber_grid', name: 'КИБЕР СЕТКА', type: 'css' },
    { id: 'neon_fluid', name: 'НЕОНОВЫЙ ПОТОК', type: 'css' },
    { id: 'img_1', name: 'ХАКЕР', type: 'image', src: 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=2070&auto=format&fit=crop' },
    { id: 'img_2', name: 'АБСТРАКЦИЯ', type: 'image', src: 'https://images.unsplash.com/photo-1614729939124-032f0b56c9ce?q=80&w=2070&auto=format&fit=crop' },
    { id: 'img_3', name: 'ГОРОД', type: 'image', src: 'https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=2070&auto=format&fit=crop' },
    { id: 'img_4', name: 'РЕТРО', type: 'image', src: 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=2070&auto=format&fit=crop' },
    { id: 'img_5', name: 'ЧЕРНАЯ ДЫРА', type: 'image', src: 'https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2045&auto=format&fit=crop' }
];

let currentAnimationId = null;
let canvasAnimationRef = null;

function initDashboard() {
    initThemePicker();
    loadTelegram();
    initPanelLogs();
    initGlobe();
    
    // Load saved BG
    const savedBgId = localStorage.getItem('aurex_bg_id') || 'matrix';
    setTheme(savedBgId);
    
    // Load Tint
    const savedColor = localStorage.getItem('aurex_tint_color') || '#000000';
    const savedOpacity = localStorage.getItem('aurex_tint_opacity') || '0.5';
    document.getElementById('tint-color').value = savedColor;
    document.getElementById('tint-opacity').value = savedOpacity;
    updateTint();
}

// ════════════════════════════════════════════════
// THEME & BACKGROUND LOGIC
// ════════════════════════════════════════════════

function initThemePicker() {
    const grid = document.getElementById('bg-grid');
    if(!grid) return;
    
    backgrounds.forEach(bg => {
        const div = document.createElement('div');
        div.className = 'bg-thumb';
        div.id = `thumb-${bg.id}`;
        
        if(bg.type === 'image') div.style.backgroundImage = `url('${bg.src}')`;
        else if(bg.id === 'matrix') div.style.background = '#003300';
        else if(bg.id === 'stars') div.style.background = '#000022';
        else if(bg.id === 'cyber_grid') div.style.background = '#110022';
        else if(bg.id === 'neon_fluid') div.style.background = 'linear-gradient(45deg, #ff00cc, #3333ff)';
        else if(bg.type === 'video') div.style.background = '#333';
        
        div.innerHTML = `<span>${bg.name}</span>`;
        div.onclick = () => setTheme(bg.id);
        grid.appendChild(div);
    });
}

function setTheme(id) {
    localStorage.setItem('aurex_bg_id', id);
    document.querySelectorAll('.bg-thumb').forEach(el => el.classList.remove('active'));
    const thumb = document.getElementById(`thumb-${id}`);
    if(thumb) thumb.classList.add('active');
    
    const bg = backgrounds.find(b => b.id === id);
    if(!bg) return;
    
    // Reset all layers
    cancelAnimationFrame(canvasAnimationRef);
    const canvas = document.getElementById('bg-canvas');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    canvas.style.display = 'none';
    
    const cssLayer = document.getElementById('bg-css-layer');
    cssLayer.style.backgroundImage = 'none';
    cssLayer.style.background = 'transparent';
    cssLayer.innerHTML = '';
    
    if(bg.type === 'image') {
        cssLayer.style.backgroundImage = `url('${bg.src}')`;
    } 
    else if (bg.type === 'video') {
        cssLayer.innerHTML = `
            <video autoplay loop muted playsinline style="width:100vw; height:100vh; object-fit:cover;">
                <source src="${bg.src}" type="video/mp4">
            </video>`;
    }
    else if (bg.type === 'canvas') {
        canvas.style.display = 'block';
        if (bg.id === 'matrix') drawMatrix(canvas, ctx);
        if (bg.id === 'stars') drawStars(canvas, ctx);
    }
    else if (bg.type === 'css') {
        if (bg.id === 'cyber_grid') drawCyberGrid(cssLayer);
        if (bg.id === 'neon_fluid') drawNeonFluid(cssLayer);
    }
}

function updateTint() {
    const hex = document.getElementById('tint-color').value;
    const alpha = document.getElementById('tint-opacity').value;
    const r = parseInt(hex.slice(1,3), 16) || 0;
    const g = parseInt(hex.slice(3,5), 16) || 0;
    const b = parseInt(hex.slice(5,7), 16) || 0;
    document.getElementById('bg-overlay').style.backgroundColor = `rgba(${r}, ${g}, ${b}, ${alpha})`;
    localStorage.setItem('aurex_tint_color', hex);
    localStorage.setItem('aurex_tint_opacity', alpha);
}

// ════════════════════════════════════════════════
// CANVAS ANIMATIONS
// ════════════════════════════════════════════════

function drawMatrix(canvas, ctx) {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレゲゼデベペオォコソトノホモヨョロゴゾドボポヴッン';
    const latin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const nums = '0123456789';
    const alphabet = katakana + latin + nums;
    const fontSize = 16;
    const columns = canvas.width / fontSize;
    const drops = [];
    for(let x = 0; x < columns; x++) drops[x] = 1;

    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00ffcc';
        ctx.font = fontSize + 'px monospace';
        for(let i = 0; i < drops.length; i++) {
            const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
        canvasAnimationRef = requestAnimationFrame(draw);
    }
    draw();
}

function drawStars(canvas, ctx) {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const stars = [];
    for(let i=0; i<800; i++) {
        stars.push({
            x: Math.random() * canvas.width - canvas.width/2,
            y: Math.random() * canvas.height - canvas.height/2,
            z: Math.random() * canvas.width
        });
    }
    let speed = 2;
    function draw() {
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#ffffff';
        const cx = canvas.width / 2;
        const cy = canvas.height / 2;
        stars.forEach(star => {
            star.z -= speed;
            if (star.z <= 0) {
                star.z = canvas.width;
                star.x = Math.random() * canvas.width - cx;
                star.y = Math.random() * canvas.height - cy;
            }
            const k = 128.0 / star.z;
            const px = star.x * k + cx;
            const py = star.y * k + cy;
            if (px >= 0 && px <= canvas.width && py >= 0 && py <= canvas.height) {
                const size = (1 - star.z / canvas.width) * 3;
                ctx.beginPath();
                ctx.arc(px, py, size, 0, Math.PI * 2);
                ctx.fill();
            }
        });
        canvasAnimationRef = requestAnimationFrame(draw);
    }
    draw();
}

function drawCyberGrid(container) {
    container.innerHTML = `
    <style>
        .grid-wrap { perspective: 1000px; width: 100vw; height: 100vh; background: #000; overflow: hidden; position: absolute; }
        .grid-plane { width: 200%; height: 200%; position: absolute; bottom: -50%; left: -50%;
            background-image: linear-gradient(rgba(0, 255, 204, 0.5) 2px, transparent 2px), linear-gradient(90deg, rgba(0, 255, 204, 0.5) 2px, transparent 2px);
            background-size: 100px 100px; transform: rotateX(75deg); animation: moveGrid 3s linear infinite; }
        @keyframes moveGrid { 0% { transform: rotateX(75deg) translateY(0); } 100% { transform: rotateX(75deg) translateY(100px); } }
    </style>
    <div class="grid-wrap"><div class="grid-plane"></div></div>`;
}

function drawNeonFluid(container) {
    container.style.background = 'linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab)';
    container.style.backgroundSize = '400% 400%';
    container.style.animation = 'fluidGradient 15s ease infinite';
    if(!document.getElementById('fluid-style')) {
        const style = document.createElement('style');
        style.id = 'fluid-style';
        style.innerHTML = `@keyframes fluidGradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }`;
        document.head.appendChild(style);
    }
}

// ════════════════════════════════════════════════
// UI LOGIC
// ════════════════════════════════════════════════

function switchTab(tabId) {
    document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
    document.querySelector(`.nav-tab[onclick="switchTab('${tabId}')"]`).classList.add('active');
    document.getElementById(`tab-${tabId}`).style.display = 'block';
}

function logout() {
    fetch('/api/logout', {method: 'POST'}).then(() => window.location.href = '/');
}

// ════════════════════════════════════════════════
// TELEGRAM
// ════════════════════════════════════════════════

function loadTelegram() {
    fetch('/api/telegram').then(r=>r.json()).then(data => {
        if(data.success) {
            document.getElementById('tg-name').value = data.profile.name;
            document.getElementById('tg-bio').value = data.profile.bio;
            if(data.profile.avatar) {
                document.getElementById('tg-avatar-img').src = data.profile.avatar;
                document.getElementById('header-avatar').src = data.profile.avatar;
            }
            document.getElementById('header-name').innerText = data.profile.name || '@USER';
        }
    });
}

function saveTelegram() {
    const name = document.getElementById('tg-name').value;
    const bio = document.getElementById('tg-bio').value;
    const avatar = document.getElementById('tg-avatar-img').src;
    
    fetch('/api/telegram', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name, bio, avatar})
    }).then(r=>r.json()).then(data => {
        if(data.success) {
            document.getElementById('header-name').innerText = name;
            document.getElementById('header-avatar').src = avatar;
            const status = document.getElementById('tg-save-status');
            status.innerText = 'Сохранено успешно!';
            status.style.color = '#00ffcc';
            setTimeout(() => status.innerText='', 3000);
        }
    });
}

function updateAvatar(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('tg-avatar-img').src = e.target.result;
        }
        reader.readAsDataURL(input.files[0]);
    }
}

// ════════════════════════════════════════════════
// BOTNET PANEL
// ════════════════════════════════════════════════

function initPanelLogs() {
    const logs = document.getElementById('fake-logs');
    if(!logs) return;
    const msgs = [
        "Connection established to remote node...",
        "Bypassing firewall...",
        "Extracting Telegram session tokens...",
        "Roblox cookies retrieved (n=204).",
        "Uploading payload to C2 server...",
        "Access granted.",
        "System check: Nominal."
    ];
    setInterval(() => {
        const msg = document.createElement('div');
        msg.innerText = `> ${new Date().toLocaleTimeString()} - ${msgs[Math.floor(Math.random()*msgs.length)]}`;
        logs.appendChild(msg);
        if(logs.childNodes.length > 5) logs.removeChild(logs.firstChild);
    }, 1500);
    setInterval(() => {
        document.getElementById('node-count').innerText = (14000 + Math.floor(Math.random()*500)).toLocaleString();
        document.getElementById('traffic').innerText = (1.0 + Math.random()).toFixed(2) + " TB/s";
    }, 3000);
}

function initGlobe() {
    const container = document.getElementById('globe-container');
    if(!container || !window.THREE) return;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({alpha: true, antialias: true});
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);
    
    const geometry = new THREE.SphereGeometry( 2, 24, 24 );
    const material = new THREE.MeshBasicMaterial( { color: 0x00ffcc, wireframe: true, transparent: true, opacity: 0.15 } );
    const sphere = new THREE.Mesh( geometry, material );
    scene.add( sphere );
    
    const dotsGeo = new THREE.BufferGeometry();
    const posArray = new Float32Array(800 * 3);
    for(let i=0; i<800*3; i+=3) {
        const u = Math.random();
        const v = Math.random();
        const theta = 2 * Math.PI * u;
        const phi = Math.acos(2 * v - 1);
        const r = 2.02;
        posArray[i] = r * Math.sin(phi) * Math.cos(theta);
        posArray[i+1] = r * Math.sin(phi) * Math.sin(theta);
        posArray[i+2] = r * Math.cos(phi);
    }
    dotsGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    const dotsMat = new THREE.PointsMaterial({size: 0.04, color: 0xff0033, transparent: true, opacity: 0.8});
    const particles = new THREE.Points(dotsGeo, dotsMat);
    scene.add(particles);
    camera.position.z = 5.5;
    
    function animate() {
        requestAnimationFrame( animate );
        sphere.rotation.y += 0.003;
        sphere.rotation.x += 0.001;
        particles.rotation.y += 0.003;
        particles.rotation.x += 0.001;
        renderer.render( scene, camera );
    }
    animate();
}

document.addEventListener('DOMContentLoaded', initDashboard);
