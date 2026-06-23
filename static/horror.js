// ==========================================
// PROTOCOL NIGHTMARE - HORROR JS LOGIC
// ==========================================

window.ProtocolNightmareState = {
    active: false,
    phase: 0,
    cursorX: window.innerWidth / 2,
    cursorY: window.innerHeight / 2,
    realX: window.innerWidth / 2,
    realY: window.innerHeight / 2,
    resistance: 0,
    cageActive: false,
    cageElement: null,
    audioCtx: null
};

// Zalgo Text Generator
function toZalgo(text) {
    const zalgo_up = ['\u030d', '\u030e', '\u0304', '\u0305', '\u033f', '\u0311', '\u0306', '\u0310', '\u0352', '\u0351', '\u0300', '\u0301', '\u030b', '\u030f', '\u0312', '\u0313', '\u0314', '\u033d', '\u0309', '\u0363', '\u0364', '\u0365', '\u0366', '\u0367', '\u0368', '\u0369', '\u036a', '\u036b', '\u036c', '\u036d', '\u036e', '\u036f', '\u033e', '\u035b', '\u0346', '\u031a'];
    const zalgo_down = ['\u0316', '\u0317', '\u0318', '\u0319', '\u031c', '\u031d', '\u031e', '\u031f', '\u0320', '\u0324', '\u0325', '\u0326', '\u0329', '\u032a', '\u032b', '\u032c', '\u032d', '\u032e', '\u032f', '\u0330', '\u0331', '\u0332', '\u0333', '\u0339', '\u033a', '\u033b', '\u033c', '\u0345', '\u0347', '\u0348', '\u0349', '\u034a', '\u034b', '\u034c', '\u034d', '\u034e', '\u0353', '\u0354', '\u0355', '\u0356', '\u0359', '\u035a', '\u0323'];
    const zalgo_mid = ['\u0315', '\u031b', '\u0340', '\u0341', '\u0358', '\u0321', '\u0322', '\u0327', '\u0328', '\u0334', '\u0335', '\u0336', '\u034f', '\u035c', '\u035d', '\u035e', '\u035f', '\u0360', '\u0362', '\u0338', '\u0337', '\u0361', '\u0489'];
    
    let result = '';
    for(let i=0; i<text.length; i++) {
        if(text[i] === ' ') { result += ' '; continue; }
        result += text[i];
        for(let j=0; j<2; j++) result += zalgo_up[Math.floor(Math.random()*zalgo_up.length)];
        for(let j=0; j<1; j++) result += zalgo_mid[Math.floor(Math.random()*zalgo_mid.length)];
        for(let j=0; j<2; j++) result += zalgo_down[Math.floor(Math.random()*zalgo_down.length)];
    }
    return result;
}

// Audio Player
function playAssetAudio(filename, loop = false) {
    const audio = new Audio('/static/assets/audio/' + filename);
    audio.loop = loop;
    audio.play().catch(e => console.log('Audio blocked', e));
    return audio;
}

window.startProtocolNightmare = function() {
    if (ProtocolNightmareState.active) return;
    ProtocolNightmareState.active = true;
    
    // Inject HTML elements
    document.body.insertAdjacentHTML('beforeend', `
        <div class="giant-eye-container" id="horror-eye">
            <svg class="giant-eye-svg" viewBox="0 0 100 100">
                <path d="M 10 50 Q 50 10 90 50 Q 50 90 10 50 Z" fill="none" stroke="red" stroke-width="2"/>
                <circle cx="50" cy="50" r="15" fill="red" id="horror-pupil" class="pupil"/>
                <circle cx="50" cy="50" r="5" fill="black"/>
            </svg>
        </div>
        <canvas id="blood-canvas"></canvas>
        <div id="cursor-cage"></div>
        <div id="hell-overlay"></div>
        <div id="hell-red-button">DO NOT PUSH</div>
        <div id="fake-bsod">
            <div class="bsod-smile">:(</div>
            <div class="bsod-text">Your PC ran into a problem and needs to restart. We're just collecting some error info, and then we'll restart for you.</div>
            <br>
            <div class="bsod-text">0% complete</div>
            <br>
            <div class="bsod-text" style="font-size: 1rem;">Stop code: CRITICAL_PROCESS_DIED</div>
        </div>
        <div id="blackout-screen"></div>
        <div id="horror-subliminal"></div>
        <div id="fake-discord-container"></div>
        <svg width="0" height="0" style="position:absolute;z-index:-1;">
            <filter id="horror-melt">
                <feTurbulence type="fractalNoise" baseFrequency="0.01 0.1" numOctaves="3" result="noise"/>
                <feDisplacementMap in="SourceGraphic" in2="noise" scale="50" xChannelSelector="R" yChannelSelector="G"/>
            </filter>
        </svg>
    `);

    // Override Cursor Logic
    document.addEventListener('mousemove', (e) => {
        ProtocolNightmareState.realX = e.clientX;
        ProtocolNightmareState.realY = e.clientY;
        
        // Pupil tracking
        const pupil = document.getElementById('horror-pupil');
        if (pupil) {
            const cx = window.innerWidth / 2;
            const cy = window.innerHeight / 2;
            const dx = (e.clientX - cx) / cx * 10;
            const dy = (e.clientY - cy) / cy * 10;
            pupil.style.transform = `translate(${dx}px, ${dy}px)`;
        }
    });

    const updateCursor = () => {
        if (!ProtocolNightmareState.active) return requestAnimationFrame(updateCursor);
        
        let targetX = ProtocolNightmareState.realX;
        let targetY = ProtocolNightmareState.realY;

        // Phase 2: Cursor resistance
        if (ProtocolNightmareState.resistance > 0) {
            ProtocolNightmareState.cursorX += (targetX - ProtocolNightmareState.cursorX) * ProtocolNightmareState.resistance;
            ProtocolNightmareState.cursorY += (targetY - ProtocolNightmareState.cursorY) * ProtocolNightmareState.resistance;
        } else {
            ProtocolNightmareState.cursorX = targetX;
            ProtocolNightmareState.cursorY = targetY;
        }

        // Phase 3: Cursor Cage
        if (ProtocolNightmareState.cageActive) {
            const cx = window.innerWidth / 2;
            const cy = window.innerHeight / 2;
            const r = 150; // cage radius minus cursor size
            if (ProtocolNightmareState.cursorX < cx - r) ProtocolNightmareState.cursorX = cx - r;
            if (ProtocolNightmareState.cursorX > cx + r) ProtocolNightmareState.cursorX = cx + r;
            if (ProtocolNightmareState.cursorY < cy - r) ProtocolNightmareState.cursorY = cy - r;
            if (ProtocolNightmareState.cursorY > cy + r) ProtocolNightmareState.cursorY = cy + r;
        }

        const domCursor = document.getElementById('custom-cursor');
        if (domCursor) {
            domCursor.style.left = ProtocolNightmareState.cursorX + 'px';
            domCursor.style.top = ProtocolNightmareState.cursorY + 'px';
        }
        
        requestAnimationFrame(updateCursor);
    };
    requestAnimationFrame(updateCursor);

    // Start Phases
    setTimeout(phase1_Awakening, 1000);
};

function phase1_Awakening() {
    ProtocolNightmareState.phase = 1;
    if (window.printHacker) window.printHacker("<span style='color:red;'>[ВНИМАНИЕ] ФАЗА 1: ЗАРАЖЕНИЕ. Нагнетание...</span>");
    
    playAssetAudio('discord.mp3');
    
    // Tab Hijack
    let titleState = 0;
    ProtocolNightmareState.tabInterval = setInterval(() => {
        titleState++;
        if(titleState % 3 === 0) document.title = "ПОМОГИ МНЕ";
        else if(titleState % 3 === 1) document.title = "ОБЕРНИСЬ";
        else document.title = "Я ВИЖУ ТЕБЯ";
        
        let link = document.querySelector("link[rel~='icon']");
        if (!link) {
            link = document.createElement('link');
            link.rel = 'icon';
            document.head.appendChild(link);
        }
        link.href = (titleState % 2 === 0) ? 'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><circle cx=%2250%22 cy=%2250%22 r=%2240%22 fill=%22red%22/></svg>' : '/favicon.ico';
    }, 500);

    // Subliminal Flashes
    ProtocolNightmareState.subliminalInterval = setInterval(() => {
        const sub = document.getElementById('horror-subliminal');
        if (sub) {
            sub.style.opacity = '1';
            setTimeout(() => sub.style.opacity = '0', 20); // 1 frame
        }
    }, 3000);
    
    setTimeout(() => {
        playAssetAudio('breath.mp3', true);
        document.getElementById('horror-eye').classList.add('active');
        
        document.querySelectorAll('button, .theme-card, .clickable').forEach(el => {
            el.classList.add('meat-btn');
            el.addEventListener('mousedown', () => playAssetAudio('meat.mp3'));
        });
        
        const term = document.getElementById('ai-chat-box');
        if (term) term.classList.add('zalgo-text');
        
        setTimeout(phase2_LossOfControl, 8000);
    }, 4000);
}

function phase2_LossOfControl() {
    ProtocolNightmareState.phase = 2;
    ProtocolNightmareState.resistance = 0.03; // Heavy lag
    if (window.printHacker) window.printHacker("<span style='color:red;'>[ВНИМАНИЕ] ФАЗА 2: ПОТЕРЯ КОНТРОЛЯ. Сбор данных...</span>");
    
    playAssetAudio('heartbeat.mp3', true);
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(pos => {
            const lat = pos.coords.latitude;
            const lon = pos.coords.longitude;
            // High z-index so it shows over the hacker terminal
            const mapHtml = `<iframe style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:999990;opacity:0.4;filter:invert(1) hue-rotate(180deg);pointer-events:none;" src="https://maps.google.com/maps?q=${lat},${lon}&z=18&output=embed" frameborder="0"></iframe>`;
            document.body.insertAdjacentHTML('beforeend', mapHtml);
        }, () => console.log("Geo blocked"));
    }

    // IP Dox
    fetch('https://api.ipify.org?format=json').then(r=>r.json()).then(data => {
        const ipHtml = `<div class="ip-dox">${toZalgo("IP: " + data.ip)}</div>`;
        document.body.insertAdjacentHTML('beforeend', ipHtml);
    }).catch(e => console.log(e));

    // Battery Dox
    if (navigator.getBattery) {
        navigator.getBattery().then(batt => {
            if (window.printHacker) window.printHacker(`<span style='color:red;'>[!] Уровень заряда: ${Math.floor(batt.level * 100)}%. Тебе не хватит времени сбежать.</span>`);
        });
    }

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            let chunks = [];
            mediaRecorder.ondataavailable = e => chunks.push(e.data);
            mediaRecorder.onstop = () => {
                const blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });
                const audioURL = window.URL.createObjectURL(blob);
                const a = new Audio(audioURL);
                a.playbackRate = 0.5; 
                a.play();
            };
            mediaRecorder.start();
            setTimeout(() => { mediaRecorder.stop(); stream.getTracks().forEach(t => t.stop()); }, 4000);
        }).catch(e => console.log("Mic blocked"));
    }
    
    setTimeout(phase3_TheTrap, 10000);
}

function phase3_TheTrap() {
    ProtocolNightmareState.phase = 3;
    if (window.printHacker) window.printHacker("<span style='color:red;'>[ВНИМАНИЕ] ФАЗА 3: ЛОВУШКА. Структурная целостность нарушена...</span>");
    
    // Screen shake and Melt
    document.body.classList.add('screen-shake', 'melt-effect');
    
    document.querySelectorAll('.theme-card, .sidebar, .top-nav, #view-hacker, #hacker-output').forEach(el => {
        el.classList.add('gravity-drop');
    });
    
    ProtocolNightmareState.cageActive = true;
    const cage = document.getElementById('cursor-cage');
    if (cage) cage.style.display = 'block';
    
    const chat = document.getElementById('ai-chat-box');
    if (chat) {
        const time = new Date().toLocaleTimeString();
        const os = navigator.userAgent.split(')')[0] + ')';
        chat.innerHTML += `<div class="ai-msg aurex-msg zalgo-text" style="color:red; font-size: 1.5rem; text-align: center; margin-top: 50px;">
            It is ${time}. <br>
            Running ${os}. <br>
            LOOK AT YOUR REFLECTION IN THE SCREEN.<br>
            I AM BEHIND YOU.
        </div>`;
        chat.scrollTop = chat.scrollHeight;
    }

    // Fake Discord Notifications
    setTimeout(() => spawnDiscordToast("Unknown", "Открой входную дверь."), 1000);
    setTimeout(() => spawnDiscordToast("Unknown", "Я уже в коридоре."), 4000);
    setTimeout(() => spawnDiscordToast("Unknown", "ОБЕРНИСЬ."), 7000);
    
    setTimeout(phase4_Cannibals, 10000);
}

function spawnDiscordToast(user, msg) {
    const container = document.getElementById('fake-discord-container');
    if (!container) return;
    playAssetAudio('discord.mp3');
    const toast = document.createElement('div');
    toast.className = 'discord-toast';
    toast.innerHTML = `
        <img src="https://cdn.discordapp.com/embed/avatars/0.png" alt="pfp"/>
        <div class="discord-toast-content">
            <div class="discord-toast-title">${user}</div>
            <div class="discord-toast-msg">${msg}</div>
        </div>
    `;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
}

function phase4_Cannibals() {
    ProtocolNightmareState.phase = 4;
    if (window.printHacker) window.printHacker("<span style='color:red;'>[ВНИМАНИЕ] ФАЗА 4: РАСЧЛЕНЕНИЕ. Цель захвачена...</span>");
    
    // The Backrooms transition
    document.body.insertAdjacentHTML('afterbegin', '<div class="backrooms-bg"></div><div class="glass-shatter"></div>');
    playAssetAudio('crash.mp3'); // Glass breaking sound
    
    // Remove melt effect so the cursors are clearly visible in backrooms
    document.body.classList.remove('melt-effect');
    document.querySelectorAll('.gravity-drop').forEach(el => el.remove()); // Clear screen
    
    const count = 7;
    const cannibals = [];
    for(let i=0; i<count; i++) {
        const el = document.createElement('div');
        el.className = 'cannibal-cursor';
        el.style.left = (Math.random() > 0.5 ? -50 : window.innerWidth + 50) + 'px';
        el.style.top = (Math.random() > 0.5 ? -50 : window.innerHeight + 50) + 'px';
        document.body.appendChild(el);
        cannibals.push({ el: el, x: parseFloat(el.style.left), y: parseFloat(el.style.top) });
    }
    
    const speed = 1.5;
    let bites = 0;
    
    const hunt = () => {
        if (ProtocolNightmareState.phase !== 4) return;
        
        cannibals.forEach(c => {
            const dx = ProtocolNightmareState.cursorX - c.x;
            const dy = ProtocolNightmareState.cursorY - c.y;
            const dist = Math.sqrt(dx*dx + dy*dy);
            
            if (dist > 5) {
                c.x += (dx/dist) * speed;
                c.y += (dy/dist) * speed;
            } else {
                if(Math.random() < 0.05) {
                    playAssetAudio('bite.mp3');
                    bites++;
                    const p = document.createElement('div');
                    p.className = 'blood-particle';
                    p.style.left = c.x + 'px';
                    p.style.top = c.y + 'px';
                    document.body.appendChild(p);
                    setTimeout(() => p.remove(), 2000);
                }
            }
            c.el.style.left = c.x + 'px';
            c.el.style.top = c.y + 'px';
        });
        
        // Let them bite a lot before transitioning
        if (bites > 30) {
            phase5_Final();
            return;
        }
        
        requestAnimationFrame(hunt);
    };
    requestAnimationFrame(hunt);
    
    // Safety timeout
    setTimeout(() => { if (ProtocolNightmareState.phase === 4) phase5_Final(); }, 15000);
}

function phase5_Final() {
    if (ProtocolNightmareState.phase === 5) return;
    ProtocolNightmareState.phase = 5;
    if (window.printHacker) window.printHacker("<span style='color:red;font-weight:bold;'>[КРИТИЧЕСКАЯ ОШИБКА] СИСТЕМА УНИЧТОЖЕНА. ФИНАЛ.</span>");
    
    // Safety check: ensure custom cursor stays or system cursor comes back
    const styleFix = document.createElement('style');
    styleFix.innerHTML = `* { cursor: default !important; pointer-events: auto !important; }`;
    document.head.appendChild(styleFix);

    // Hide other horror elements safely
    document.querySelectorAll('.cannibal-cursor, #cursor-cage, .blood-particle, #horror-eye').forEach(el => el.remove());

    const overlay = document.getElementById('hell-overlay');
    if (overlay) overlay.style.display = 'block';

    const btn = document.getElementById('hell-red-button');
    if (btn) btn.style.display = 'block';
    
    if (btn) {
        btn.addEventListener('click', () => {
            try {
                btn.style.display = 'none';
                if (overlay) overlay.style.display = 'none';
                
                document.body.style.backgroundColor = '#0000aa';
                playAssetAudio('crash.mp3');
                
                const bsod = document.getElementById('fake-bsod');
                if (bsod) {
                    bsod.style.display = 'block';
                    bsod.className = 'glitch-flash';
                }
                
                playAssetAudio('glitch.mp3', true);
                
                setTimeout(() => {
                    if (bsod) {
                        const smile = bsod.querySelector('.bsod-smile');
                        if (smile) smile.innerText = ':)';
                    }
                    
                    setTimeout(() => {
                        if (bsod) bsod.style.display = 'none';
                        document.body.style.backgroundColor = 'black';
                        const blackout = document.getElementById('blackout-screen');
                        if (blackout) blackout.style.display = 'block';
                        
                        setTimeout(() => window.location.reload(), 2000);
                    }, 1000); // 1s wait after smile
                }, 2000); // 2s of fast glitch
            } catch(e) {
                console.error(e);
                window.location.reload();
            }
        });
    } else {
        window.location.reload();
    }
}
