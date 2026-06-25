// AUREX OS v3 SCRIPT

const backgrounds = [
    { id: 'matrix', name: 'МАТРИЦА', type: 'canvas' },
    { id: 'stars', name: 'КОСМОС', type: 'canvas' },
    { id: 'video', name: 'ВИДЕО-ФОН', type: 'video', src: '/static/assets/bg_dance.mp4' },
    { id: 'cyber_grid', name: 'КИБЕР СЕТКА', type: 'css' },
    { id: 'neon_fluid', name: 'НЕОНОВЫЙ ПОТОК', type: 'css' },
    { id: 'blood_rain', name: 'КРОВАВЫЙ ДОЖДЬ', type: 'canvas' },
    { id: 'tv_static', name: 'БЕЛЫЙ ШУМ', type: 'canvas' },
    { id: 'pulse', name: 'ПСИХОЗ', type: 'css' },
    { id: 'laser', name: 'ЛАЗЕРЫ', type: 'canvas' },
    { id: 'plasma', name: 'ПЛАЗМА', type: 'css' }
];

let currentAnimationId = null;
let canvasAnimationRef = null;

function initDashboard() {
    initCursor();
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
// CUSTOM CURSOR
// ════════════════════════════════════════════════
function initCursor() {
    const dot = document.getElementById('cursor-dot');
    const outline = document.getElementById('cursor-outline');
    
    window.addEventListener('mousemove', (e) => {
        dot.style.left = e.clientX + 'px';
        dot.style.top = e.clientY + 'px';
        
        // Slight delay for outline
        setTimeout(() => {
            outline.style.left = e.clientX + 'px';
            outline.style.top = e.clientY + 'px';
        }, 50);
    });

    document.querySelectorAll('button, a, input, .nav-tab, .bg-thumb, .side-panel-handle').forEach(el => {
        el.addEventListener('mouseenter', () => outline.classList.add('cursor-hover'));
        el.addEventListener('mouseleave', () => outline.classList.remove('cursor-hover'));
    });
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
        
        if(bg.id === 'matrix') div.style.background = '#003300';
        else if(bg.id === 'stars') div.style.background = '#000022';
        else if(bg.id === 'cyber_grid') div.style.background = '#110022';
        else if(bg.id === 'neon_fluid') div.style.background = 'linear-gradient(45deg, #ff00cc, #3333ff)';
        else if(bg.id === 'blood_rain') div.style.background = '#330000';
        else if(bg.id === 'tv_static') div.style.background = '#555';
        else if(bg.id === 'pulse') div.style.background = 'radial-gradient(circle, #ff0033, #000)';
        else if(bg.id === 'laser') div.style.background = '#001133';
        else if(bg.id === 'plasma') div.style.background = 'radial-gradient(circle at center, #00ffff, #ff00ff)';
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
    
    if (bg.type === 'video') {
        cssLayer.innerHTML = `
            <video autoplay loop muted playsinline style="width:100vw; height:100vh; object-fit:cover;">
                <source src="${bg.src}" type="video/mp4">
            </video>`;
    }
    else if (bg.type === 'canvas') {
        canvas.style.display = 'block';
        if (bg.id === 'matrix') drawMatrix(canvas, ctx, '#00ffcc');
        if (bg.id === 'blood_rain') drawMatrix(canvas, ctx, '#ff0033');
        if (bg.id === 'stars') drawStars(canvas, ctx);
        if (bg.id === 'tv_static') drawStatic(canvas, ctx);
        if (bg.id === 'laser') drawLasers(canvas, ctx);
    }
    else if (bg.type === 'css') {
        if (bg.id === 'cyber_grid') drawCyberGrid(cssLayer);
        if (bg.id === 'neon_fluid') drawNeonFluid(cssLayer);
        if (bg.id === 'pulse') drawPulse(cssLayer);
        if (bg.id === 'plasma') drawPlasma(cssLayer);
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

function drawMatrix(canvas, ctx, color) {
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
        ctx.fillStyle = color;
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

function drawStatic(canvas, ctx) {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    function draw() {
        const imgData = ctx.createImageData(canvas.width, canvas.height);
        const data = imgData.data;
        for(let i = 0; i < data.length; i += 4) {
            const v = Math.random() * 255;
            data[i] = v; data[i+1] = v; data[i+2] = v; data[i+3] = 255;
        }
        ctx.putImageData(imgData, 0, 0);
        canvasAnimationRef = requestAnimationFrame(draw);
    }
    draw();
}

function drawLasers(canvas, ctx) {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    let lasers = [];
    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        if(Math.random() > 0.8) {
            lasers.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                w: Math.random() > 0.5 ? canvas.width : 2,
                h: Math.random() > 0.5 ? 2 : canvas.height,
                life: 1.0
            });
        }
        
        for(let i=lasers.length-1; i>=0; i--) {
            let l = lasers[i];
            ctx.fillStyle = `rgba(0, 255, 204, ${l.life})`;
            ctx.shadowBlur = 20;
            ctx.shadowColor = '#00ffcc';
            ctx.fillRect(l.w===2 ? l.x : 0, l.h===2 ? l.y : 0, l.w, l.h);
            ctx.shadowBlur = 0;
            l.life -= 0.1;
            if(l.life <= 0) lasers.splice(i, 1);
        }
        canvasAnimationRef = requestAnimationFrame(draw);
    }
    draw();
}

function drawPulse(container) {
    container.style.background = 'radial-gradient(circle at center, #330000 0%, #000000 100%)';
    container.style.animation = 'pulseBg 2s infinite alternate';
    if(!document.getElementById('pulse-style')) {
        const style = document.createElement('style');
        style.id = 'pulse-style';
        style.innerHTML = `@keyframes pulseBg { 0% { transform: scale(1); filter: brightness(1); } 100% { transform: scale(1.1); filter: brightness(2); } }`;
        document.head.appendChild(style);
    }
}

function drawPlasma(container) {
    container.style.background = 'radial-gradient(circle at 50% 50%, rgba(255,0,255,0.5), transparent 50%), radial-gradient(circle at 20% 30%, rgba(0,255,255,0.5), transparent 50%)';
    container.style.backgroundColor = '#000';
    container.style.animation = 'plasmaMove 10s infinite alternate linear';
    if(!document.getElementById('plasma-style')) {
        const style = document.createElement('style');
        style.id = 'plasma-style';
        style.innerHTML = `@keyframes plasmaMove { 0% { background-position: 0% 0%, 0% 0%; } 100% { background-position: 100% 100%, -50% 50%; } }`;
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
        
        // Randomize Ping and Meters
        document.getElementById('ping-count').innerText = Math.floor(Math.random() * 30 + 5) + " ms";
        document.getElementById('cpu-fill').style.width = Math.floor(Math.random() * 80 + 20) + "%";
        document.getElementById('ram-fill').style.width = Math.floor(Math.random() * 50 + 40) + "%";
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
