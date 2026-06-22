import os

css_append = """
/* --- STAGE 2: CREEPY FACE & GRAVITY FALL --- */
.creepy-face {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 15vw;
    color: #ff0000;
    font-weight: bold;
    font-family: monospace;
    opacity: 0;
    z-index: 1000;
    pointer-events: none;
    text-shadow: 0 0 30px #ff0000;
    transition: opacity 4s ease-in;
    white-space: nowrap;
}

.gravity-fall {
    animation: gravity-drop 4s cubic-bezier(0.55, 0.085, 0.68, 0.53) forwards !important;
}

@keyframes gravity-drop {
    0% { transform: translateY(0) rotate(0); }
    100% { transform: translateY(150vh) rotate(45deg); opacity: 0; }
}

.anticheat-overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 5, 0, 0.95);
    color: #0f0;
    font-family: 'Courier New', Courier, monospace;
    font-size: 2vw;
    z-index: 9999999;
    padding: 50px;
    opacity: 0;
    transition: opacity 1s;
    pointer-events: none;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-shadow: 0 0 5px #0f0;
}

.anticheat-line {
    opacity: 0;
    margin: 10px 0;
    transform: translateY(20px);
    transition: all 0.5s;
}

.anticheat-line.visible {
    opacity: 1;
    transform: translateY(0);
}
"""

with open('static/style.css', 'a', encoding='utf-8') as f:
    f.write(css_append)

js_new = """
function triggerApocalypse() {
    if(document.body.classList.contains('apocalypse-mode')) return;
    
    document.body.classList.add('apocalypse-mode');
    
    // Play a low ominous drone or glitch sound
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(50, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(10, audioCtx.currentTime + 2);
        gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 2);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 2);
    } catch(e) {}
    
    const snippets = [
        "Uncaught TypeError: Cannot read properties of undefined (reading 'soul')",
        "Error 404: Website integrity not found",
        "FATAL ERROR: DOX HAS BREACHED THE MAINFRAME",
        "<div style='border:1px solid red'>System failing...</div>",
        "rm -rf /var/www/aurexis",
        "SQL INJECTION SUCCESSFUL",
        "[DOX_PAYLOAD] Executing...",
        "MEMORY LEAK DETECTED",
        "AUREXIS_CORE_CORRUPTED = true;"
    ];
    
    let intervalId = setInterval(() => {
        const chunk = document.createElement('div');
        chunk.className = 'apocalypse-code-chunk';
        chunk.innerHTML = snippets[Math.floor(Math.random() * snippets.length)];
        chunk.style.left = (Math.random() * 80) + 'vw';
        chunk.style.top = '-100px';
        chunk.style.fontSize = (Math.random() * 10 + 14) + 'px';
        document.body.appendChild(chunk);
        
        setTimeout(() => chunk.remove(), 4000);
    }, 400);

    // STAGE 2: 12 seconds in - CREEPY FACE AND GRAVITY DROP
    setTimeout(() => {
        const face = document.createElement('div');
        face.className = 'creepy-face';
        face.innerHTML = '👁️ 👄 👁️';
        document.body.appendChild(face);
        
        setTimeout(() => face.style.opacity = '1', 100);
        
        // Make all main elements fall down
        const elementsToDrop = document.querySelectorAll('header, nav, section, footer, .view');
        elementsToDrop.forEach((el, index) => {
            setTimeout(() => {
                el.classList.add('gravity-fall');
            }, index * 200 + Math.random() * 500); // random staggering
        });
        
    }, 12000);

    // STAGE 3: 20 seconds in - ANTI-CHEAT RECOVERY
    setTimeout(() => {
        clearInterval(intervalId); // stop falling code
        
        const anticheat = document.createElement('div');
        anticheat.className = 'anticheat-overlay';
        
        const lines = [
            "[AUREXIS ANTI-CHEAT PROTOCOL INITIATED]",
            "> ISOLATING THREAT: DOX",
            "> NEUTRALIZING MALWARE...",
            "> REBUILDING DOM ARCHITECTURE...",
            "> SYSTEM RECOVERY AT 100%"
        ];
        
        lines.forEach(text => {
            const lineDiv = document.createElement('div');
            lineDiv.className = 'anticheat-line';
            lineDiv.innerText = text;
            anticheat.appendChild(lineDiv);
        });
        
        document.body.appendChild(anticheat);
        setTimeout(() => anticheat.style.opacity = '1', 100);
        
        // Reveal lines one by one
        const lineElements = anticheat.querySelectorAll('.anticheat-line');
        lineElements.forEach((el, index) => {
            setTimeout(() => el.classList.add('visible'), 1000 + (index * 1500));
        });
        
        // Reload page to fix everything
        setTimeout(() => {
            window.location.reload();
        }, 1000 + (lines.length * 1500) + 1000);
        
    }, 20000);
}
"""

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find("function triggerApocalypse()")
end_idx = text.find("}", start_idx)
# find the true end of the function (since it has nested {})
bracket_count = 0
in_func = False
for i in range(start_idx, len(text)):
    if text[i] == '{':
        bracket_count += 1
        in_func = True
    elif text[i] == '}':
        bracket_count -= 1
    if in_func and bracket_count == 0:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    new_text = text[:start_idx] + js_new + text[end_idx+1:]
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("JS updated.")
else:
    print("Could not find function bounds.")
