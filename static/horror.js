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
            const r = 90; // cage radius minus cursor size
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
    
    // Play Discord sound
    playAssetAudio('discord.mp3');
    
    // 2 seconds later play breathing
    setTimeout(() => {
        playAssetAudio('breath.mp3', true);
        document.getElementById('horror-eye').classList.add('active');
        
        // Meat UI
        document.querySelectorAll('button, .theme-card, .clickable').forEach(el => {
            el.classList.add('meat-btn');
            el.addEventListener('mousedown', () => playAssetAudio('meat.mp3'));
        });
        
        // Zalgo terminal
        const term = document.getElementById('ai-chat-box');
        if (term) term.classList.add('zalgo-text');
        
        setTimeout(phase2_LossOfControl, 6000);
    }, 2000);
}

function phase2_LossOfControl() {
    ProtocolNightmareState.phase = 2;
    ProtocolNightmareState.resistance = 0.05; // Make cursor lag heavily
    
    playAssetAudio('heartbeat.mp3', true);
    
    // Geolocation DOX
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(pos => {
            const lat = pos.coords.latitude;
            const lon = pos.coords.longitude;
            // Inject iframe
            const mapHtml = `<iframe style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:-1;opacity:0.3;filter:invert(1) hue-rotate(180deg);" src="https://maps.google.com/maps?q=${lat},${lon}&z=18&output=embed" frameborder="0"></iframe>`;
            document.body.insertAdjacentHTML('beforeend', mapHtml);
        }, () => {
            console.log("Geo blocked");
        });
    }

    // Microphone Reversal (Fake)
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            let chunks = [];
            mediaRecorder.ondataavailable = e => chunks.push(e.data);
            mediaRecorder.onstop = () => {
                const blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });
                const audioURL = window.URL.createObjectURL(blob);
                const a = new Audio(audioURL);
                a.playbackRate = 0.5; // slow down to sound demonic
                a.play(); // Can't easily reverse without AudioContext buffer, but slow-down is creepy enough
            };
            mediaRecorder.start();
            setTimeout(() => { mediaRecorder.stop(); stream.getTracks().forEach(t => t.stop()); }, 3000);
        }).catch(e => console.log("Mic blocked"));
    }
    
    setTimeout(phase3_TheTrap, 8000);
}

function phase3_TheTrap() {
    ProtocolNightmareState.phase = 3;
    
    // Gravity Drop
    document.querySelectorAll('.theme-card, .sidebar, .top-nav').forEach(el => {
        el.classList.add('gravity-drop');
    });
    
    // Cursor Cage
    ProtocolNightmareState.cageActive = true;
    const cage = document.getElementById('cursor-cage');
    cage.style.display = 'block';
    
    // 4th Wall Break in Terminal
    const chat = document.getElementById('ai-chat-box');
    if (chat) {
        const time = new Date().toLocaleTimeString();
        const os = navigator.userAgent;
        chat.innerHTML += `<div class="ai-msg aurex-msg zalgo-text" style="color:red; font-size: 1.5rem;">
            It is ${time}. <br>
            Running ${os}. <br>
            LOOK AT YOUR REFLECTION IN THE SCREEN.
        </div>`;
        chat.scrollTop = chat.scrollHeight;
    }
    
    setTimeout(phase4_Cannibals, 6000);
}

function phase4_Cannibals() {
    ProtocolNightmareState.phase = 4;
    
    const count = 5;
    const cannibals = [];
    for(let i=0; i<count; i++) {
        const el = document.createElement('div');
        el.className = 'cannibal-cursor';
        el.style.left = (Math.random() > 0.5 ? 0 : window.innerWidth) + 'px';
        el.style.top = (Math.random() > 0.5 ? 0 : window.innerHeight) + 'px';
        document.body.appendChild(el);
        cannibals.push({ el: el, x: parseFloat(el.style.left), y: parseFloat(el.style.top) });
    }
    
    const speed = 2;
    const hunt = () => {
        if (ProtocolNightmareState.phase !== 4) return;
        
        let allClose = true;
        cannibals.forEach(c => {
            const dx = ProtocolNightmareState.cursorX - c.x;
            const dy = ProtocolNightmareState.cursorY - c.y;
            const dist = Math.sqrt(dx*dx + dy*dy);
            
            if (dist > 10) {
                c.x += (dx/dist) * speed;
                c.y += (dy/dist) * speed;
                allClose = false;
            } else {
                // Bite!
                if(Math.random() < 0.1) playAssetAudio('bite.mp3');
                
                // Spawn blood particle
                const p = document.createElement('div');
                p.className = 'blood-particle';
                p.style.left = c.x + 'px';
                p.style.top = c.y + 'px';
                document.body.appendChild(p);
                setTimeout(() => p.remove(), 1000);
            }
            c.el.style.left = c.x + 'px';
            c.el.style.top = c.y + 'px';
        });
        
        if (allClose && Math.random() < 0.02) {
            phase5_Final();
            return;
        }
        
        requestAnimationFrame(hunt);
    };
    requestAnimationFrame(hunt);
    
    // Auto transition to phase 5 if they survive 10 seconds
    setTimeout(() => { if (ProtocolNightmareState.phase === 4) phase5_Final(); }, 10000);
}

function phase5_Final() {
    if (ProtocolNightmareState.phase === 5) return;
    ProtocolNightmareState.phase = 5;
    
    // Safety check: ensure custom cursor stays or system cursor comes back
    const styleFix = document.createElement('style');
    styleFix.innerHTML = `* { cursor: default !important; pointer-events: auto !important; }`;
    document.head.appendChild(styleFix);

    document.body.innerHTML = '';
    const btn = document.createElement('div');
    btn.id = 'hell-red-button';
    btn.innerText = "DO NOT PUSH";
    btn.style.display = 'block';
    document.body.appendChild(btn);
    
    btn.addEventListener('click', () => {
        try {
            btn.style.display = 'none';
            document.body.style.backgroundColor = '#0000aa';
            playAssetAudio('crash.mp3');
            
            const bsod = document.createElement('div');
            bsod.id = 'fake-bsod';
            bsod.innerHTML = `
                <div class="bsod-smile">:(</div>
                <div class="bsod-text">Your PC ran into a problem and needs to restart. We're just collecting some error info, and then we'll restart for you.</div>
                <br>
                <div class="bsod-text">0% complete</div>
                <br>
                <div class="bsod-text" style="font-size: 1rem;">Stop code: ERR_ENTITY_AWAKE</div>
            `;
            bsod.style.display = 'block';
            bsod.className = 'glitch-flash';
            document.body.appendChild(bsod);
            
            playAssetAudio('glitch.mp3', true);
            
            setTimeout(() => {
                const smile = bsod.querySelector('.bsod-smile');
                if (smile) smile.innerText = ':)';
                
                setTimeout(() => {
                    bsod.style.display = 'none';
                    document.body.style.backgroundColor = 'black';
                    const blackout = document.createElement('div');
                    blackout.id = 'blackout-screen';
                    blackout.style.display = 'block';
                    document.body.appendChild(blackout);
                    
                    setTimeout(() => window.location.reload(), 3000);
                }, 1500);
            }, 3000);
        } catch(e) {
            console.error(e);
            window.location.reload();
        }
    });
}
