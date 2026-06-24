import re

index_path = r"C:\Users\user\Desktop\сайт\templates\index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    text = f.read()

new_vault_content = """<!-- Настоящий скрытый контент -->
<div id="secret-vault" style="display: none; min-height: 100vh; background: #000; color: #fff; font-family: 'Space Grotesk', sans-serif; position: relative; overflow: hidden; margin: 0; padding: 0;">
    
    <style>
        body, html { margin: 0; padding: 0; overflow: hidden; background: #000; }
        
        .sanity-meter-container { width: 300px; font-family: monospace; }
        .sanity-label { color: #ff0033; font-weight: bold; margin-bottom: 5px; text-shadow: 0 0 5px #ff0033; }
        .sanity-bar-bg { width: 100%; height: 15px; background: rgba(255,0,0,0.1); border: 1px solid #ff0033; position: relative; }
        .sanity-bar-fill { height: 100%; background: #ff0033; box-shadow: 0 0 10px #ff0033; }
        
        .loop-timer { text-align: right; font-family: monospace; color: #aaa; }
        .timer-label { font-size: 0.8rem; margin-bottom: 5px; letter-spacing: 2px; }
        .timer-value { font-size: 1.5rem; color: #ff0033; text-shadow: 0 0 8px #ff0033; }
        
        .glitch-anim { animation: glitchBar 0.2s infinite; }
        @keyframes glitchBar {
            0% { transform: translateX(0) scaleY(1); opacity: 1; }
            50% { transform: translateX(-2px) scaleY(0.8); opacity: 0.8; }
            100% { transform: translateX(2px) scaleY(1.1); opacity: 1; }
        }
        
        .glitch-text-fx { animation: glitchText 0.1s infinite; }
        @keyframes glitchText {
            0% { transform: translate(0); }
            20% { transform: translate(-2px, 1px); }
            40% { transform: translate(2px, -1px); color: #fff; }
            60% { transform: translate(-1px, 2px); }
            80% { transform: translate(1px, -2px); color: #ff0033; }
            100% { transform: translate(0); }
        }

        .shard {
            position: absolute;
            background: rgba(20, 0, 0, 0.7);
            border: 1px solid rgba(255, 0, 51, 0.4);
            box-shadow: 0 0 15px rgba(255, 0, 51, 0.2);
            color: #ff0033;
            padding: 20px;
            cursor: pointer;
            transition: all 0.5s ease;
            backdrop-filter: blur(5px);
            clip-path: polygon(10% 0, 100% 0, 90% 100%, 0% 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        .shard:hover {
            transform: translate3d(0,0,100px) rotateX(0) rotateY(0) scale(1.1) !important;
            box-shadow: 0 0 30px rgba(255, 0, 51, 0.8);
            border-color: #ff0033;
            z-index: 100;
            clip-path: polygon(0 0, 100% 0, 100% 100%, 0% 100%);
        }
        .shard h3 { margin: 0 0 10px 0; font-family: monospace; font-size: 1.5rem; }
        .shard p { font-size: 0.9rem; color: #ccc; margin: 0; }
        
        #paranoia-eye {
            position: fixed;
            top: 50%; left: 50%;
            width: 50px; height: 50px;
            border-radius: 50%;
            background: radial-gradient(circle, #aa0000 10%, #220000 70%, #000 100%);
            box-shadow: 0 0 30px #ff0033;
            pointer-events: none;
            z-index: 5;
            transition: transform 0.05s ease-out;
            opacity: 0.3;
            mix-blend-mode: screen;
        }
        #pupil {
            position: absolute;
            top: 20px; left: 20px;
            width: 10px; height: 10px;
            background: #000;
            border-radius: 50%;
            box-shadow: 0 0 5px #000;
        }
    </style>

    <!-- Dynamic Canvas Background -->
    <canvas id="vault-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0;"></canvas>

    <!-- UI Overlay -->
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; pointer-events: none; display: flex; flex-direction: column;">
        
        <!-- Top Bar -->
        <div style="display: flex; justify-content: space-between; padding: 30px; pointer-events: auto;">
            <div class="sanity-meter-container">
                <div class="sanity-label">[ СВЯЗЬ_С_РЕАЛЬНОСТЬЮ: КРИТИЧЕСКАЯ ]</div>
                <div class="sanity-bar-bg">
                    <div class="sanity-bar-fill glitch-anim" id="sanity-fill" style="width: 3%;"></div>
                </div>
            </div>
            <div class="loop-timer">
                <div class="timer-label">ВРЕМЯ_В_ПЕТЛЕ (С 2021)</div>
                <div class="timer-value" id="loop-time">00:00:00:00</div>
            </div>
        </div>

        <!-- Main Center Content (Archive Shards) -->
        <div style="flex-grow: 1; display: flex; justify-content: center; align-items: center; pointer-events: auto; perspective: 1200px;">
            <div id="shard-container" style="position: relative; width: 1000px; height: 600px; transform-style: preserve-3d;">
                <!-- Shards will be injected here -->
            </div>
        </div>

        <!-- Bottom Bar / Settings -->
        <div style="padding: 30px; display: flex; justify-content: flex-end; pointer-events: auto;">
            <button id="vault-settings-btn" style="background: rgba(20,0,0,0.8); border: 1px solid #ff0033; color: #ff0033; padding: 10px 20px; cursor: pointer; text-shadow: 0 0 5px #ff0033; box-shadow: 0 0 10px rgba(255,0,51,0.2); font-family: monospace;">[ НАСТРОЙКИ_СИСТЕМЫ ]</button>
        </div>
        
        <!-- Settings Panel -->
        <div id="vault-settings-panel" style="display: none; position: absolute; bottom: 80px; right: 30px; background: rgba(10,0,0,0.95); border: 1px solid #ff0033; padding: 20px; pointer-events: auto; font-family: monospace; width: 250px; box-shadow: 0 0 20px rgba(255,0,51,0.3);">
            <h3 style="color: #ff0033; margin-top: 0; font-size: 1rem; border-bottom: 1px solid rgba(255,0,51,0.3); padding-bottom: 5px;">ВИЗУАЛИЗАЦИЯ_ФОНА</h3>
            <select id="bg-selector" style="background: #000; color: #ff0033; border: 1px solid #ff0033; padding: 8px; width: 100%; margin-bottom: 20px; outline: none; cursor: pointer;">
                <option value="sparks">А: Пепел и Искры</option>
                <option value="abyss">Б: Цифровая Бездна</option>
                <option value="fluid">В: Живая Материя</option>
            </select>
            
            <h3 style="color: #ff0033; margin-top: 0; font-size: 1rem; border-bottom: 1px solid rgba(255,0,51,0.3); padding-bottom: 5px;">АУДИО_ПОТОК</h3>
            <label style="display: flex; align-items: center; color: #ff0033; cursor: pointer; margin-bottom: 20px;">
                <input type="checkbox" id="audio-toggle" style="margin-right: 10px; accent-color: #ff0033;">
                ДАРК-ЭМБИЕНТ
            </label>

            <h3 style="color: #ff0033; margin-top: 0; font-size: 1rem; border-bottom: 1px solid rgba(255,0,51,0.3); padding-bottom: 5px;">ПАРАНОЙЯ</h3>
            <label style="display: flex; align-items: center; color: #ff0033; cursor: pointer;">
                <input type="checkbox" id="eye-toggle" checked style="margin-right: 10px; accent-color: #ff0033;">
                ГЛАЗ-НАБЛЮДАТЕЛЬ
            </label>
        </div>
    </div>
    
    <!-- Paranoia Eye -->
    <div id="paranoia-eye">
        <div id="pupil"></div>
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
            updateEye(mx, my);
        });

        // Init UI
        initTimer();
        initShards();
        
        // Settings bindings
        document.getElementById('vault-settings-btn').onclick = () => {
            const panel = document.getElementById('vault-settings-panel');
            panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
        };
        
        document.getElementById('bg-selector').onchange = (e) => {
            bgTheme = e.target.value;
            particles = []; // reset
        };

        document.getElementById('audio-toggle').onchange = (e) => {
            if(e.target.checked) startAudio();
            else stopAudio();
        };

        document.getElementById('eye-toggle').onchange = (e) => {
            document.getElementById('paranoia-eye').style.display = e.target.checked ? 'block' : 'none';
        };

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
        
        // Random sanity glitch
        if(Math.random() < 0.05) {
            document.getElementById('sanity-fill').style.width = (Math.random() * 10) + '%';
        } else {
            document.getElementById('sanity-fill').style.width = '3%';
        }

        requestAnimationFrame(renderBackground);
    }

    // Theme A: Sparks
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
            
            // Mouse interaction
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

    // Theme B: Digital Abyss
    function drawAbyss() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.strokeStyle = `rgba(255, 0, 51, ${(Math.sin(frameCount * 0.05) + 1) / 4})`;
        ctx.lineWidth = 1;
        
        let cx = canvas.width / 2;
        let cy = canvas.height / 2;
        
        for(let i=1; i<10; i++) {
            let scale = (frameCount % 100) / 100 + i;
            let size = scale * 50;
            ctx.strokeRect(cx - size, cy - size, size*2, size*2);
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.lineTo(cx - size, cy - size);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.lineTo(cx + size, cy + size);
            ctx.stroke();
        }
    }

    // Theme C: Fluid (Simple trailing)
    function drawFluid() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        particles.push({x: mx, y: my, age: 0});
        
        ctx.beginPath();
        particles.forEach((p, i) => {
            p.age++;
            p.y -= 2;
            p.x += (Math.random()-0.5)*5;
            ctx.strokeStyle = `rgba(255, 0, 51, ${1 - p.age/50})`;
            ctx.lineWidth = 20 * (1 - p.age/50);
            ctx.lineTo(p.x, p.y);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            if(p.age > 50) particles.splice(i, 1);
        });
    }

    // --- PARANOIA EYE ---
    function updateEye(x, y) {
        const eye = document.getElementById('paranoia-eye');
        const pupil = document.getElementById('pupil');
        if(!eye || eye.style.display === 'none') return;
        
        let rect = eye.getBoundingClientRect();
        let ex = rect.left + 25;
        let ey = rect.top + 25;
        
        let dx = x - ex;
        let dy = y - ey;
        
        eye.style.transform = `translate(${dx * 0.05}px, ${dy * 0.05}px)`;
        
        let angle = Math.atan2(dy, dx);
        let dist = Math.min(10, Math.sqrt(dx*dx + dy*dy) * 0.1);
        pupil.style.transform = `translate(${Math.cos(angle)*dist}px, ${Math.sin(angle)*dist}px)`;
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

    // --- ARCHIVE SHARDS ---
    function initShards() {
        const container = document.getElementById('shard-container');
        const projects = [
            { title: "SYSTEM_LOGS", desc: "Дневник мыслей." },
            { title: "PROJECT_AUREX", desc: "Заброшенный бот." },
            { title: "DOX_DB", desc: "База данных." },
            { title: "THE_VOID", desc: "Пустота." },
            { title: "LOOP_DATA", desc: "5 лет дежавю." }
        ];

        projects.forEach((p, i) => {
            let el = document.createElement('div');
            el.className = 'shard';
            el.innerHTML = `<h3>${p.title}</h3><p>${p.desc}</p>`;
            
            let rx = (Math.random() - 0.5) * 60;
            let ry = (Math.random() - 0.5) * 60;
            let tz = (Math.random() - 0.5) * 400;
            let x = Math.random() * 800;
            let y = Math.random() * 400;
            
            el.style.left = x + 'px';
            el.style.top = y + 'px';
            el.style.transform = `translate3d(0, 0, ${tz}px) rotateX(${rx}deg) rotateY(${ry}deg)`;
            
            container.appendChild(el);
        });
    }

    // --- AUDIO GENERATOR ---
    let audioCtx, osc, lfo, gain;
    function startAudio() {
        if(!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if(audioCtx.state === 'suspended') audioCtx.resume();
        
        osc = audioCtx.createOscillator();
        lfo = audioCtx.createOscillator();
        gain = audioCtx.createGain();
        
        osc.type = 'sine';
        osc.frequency.value = 60;
        
        lfo.type = 'sine';
        lfo.frequency.value = 0.2;
        
        let lfoGain = audioCtx.createGain();
        lfoGain.gain.value = 10;
        lfo.connect(lfoGain);
        lfoGain.connect(osc.frequency);
        
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        
        gain.gain.value = 0.1;
        
        osc.start();
        lfo.start();
    }
    
    function stopAudio() {
        if(osc) osc.stop();
        if(lfo) lfo.stop();
    }

</script>
</body>"""

new_text = re.sub(r'<!-- Настоящий скрытый контент \(пока что заглушка\) -->.*</body>', new_vault_content, text, flags=re.DOTALL)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Vault built in index.html")
