import re

index_path = r"C:\Users\user\Desktop\сайт\templates\index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    text = f.read()

new_vault_content = """<!-- Настоящий скрытый контент -->
<div id="secret-vault" style="display: none; min-height: 100vh; background: #000; color: #fff; font-family: 'Space Grotesk', sans-serif; position: relative; overflow: hidden; margin: 0; padding: 0;">
    
    <style>
        body, html { margin: 0; padding: 0; overflow: hidden; background: #000; }
        
        .loop-timer { position: absolute; top: 30px; right: 30px; text-align: right; font-family: monospace; color: #aaa; z-index: 20; pointer-events: auto; }
        .timer-label { font-size: 0.8rem; margin-bottom: 5px; letter-spacing: 2px; }
        .timer-value { font-size: 1.5rem; color: #ff0033; text-shadow: 0 0 8px #ff0033; }
        
        .glitch-text-fx { animation: glitchText 0.1s infinite; }
        @keyframes glitchText {
            0% { transform: translate(0); }
            20% { transform: translate(-2px, 1px); }
            40% { transform: translate(2px, -1px); color: #fff; }
            60% { transform: translate(-1px, 2px); }
            80% { transform: translate(1px, -2px); color: #ff0033; }
            100% { transform: translate(0); }
        }

        /* --- TELEGRAM SIDEBAR STYLES --- */
        .sidebar {
            position: fixed;
            top: 0;
            left: -300px;
            width: 300px;
            height: 100vh;
            background: #17212b; /* Telegram Dark Theme */
            color: #fff;
            z-index: 9999;
            transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 5px 0 15px rgba(0,0,0,0.5);
            display: flex;
            flex-direction: column;
            pointer-events: auto;
            font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
        }
        .sidebar-trigger {
            position: fixed;
            top: 0;
            left: 0;
            width: 20px;
            height: 100vh;
            z-index: 9998;
            pointer-events: auto;
        }
        .sidebar-header {
            padding: 20px;
            background: #242f3d;
            display: flex;
            flex-direction: column;
            gap: 15px;
            border-bottom: 1px solid #10161c;
        }
        .sidebar-avatar {
            width: 55px; height: 55px;
            border-radius: 50%;
            background: #000;
            object-fit: cover;
            border: 2px solid transparent;
        }
        .sidebar-user-info {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        .sidebar-name {
            font-weight: 600; 
            font-size: 1.1rem;
            color: #fff;
        }
        .sidebar-status {
            color: #7f91a4; 
            font-size: 0.85rem; 
            cursor: pointer;
        }
        .sidebar-menu {
            flex-grow: 1;
            overflow-y: auto;
            padding: 10px 0;
        }
        .sidebar-menu::-webkit-scrollbar {
            width: 6px;
        }
        .sidebar-menu::-webkit-scrollbar-thumb {
            background: #2a394a;
            border-radius: 3px;
        }
        .sidebar-item {
            padding: 12px 20px;
            display: flex;
            align-items: center;
            gap: 20px;
            cursor: pointer;
            transition: background 0.15s;
            color: #fff;
            font-size: 0.95rem;
            font-weight: 500;
        }
        .sidebar-item:hover {
            background: #202b36;
        }
        .sidebar-item i {
            width: 24px;
            text-align: center;
            color: #7f91a4;
            font-size: 1.2rem;
        }
        .sidebar-divider {
            height: 1px;
            background: #10161c;
            margin: 5px 0;
        }
    </style>

    <!-- Dynamic Canvas Background -->
    <canvas id="vault-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0;"></canvas>

    <!-- UI Overlay -->
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; pointer-events: none; display: flex; flex-direction: column;">
        
        <div class="loop-timer">
            <div class="timer-label">ВРЕМЯ_В_ПЕТЛЕ (С 2021)</div>
            <div class="timer-value" id="loop-time">00:00:00:00</div>
        </div>

        <!-- Main Center Content Placeholder -->
        <div style="flex-grow: 1; display: flex; justify-content: center; align-items: center; pointer-events: auto;">
            <div style="color: rgba(255,255,255,0.2); font-size: 1.2rem; letter-spacing: 2px;">ПОТЯНИ МЫШКУ К ЛЕВОМУ КРАЮ</div>
        </div>
    </div>

    <!-- TELEGRAM-LIKE SIDEBAR -->
    <div class="sidebar-trigger" id="sidebar-trigger"></div>
    <div class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <img src="/static/assets/default-avatar.png" class="sidebar-avatar" id="vault-avatar">
            <div class="sidebar-user-info">
                <div class="sidebar-name">ДомадOX</div>
                <div class="sidebar-status">Установить эмодзи-статус</div>
            </div>
        </div>
        
        <div class="sidebar-menu">
            <!-- Accounts (Optional, like in screenshot) -->
            <div class="sidebar-item"><img src="/static/assets/default-avatar.png" style="width: 24px; height: 24px; border-radius: 50%;"> ДомадOX</div>
            <div class="sidebar-divider"></div>
            
            <div class="sidebar-item" id="menu-profile"><i class="fa-regular fa-user"></i> Мой профиль</div>
            <div class="sidebar-item" id="menu-wallet"><i class="fa-solid fa-wallet"></i> Кошелёк</div>
            <div class="sidebar-item" id="menu-projects"><i class="fa-solid fa-folder-open"></i> Архив проектов</div>
            <div class="sidebar-item" id="menu-diary"><i class="fa-solid fa-book"></i> Дневник</div>
            <div class="sidebar-divider"></div>
            <div class="sidebar-item" id="menu-settings"><i class="fa-solid fa-gear"></i> Настройки</div>
            
            <div class="sidebar-item" style="justify-content: space-between;">
                <div style="display: flex; gap: 20px; align-items: center;">
                    <i class="fa-solid fa-moon"></i> Ночной режим
                </div>
                <div style="width: 30px; height: 16px; background: #2a394a; border-radius: 10px; position: relative;">
                    <div style="position: absolute; top: 2px; left: 16px; width: 12px; height: 12px; background: #8774e1; border-radius: 50%;"></div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    // --- LOGIN LOGIC ---
    let keySequence = "";
    const secretCode = "open";
    let vaultUnlocked = false;

    document.addEventListener('keydown', function(e) {
        if(vaultUnlocked) return;
        keySequence += e.key.toLowerCase();
        if (keySequence.length > secretCode.length) {
            keySequence = keySequence.substring(1, keySequence.length);
        }
        if (keySequence === secretCode) {
            unlockVault();
        }
    });

    function unlockVault() {
        vaultUnlocked = true;
        const fakeFront = document.getElementById('fake-front');
        const vault = document.getElementById('secret-vault');
        
        fakeFront.style.filter = "blur(10px) hue-rotate(90deg)";
        fakeFront.style.transform = "scale(1.1)";
        fakeFront.style.opacity = "0";
        fakeFront.style.transition = "all 0.8s ease-in-out";
        
        setTimeout(() => {
            fakeFront.style.display = 'none';
            vault.style.display = 'flex';
            initVault();
        }, 800);
    }

    // --- SIDEBAR LOGIC ---
    const sidebar = document.getElementById('sidebar');
    const trigger = document.getElementById('sidebar-trigger');
    
    trigger.addEventListener('mouseenter', () => {
        sidebar.style.left = '0';
    });
    
    sidebar.addEventListener('mouseleave', () => {
        sidebar.style.left = '-300px';
    });

    // --- VAULT LOGIC ---
    let canvas, ctx;
    let bgTheme = 'sparks';
    let particles = [];
    let mx = 0, my = 0;
    
    function initVault() {
        canvas = document.getElementById('vault-canvas');
        ctx = canvas.getContext('2d');
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
        
        document.addEventListener('mousemove', (e) => {
            mx = e.clientX;
            my = e.clientY;
        });

        // Init UI
        initTimer();
        
        // Start render loop
        requestAnimationFrame(renderBackground);
    }

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    // --- DYNAMIC BACKGROUNDS ---
    let frameCount = 0;
    
    function renderBackground() {
        frameCount++;
        if(bgTheme === 'sparks') drawSparks();
        else if(bgTheme === 'abyss') drawAbyss();
        else if(bgTheme === 'fluid') drawFluid();
        
        requestAnimationFrame(renderBackground);
    }

    function drawSparks() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        if(particles.length < 150) {
            particles.push({
                x: Math.random() * canvas.width,
                y: canvas.height + 10,
                vx: (Math.random() - 0.5) * 1,
                vy: -(Math.random() * 2 + 1),
                size: Math.random() * 3 + 1,
                color: `rgba(255, ${Math.random()*100}, 0, ${Math.random()})`
            });
        }
        
        particles.forEach((p, i) => {
            p.x += p.vx;
            p.y += p.vy;
            let dx = mx - p.x;
            let dy = my - p.y;
            let dist = Math.sqrt(dx*dx + dy*dy);
            if(dist < 100) {
                p.x -= dx * 0.05;
                p.y -= dy * 0.05;
            }
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
            ctx.fill();
            if(p.y < -10) particles.splice(i, 1);
        });
    }

    // --- LOOP TIMER ---
    function initTimer() {
        const startDate = new Date('2021-01-01T00:00:00');
        const timerEl = document.getElementById('loop-time');
        
        setInterval(() => {
            let now = new Date();
            let diff = now - startDate;
            let years = Math.floor(diff / (1000 * 60 * 60 * 24 * 365));
            diff -= years * (1000 * 60 * 60 * 24 * 365);
            let days = Math.floor(diff / (1000 * 60 * 60 * 24));
            diff -= days * (1000 * 60 * 60 * 24);
            let hours = Math.floor(diff / (1000 * 60 * 60));
            diff -= hours * (1000 * 60 * 60);
            let mins = Math.floor(diff / (1000 * 60));
            diff -= mins * (1000 * 60);
            let secs = Math.floor(diff / 1000);
            let ms = Math.floor((diff % 1000) / 10);
            
            let text = `${years}Г : ${days}Д : ${hours}Ч : ${mins}М : ${secs}С : ${ms}МС`;
            
            if(Math.random() < 0.02) {
                text = text.replace(/[0-9]/g, () => Math.floor(Math.random()*10));
                timerEl.classList.add('glitch-text-fx');
            } else {
                timerEl.classList.remove('glitch-text-fx');
            }
            timerEl.innerText = text;
        }, 50);
    }
</script>
</body>"""

new_text = re.sub(r'<!-- Настоящий скрытый контент -->.*</body>', new_vault_content, text, flags=re.DOTALL)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Sidebar added")
