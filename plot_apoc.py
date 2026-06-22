import os
import re

css_code = """
/* --- STAGE 3: RECOVERY AND DRONES --- */
.gravity-restore {
    animation: gravity-restore 3s cubic-bezier(0.25, 1, 0.5, 1) forwards !important;
}

@keyframes gravity-restore {
    0% { transform: translateY(150vh) rotate(45deg); opacity: 0; }
    100% { transform: translateY(0) rotate(0deg); opacity: 1; }
}

.recovery-drone {
    position: fixed;
    width: 8px; height: 8px;
    background: #00ffaa;
    border-radius: 50%;
    box-shadow: 0 0 15px #00ffaa, 0 0 30px #00ffaa;
    z-index: 9999;
    pointer-events: none;
    animation: drone-fly 4s ease-out forwards;
}

@keyframes drone-fly {
    0% { transform: translateY(110vh) scale(1.5); opacity: 1; }
    100% { transform: translateY(-20vh) scale(0.1); opacity: 0; }
}
"""

with open('static/style.css', 'a', encoding='utf-8') as f:
    f.write(css_code)

js_new = """
function triggerApocalypse() {
    if(document.body.classList.contains('apocalypse-mode')) return;
    document.body.classList.add('apocalypse-mode');
    
    // Low drone sound
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(40, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(10, audioCtx.currentTime + 3);
        gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 3);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 3);
    } catch(e) {}
    
    // Falling code chunks
    const snippets = [
        "DOX HAS BREACHED THE MAINFRAME",
        "rm -rf /var/www/aurexis",
        "SQL INJECTION SUCCESSFUL",
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
    }, 300);

    // STAGE 1: Gravity Drop
    const elementsToDrop = document.querySelectorAll('header, nav, section, footer, .view');
    setTimeout(() => {
        elementsToDrop.forEach((el, index) => {
            setTimeout(() => {
                el.classList.add('gravity-fall');
            }, index * 200 + Math.random() * 500);
        });
    }, 4000);

    // STAGE 2: Anti-Cheat Terminal
    setTimeout(() => {
        clearInterval(intervalId); // Stop falling code
        
        const anticheat = document.createElement('div');
        anticheat.className = 'anticheat-overlay';
        
        const lines = [
            "[AUREXIS ANTI-CHEAT PROTOCOL INITIATED]",
            "> ISOLATING THREAT: DOX",
            "> NEUTRALIZING MALWARE...",
            "> DELETING DOX...",
            "> ERROR: ACCESS DENIED.",
            "> DELETION FAILED. DOX IS IMMORTAL.",
            "> INITIATING EMERGENCY DOM RECOVERY..."
        ];
        
        document.body.appendChild(anticheat);
        setTimeout(() => anticheat.style.opacity = '1', 100);
        
        lines.forEach((text, index) => {
            setTimeout(() => {
                const lineDiv = document.createElement('div');
                lineDiv.className = 'anticheat-line visible';
                if (text.includes("FAILED") || text.includes("ERROR") || text.includes("IMMORTAL")) {
                    lineDiv.style.color = '#ff0033';
                    lineDiv.style.textShadow = '0 0 10px #ff0033';
                }
                lineDiv.innerText = text;
                anticheat.appendChild(lineDiv);
            }, 1000 + (index * 1500));
        });
        
        // STAGE 3: Recovery with Drones
        const totalLinesTime = 1000 + (lines.length * 1500) + 2000;
        setTimeout(() => {
            anticheat.style.opacity = '0';
            setTimeout(() => anticheat.remove(), 2000);
            
            // Remove apocalypse classes except maybe a subtle red tint
            document.body.classList.remove('apocalypse-mode');
            
            // Drones swarm to lift elements
            let droneInterval = setInterval(() => {
                const drone = document.createElement('div');
                drone.className = 'recovery-drone';
                drone.style.left = (Math.random() * 100) + 'vw';
                drone.style.animationDuration = (2 + Math.random() * 3) + 's';
                document.body.appendChild(drone);
                setTimeout(() => drone.remove(), 5000);
            }, 50);
            
            // Elements fly back up
            elementsToDrop.forEach((el, index) => {
                setTimeout(() => {
                    el.classList.remove('gravity-fall');
                    el.classList.add('gravity-restore');
                }, index * 100 + Math.random() * 300);
            });
            
            // Stop drones after a while
            setTimeout(() => {
                clearInterval(droneInterval);
                // Clean up animation classes
                elementsToDrop.forEach(el => el.classList.remove('gravity-restore'));
            }, 5000);
            
        }, totalLinesTime);
        
    }, 10000);
}
"""

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace triggerApocalypse entirely
pattern = re.compile(r'function triggerApocalypse\(\)\s*\{.*?(?=\n\}\n(?:$|function|let|const|var|if|document))\}', re.DOTALL)
match = pattern.search(text)

if match:
    new_text = text[:match.start()] + js_new + text[match.end():]
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("JS successfully replaced with the complex storyline.")
else:
    print("Regex failed to find function bounds.")
