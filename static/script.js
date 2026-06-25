// AUREX OS v3 SCRIPT

const backgrounds = [
    "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=2070&auto=format&fit=crop", // Cyberpunk city
    "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=2070&auto=format&fit=crop", // Circuit board
    "https://images.unsplash.com/photo-1614729939124-032f0b56c9ce?q=80&w=2070&auto=format&fit=crop", // Space nebula
    "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=2070&auto=format&fit=crop", // Matrix code
    "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2070&auto=format&fit=crop", // Abstract liquid
    "https://images.unsplash.com/photo-1515630278258-407f66498911?q=80&w=2070&auto=format&fit=crop", // Dark geometry
    "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?q=80&w=2070&auto=format&fit=crop", // Tech server room
    "https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=2070&auto=format&fit=crop", // Retro grid
    "https://images.unsplash.com/photo-1634152962476-4b8a00e1915c?q=80&w=2070&auto=format&fit=crop", // Dark gradient
    "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop", // Earth space
    "https://images.unsplash.com/photo-1605806616949-1e87b487cb2a?q=80&w=2070&auto=format&fit=crop", // Glowing neon lines
    "https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=2070&auto=format&fit=crop", // Coding screen
    "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?q=80&w=2093&auto=format&fit=crop", // Stars
    "https://images.unsplash.com/photo-1614850715649-1d0106293cb1?q=80&w=2070&auto=format&fit=crop", // Abstract 3D blocks
    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=2072&auto=format&fit=crop"  // Hacker desk
];

function initDashboard() {
    const bgGrid = document.getElementById('bg-grid');
    if(!bgGrid) return;
    
    // Load saved BG and Tint
    const savedBg = localStorage.getItem('aurex_bg') || backgrounds[0];
    const savedColor = localStorage.getItem('aurex_tint_color') || '#000000';
    const savedOpacity = localStorage.getItem('aurex_tint_opacity') || '0.5';
    
    document.getElementById('bg-container').style.backgroundImage = `url('${savedBg}')`;
    document.getElementById('tint-color').value = savedColor;
    document.getElementById('tint-opacity').value = savedOpacity;
    updateTint();

    // Populate BG picker
    backgrounds.forEach(bg => {
        const div = document.createElement('div');
        div.className = 'bg-thumb';
        div.style.backgroundImage = `url('${bg}')`;
        if(bg === savedBg) div.classList.add('active');
        
        div.onclick = () => {
            document.querySelectorAll('.bg-thumb').forEach(el => el.classList.remove('active'));
            div.classList.add('active');
            document.getElementById('bg-container').style.backgroundImage = `url('${bg}')`;
            localStorage.setItem('aurex_bg', bg);
        };
        bgGrid.appendChild(div);
    });

    loadTelegram();
    initPanelLogs();
    initGlobe();
}

function updateTint() {
    const hex = document.getElementById('tint-color').value;
    const alpha = document.getElementById('tint-opacity').value;
    
    // Convert hex to rgb
    const r = parseInt(hex.slice(1,3), 16) || 0;
    const g = parseInt(hex.slice(3,5), 16) || 0;
    const b = parseInt(hex.slice(5,7), 16) || 0;
    
    const rgba = `rgba(${r}, ${g}, ${b}, ${alpha})`;
    document.getElementById('bg-overlay').style.backgroundColor = rgba;
    
    localStorage.setItem('aurex_tint_color', hex);
    localStorage.setItem('aurex_tint_opacity', alpha);
}

function switchTab(tabId) {
    document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
    
    document.querySelector(`.nav-tab[onclick="switchTab('${tabId}')"]`).classList.add('active');
    document.getElementById(`tab-${tabId}`).style.display = 'block';
}

function logout() {
    fetch('/api/logout', {method: 'POST'}).then(() => window.location.href = '/');
}

// TELEGRAM LOGIC
function loadTelegram() {
    fetch('/api/telegram').then(r=>r.json()).then(data => {
        if(data.success) {
            document.getElementById('tg-name').value = data.profile.name;
            document.getElementById('tg-bio').value = data.profile.bio;
            if(data.profile.avatar) {
                document.getElementById('tg-avatar-img').src = data.profile.avatar;
            }
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

// PANEL LOGS
function initPanelLogs() {
    const logs = document.getElementById('fake-logs');
    if(!logs) return;
    
    const messages = [
        "Connection established to remote node...",
        "Bypassing firewall...",
        "Extracting Telegram session tokens...",
        "Roblox cookies retrieved (n=204).",
        "Uploading payload to C2 server...",
        "Access granted.",
        "System check: Nominal.",
        "Injecting dynamic library...",
        "Evading EDR detection...",
        "Keylogger started on target."
    ];
    
    setInterval(() => {
        const msg = document.createElement('div');
        msg.innerText = `> ${new Date().toLocaleTimeString()} - ${messages[Math.floor(Math.random()*messages.length)]}`;
        logs.appendChild(msg);
        if(logs.childNodes.length > 7) logs.removeChild(logs.firstChild);
    }, 1500);
    
    setInterval(() => {
        document.getElementById('node-count').innerText = (14000 + Math.floor(Math.random()*500)).toLocaleString();
        document.getElementById('traffic').innerText = (1.0 + Math.random()).toFixed(2) + " TB/s";
    }, 3000);
}

// 3D GLOBE
function initGlobe() {
    const container = document.getElementById('globe-container');
    if(!container || !window.THREE) return;
    
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({alpha: true, antialias: true});
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);
    
    // Wireframe Sphere
    const geometry = new THREE.SphereGeometry( 2, 24, 24 );
    const material = new THREE.MeshBasicMaterial( { color: 0x00ffcc, wireframe: true, transparent: true, opacity: 0.15 } );
    const sphere = new THREE.Mesh( geometry, material );
    scene.add( sphere );
    
    // Infected Dots
    const dotsGeo = new THREE.BufferGeometry();
    const dotsCount = 800;
    const posArray = new Float32Array(dotsCount * 3);
    for(let i=0; i<dotsCount*3; i+=3) {
        // Random points on sphere
        const u = Math.random();
        const v = Math.random();
        const theta = 2 * Math.PI * u;
        const phi = Math.acos(2 * v - 1);
        const r = 2.02; // slightly larger than sphere
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
    
    window.addEventListener('resize', () => {
        if(container.clientWidth > 0) {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        }
    });
}

document.addEventListener('DOMContentLoaded', initDashboard);
