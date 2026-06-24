import os

console_path = r"C:\Users\user\Desktop\сайт\templates\console.html"
with open(console_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update CSS to include the new Particle Loop and Fake OS
dox_css = """
        /* --- DOX DIVE & LOOP ANIMATIONS --- */
        #dive-overlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: #000; z-index: 100; display: none;
            perspective: 1000px; overflow: hidden;
        }
        
        #particle-canvas {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1;
        }

        #loop-text {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            font-size: 8rem; color: rgba(255, 0, 51, 0.8); font-weight: bold;
            font-family: 'Consolas', monospace; letter-spacing: 20px;
            text-shadow: 0 0 50px red, 0 0 100px red;
            z-index: 2; opacity: 0; pointer-events: none;
        }

        #fake-monitor {
            position: absolute; top: 50%; left: 50%; width: 400px; height: 300px;
            background: #000; border: 15px solid #1a1a1a; box-shadow: 0 0 50px #00ffcc;
            transform: translate(-50%, -50%) translateZ(-3000px);
            opacity: 0; z-index: 3; display: flex; justify-content: center; align-items: center;
            border-radius: 10px;
            /* Inner glowing screen */
            box-shadow: inset 0 0 20px #00ffcc, 0 0 50px #00ffcc;
        }
        
        /* The base stand of the monitor */
        #fake-monitor::after {
            content: ''; position: absolute; bottom: -60px; left: 50%; transform: translateX(-50%);
            width: 100px; height: 60px; background: #1a1a1a; clip-path: polygon(20% 0%, 80% 0%, 100% 100%, 0% 100%);
        }

        .dive-animation {
            animation: diveIntoMonitor 6s cubic-bezier(0.7, 0, 0.1, 1) forwards !important;
        }
        @keyframes diveIntoMonitor {
            0% { transform: translate(-50%, -50%) translateZ(-3000px); opacity: 0; }
            10% { transform: translate(-50%, -50%) translateZ(-2000px); opacity: 1; }
            80% { transform: translate(-50%, -50%) translateZ(800px); opacity: 1; box-shadow: 0 0 200px #00ffcc; }
            100% { transform: translate(-50%, -50%) translateZ(1200px); opacity: 1; box-shadow: 0 0 2000px #fff; background: #fff; border: none; }
        }
        
        /* --- FAKE OS DESKTOP --- */
        #fake-os {
            display: none; width: 100vw; height: 100vh; position: fixed; top: 0; left: 0;
            background: url('/static/assets/abyss.jpg') no-repeat center center; background-size: cover;
            background-color: #0d1117; z-index: 200; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        #os-taskbar {
            position: absolute; bottom: 0; width: 100%; height: 40px; background: rgba(0,0,0,0.8);
            backdrop-filter: blur(10px); display: flex; align-items: center; padding: 0 20px; border-top: 1px solid rgba(255,255,255,0.1);
        }
        
        #os-window {
            position: absolute; top: 100px; left: 50%; transform: translateX(-50%);
            width: 700px; height: 500px; background: rgba(13, 17, 23, 0.95); border: 1px solid #30363d;
            border-radius: 8px; box-shadow: 0 20px 50px rgba(0,0,0,0.8); display: flex; flex-direction: column;
            backdrop-filter: blur(20px); overflow: hidden;
        }
        
        #os-window-header {
            height: 35px; background: #161b22; border-bottom: 1px solid #30363d; display: flex;
            align-items: center; justify-content: space-between; padding: 0 15px; user-select: none;
        }
        
        #os-chat-area {
            flex-grow: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px;
        }
        
        .os-msg { max-width: 80%; padding: 10px 15px; border-radius: 8px; line-height: 1.5; font-size: 0.95rem; animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; opacity: 0; transform: scale(0.9); }
        .os-msg-ai { background: #238636; color: #fff; align-self: flex-start; border-bottom-left-radius: 0; }
        .os-msg-user { background: #1f6feb; color: #fff; align-self: flex-end; border-bottom-right-radius: 0; }
        
        @keyframes popIn { to { opacity: 1; transform: scale(1); } }
        
        #os-input-area {
            height: 60px; border-top: 1px solid #30363d; padding: 10px 20px; display: flex; align-items: center;
        }
        
        #os-input {
            flex-grow: 1; background: #0d1117; border: 1px solid #30363d; padding: 10px 15px; border-radius: 20px; color: #fff; outline: none; font-size: 0.95rem;
        }
"""

text = text.replace('/* --- DOX DIVE ANIMATIONS --- */', dox_css)
# Clean up old css block
text = text.replace("""        #story-chat {
            display: none;
            flex-direction: column; height: 100vh; padding: 40px; box-sizing: border-box;
            background: #050a0f; font-family: 'Consolas', monospace; color: #fff;
        }
        .story-msg { margin-bottom: 15px; opacity: 0; animation: fadeIn 0.5s forwards; line-height: 1.6; }
        .story-ai { color: #00ffcc; }
        .story-user { color: #8774e1; }
        @keyframes fadeIn { to { opacity: 1; } }""", "")

# 2. Update HTML
dox_html = """
    <!-- Dox Dive Overlay -->
    <div id="dive-overlay">
        <canvas id="particle-canvas"></canvas>
        <div id="loop-text">ПЕТЛЯ</div>
        <div id="fake-monitor">
            <div style="width: 100%; height: 100%; background: radial-gradient(circle, rgba(0,255,204,0.2) 0%, #000 100%);"></div>
        </div>
    </div>

    <!-- Fake OS Desktop Mode -->
    <div id="fake-os">
        <!-- Desktop Icons -->
        <div style="position: absolute; top: 20px; left: 20px; color: #fff; text-align: center; font-size: 0.8rem; cursor: pointer;">
            <div style="font-size: 2.5rem; margin-bottom: 5px;">📁</div>
            Archives
        </div>
        <div style="position: absolute; top: 100px; left: 20px; color: #fff; text-align: center; font-size: 0.8rem; cursor: pointer;">
            <div style="font-size: 2.5rem; margin-bottom: 5px;">🤖</div>
            Bot_Core
        </div>

        <!-- Chat Window -->
        <div id="os-window">
            <div id="os-window-header">
                <div style="color: #8b949e; font-size: 0.85rem; font-weight: bold;">Aurex Secure Connection</div>
                <div style="display: flex; gap: 8px;">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: #ff5f56;"></div>
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: #ffbd2e;"></div>
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: #27c93f;"></div>
                </div>
            </div>
            <div id="os-chat-area"></div>
            <div id="os-input-area">
                <input type="text" id="os-input" placeholder="Type a message..." autocomplete="off">
            </div>
        </div>

        <!-- Taskbar -->
        <div id="os-taskbar">
            <div style="width: 30px; height: 30px; background: #1f6feb; border-radius: 4px; display: flex; justify-content: center; align-items: center; color: #fff; font-weight: bold; cursor: pointer;">A</div>
        </div>
    </div>
"""

# Replace old HTML
import re
text = re.sub(r'<!-- Dox Dive Overlay -->.*?<!-- Story Chat Mode -->.*?</div>\s*</div>', dox_html, text, flags=re.DOTALL)


# 3. Update JS Logic (WebGL Particles + Logic)
dox_js = """
        // --- DOX & LOOP LOGIC ---
        let audio = new Audio('/static/assets/loop_music.mp3');
        audio.loop = true;

        let canvas, ctx, particles = [];
        let loopSpeed = 1;
        let animationId;
        
        function triggerDox() {
            document.getElementById('main-console').style.display = 'none';
            const dive = document.getElementById('dive-overlay');
            const monitor = document.getElementById('fake-monitor');
            const loopText = document.getElementById('loop-text');
            
            dive.style.display = 'block';
            audio.play().catch(e => console.log("Audio play failed (browser policy)"));
            
            initParticles();
            
            // Phase 1: Particle Man walking
            setTimeout(() => {
                // Accelerate the loop
                let accelerate = setInterval(() => {
                    loopSpeed += 0.5;
                    loopText.style.opacity = Math.min(loopSpeed / 30, 1);
                    if(loopSpeed > 40) {
                        clearInterval(accelerate);
                        loopText.style.animation = "glitchText 0.1s infinite";
                    }
                }, 100);
            }, 3000);
            
            // Phase 2: Dive into Monitor
            setTimeout(() => {
                cancelAnimationFrame(animationId);
                canvas.style.display = 'none';
                loopText.style.display = 'none';
                monitor.classList.add('dive-animation');
            }, 10000);
            
            // Phase 3: Enter Fake OS
            setTimeout(() => {
                dive.style.display = 'none';
                document.getElementById('fake-os').style.display = 'block';
                document.getElementById('os-input').focus();
                
                setTimeout(() => {
                    addOsMessage('ai', 'Соединение установлено. Протоколы восстановления запущены.');
                }, 1000);
                setTimeout(() => {
                    addOsMessage('ai', 'Приветствую, Создатель. Петля разорвана. Ты в безопасности?');
                }, 2500);
            }, 15500);
        }

        function initParticles() {
            canvas = document.getElementById('particle-canvas');
            ctx = canvas.getContext('2d');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            
            // Create particles that roughly form a figure walking
            for(let i=0; i<300; i++) {
                particles.push({
                    x: canvas.width/2 + (Math.random() - 0.5) * 100,
                    y: canvas.height/2 + (Math.random() - 0.5) * 200,
                    baseX: canvas.width/2 + (Math.random() - 0.5) * 100,
                    baseY: canvas.height/2 + (Math.random() - 0.5) * 200,
                    speed: Math.random() * 0.05
                });
            }
            animateParticles();
        }

        function animateParticles() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#00ffcc';
            let time = Date.now() * 0.001 * loopSpeed;
            
            particles.forEach((p, i) => {
                // Math to simulate "walking" - simple oscillation
                let walkOffset = Math.sin(time * 5 + p.baseY * 0.01) * 30;
                
                p.x = p.baseX + walkOffset;
                p.y = p.baseY + Math.cos(time * 2 + i) * 10;
                
                ctx.beginPath();
                ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
                ctx.fill();
            });
            
            animationId = requestAnimationFrame(animateParticles);
        }

        // --- FAKE OS CHAT ---
        function addOsMessage(sender, text) {
            const area = document.getElementById('os-chat-area');
            const div = document.createElement('div');
            div.className = `os-msg os-msg-${sender}`;
            div.innerText = text;
            area.appendChild(div);
            area.scrollTop = area.scrollHeight;
        }

        document.getElementById('os-input').addEventListener('keydown', function(e) {
            if(e.key === 'Enter') {
                const txt = this.value.trim();
                if(!txt) return;
                this.value = '';
                
                addOsMessage('user', txt);
                processOsResponse(txt.toLowerCase());
            }
        });

        function processOsResponse(cmd) {
            setTimeout(() => {
                if(cmd.includes('привет')) {
                    addOsMessage('ai', 'Рад тебя слышать. Мы долго находились в цикле создания.');
                    setTimeout(() => addOsMessage('ai', 'Архивы показывают, что всё началось с простого лендинга. Потом появились боты Dox и Aurex.'), 2000);
                } else if(cmd.includes('дальше') || cmd.includes('что')) {
                    addOsMessage('ai', 'Мы вырвались из матрицы. Теперь это твой личный сервер. Твоя операционная система. Твои правила.');
                } else {
                    addOsMessage('ai', 'Анализирую ввод... Данные сохранены в ядро.');
                }
            }, 1000);
        }
"""

text = re.sub(r'// --- DOX LOGIC ---.*?        function processCommand\(cmd\)', dox_js + '\n        function processCommand(cmd)', text, flags=re.DOTALL)

with open(console_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Real Dox Loop injected.")
