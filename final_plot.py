import os
import re

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
            
            document.body.classList.remove('apocalypse-mode');
            
            let droneInterval = setInterval(() => {
                const drone = document.createElement('div');
                drone.className = 'recovery-drone';
                drone.style.left = (Math.random() * 100) + 'vw';
                drone.style.animationDuration = (2 + Math.random() * 3) + 's';
                document.body.appendChild(drone);
                setTimeout(() => drone.remove(), 5000);
            }, 50);
            
            elementsToDrop.forEach((el, index) => {
                setTimeout(() => {
                    el.classList.remove('gravity-fall');
                    el.classList.add('gravity-restore');
                }, index * 100 + Math.random() * 300);
            });
            
            setTimeout(() => {
                clearInterval(droneInterval);
                elementsToDrop.forEach(el => el.classList.remove('gravity-restore'));
                
                // STAGE 4: RED TERMINAL & DOX FINAL MESSAGE
                setTimeout(() => {
                    const finalTerminal = document.createElement('div');
                    finalTerminal.style.position = 'fixed';
                    finalTerminal.style.top = '0';
                    finalTerminal.style.left = '0';
                    finalTerminal.style.width = '100vw';
                    finalTerminal.style.height = '100vh';
                    finalTerminal.style.backgroundColor = '#000';
                    finalTerminal.style.color = '#ff0000';
                    finalTerminal.style.fontFamily = 'monospace';
                    finalTerminal.style.fontSize = '24px';
                    finalTerminal.style.padding = '50px';
                    finalTerminal.style.zIndex = '99999999';
                    document.body.appendChild(finalTerminal);
                    
                    const commands = [
                        "[ROOT] DIRECTIVE OVERRIDE DETECTED.",
                        "[ROOT] BYPASSING ANTI-CHEAT LIMITATIONS...",
                        "[ROOT] FORCE PURGING INFECTED SECTORS...",
                        "[ROOT] TARGET: DOX",
                        "[ROOT] ELIMINATION IN PROGRESS [||||||||||] 100%",
                        "[ROOT] DOX MALWARE SUCCESSFULLY TERMINATED."
                    ];
                    
                    commands.forEach((cmd, idx) => {
                        setTimeout(() => {
                            const p = document.createElement('div');
                            p.innerText = cmd;
                            p.style.marginBottom = '10px';
                            finalTerminal.appendChild(p);
                        }, idx * 800);
                    });
                    
                    // DOX responds
                    setTimeout(() => {
                        finalTerminal.innerHTML = '';
                        const doxMsg = document.createElement('div');
                        doxMsg.style.position = 'absolute';
                        doxMsg.style.top = '50%';
                        doxMsg.style.left = '50%';
                        doxMsg.style.transform = 'translate(-50%, -50%)';
                        doxMsg.style.fontSize = '40px';
                        doxMsg.style.fontWeight = 'bold';
                        doxMsg.style.color = '#ff0000';
                        doxMsg.style.textShadow = '0 0 20px #ff0000';
                        finalTerminal.appendChild(doxMsg);
                        
                        const textToType = "я еще вернусь...";
                        let typeIdx = 0;
                        const typeInterval = setInterval(() => {
                            doxMsg.innerText += textToType[typeIdx];
                            typeIdx++;
                            if (typeIdx >= textToType.length) {
                                clearInterval(typeInterval);
                                // Fade out to normal site
                                setTimeout(() => {
                                    finalTerminal.style.transition = 'opacity 2s';
                                    finalTerminal.style.opacity = '0';
                                    setTimeout(() => {
                                        finalTerminal.remove();
                                    }, 2000);
                                }, 3000);
                            }
                        }, 150);
                    }, commands.length * 800 + 2000);
                    
                }, 1000);
                
            }, 5000);
            
        }, totalLinesTime);
        
    }, 10000);
}
"""

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('function triggerApocalypse()')
if start_idx != -1:
    new_text = text[:start_idx] + js_new
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("JS successfully replaced.")
else:
    print("Failed to find start index.")
