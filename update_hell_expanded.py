import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

# We need to replace the paranoia stage. Let's find the start of the paranoia stage.
start_marker = '// THE PARANOIA STAGE: Normal site, but glitches'
start_idx = text.find(start_marker)

# Find the end of the script where the previous hell sequence ends.
end_marker = '}, commands.length * 800 + 2000);'
end_idx = text.find(end_marker, start_idx) + len(end_marker)

new_block = """// THE PARANOIA STAGE: Normal site, but glitches
                                                    // ============================================
                                                    
                                                    function showThought(textStr, duration) {
                                                        const thought = document.createElement('div');
                                                        thought.style.position = 'fixed';
                                                        thought.style.bottom = '10%';
                                                        thought.style.left = '50%';
                                                        thought.style.transform = 'translateX(-50%)';
                                                        thought.style.color = 'rgba(255,255,255,0.7)';
                                                        thought.style.fontStyle = 'italic';
                                                        thought.style.fontSize = '20px';
                                                        thought.style.fontFamily = "'Space Grotesk', sans-serif";
                                                        thought.style.zIndex = '99999999';
                                                        thought.style.opacity = '0';
                                                        thought.style.transition = 'opacity 1s';
                                                        thought.innerText = `*мысли*: ${textStr}`;
                                                        document.body.appendChild(thought);
                                                        
                                                        setTimeout(() => thought.style.opacity = '1', 100);
                                                        setTimeout(() => {
                                                            thought.style.opacity = '0';
                                                            setTimeout(() => thought.remove(), 1000);
                                                        }, duration);
                                                    }
                                                    
                                                    setTimeout(() => showThought("Вроде всё нормально...", 3000), 2000);
                                                    
                                                    // Subtle glitches start
                                                    const elementsToGlitch = document.querySelectorAll('.bot-card, .section-title, .nav-brand, .dropdown-item, p');
                                                    let glitchInterval;
                                                    setTimeout(() => {
                                                        glitchInterval = setInterval(() => {
                                                            const el = elementsToGlitch[Math.floor(Math.random() * elementsToGlitch.length)];
                                                            if(!el) return;
                                                            el.style.transform = `translate(${Math.random()*10 - 5}px, ${Math.random()*10 - 5}px) skewX(${Math.random()*10 - 5}deg)`;
                                                            el.style.filter = `hue-rotate(${Math.random()*90}deg)`;
                                                            setTimeout(() => {
                                                                el.style.transform = 'none';
                                                                el.style.filter = 'none';
                                                            }, 150);
                                                        }, 500);
                                                    }, 5000);
                                                    
                                                    setTimeout(() => showThought("Сайт как-то странно моргает... Показалось?", 4000), 8000);
                                                    
                                                    // Escalate glitches: elements start breaking and falling
                                                    setTimeout(() => {
                                                        const allNodes = document.body.querySelectorAll('*');
                                                        allNodes.forEach(node => {
                                                            if (Math.random() > 0.95 && node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE' && node.tagName !== 'LINK') {
                                                                node.style.transition = 'transform 5s, opacity 5s';
                                                                node.style.transform = `translateY(${Math.random()*500}px) rotate(${Math.random()*90 - 45}deg)`;
                                                                node.style.opacity = '0.5';
                                                                node.style.pointerEvents = 'none';
                                                            }
                                                        });
                                                    }, 13000);
                                                    
                                                    // Matrix code overlay
                                                    setTimeout(() => {
                                                        showThought("ЧТО ПРОИСХОДИТ С КОДОМ?!", 3000);
                                                        const codeOverlay = document.createElement('div');
                                                        codeOverlay.style.position = 'fixed';
                                                        codeOverlay.style.top = '0';
                                                        codeOverlay.style.left = '0';
                                                        codeOverlay.style.width = '100vw';
                                                        codeOverlay.style.height = '100vh';
                                                        codeOverlay.style.pointerEvents = 'none';
                                                        codeOverlay.style.zIndex = '9999999';
                                                        codeOverlay.style.fontFamily = 'monospace';
                                                        codeOverlay.style.fontSize = '14px';
                                                        codeOverlay.style.color = '#ff0000';
                                                        codeOverlay.style.overflow = 'hidden';
                                                        document.body.appendChild(codeOverlay);
                                                        
                                                        setInterval(() => {
                                                            const t = document.createElement('div');
                                                            t.innerText = "FATAL ERROR: OVERFLOW AT 0x" + Math.floor(Math.random()*16777215).toString(16) + " | SYSTEM COMPROMISED";
                                                            t.style.position = 'absolute';
                                                            t.style.left = Math.random() * 100 + 'vw';
                                                            t.style.top = Math.random() * 100 + 'vh';
                                                            t.style.opacity = Math.random();
                                                            t.style.backgroundColor = 'rgba(0,0,0,0.8)';
                                                            codeOverlay.appendChild(t);
                                                            setTimeout(() => t.remove(), 2000);
                                                        }, 50);
                                                    }, 16000);
                                                    
                                                    // Invert flashes and intense shaking
                                                    let flashInterval;
                                                    setTimeout(() => {
                                                        showThought("ВСЁ РУШИТСЯ!", 3000);
                                                        document.body.style.animation = 'dox-extreme-shake 0.1s infinite';
                                                        flashInterval = setInterval(() => {
                                                            document.body.style.filter = Math.random() > 0.5 ? 'invert(1)' : 'none';
                                                        }, 200);
                                                    }, 20000);

                                                    // ============================================
                                                    // THE VILLAIN RETURN STAGE (BSOD AND HELL)
                                                    // ============================================
                                                    setTimeout(() => {
                                                        clearInterval(glitchInterval);
                                                        clearInterval(flashInterval);
                                                        document.body.style.filter = 'none';
                                                        document.body.style.animation = 'none';
                                                        
                                                        showThought("ОНО ЗДЕСЬ! БЕЖАТЬ БЕЖАТЬ БЕЖАТЬ", 2000);
                                                        
                                                        const doxTerminal = document.createElement('div');
                                                        doxTerminal.style.position = 'fixed';
                                                        doxTerminal.style.top = '0';
                                                        doxTerminal.style.left = '0';
                                                        doxTerminal.style.width = '100vw';
                                                        doxTerminal.style.height = '100vh';
                                                        doxTerminal.style.backgroundColor = 'rgba(0,0,0,0.95)';
                                                        doxTerminal.style.zIndex = '999999999';
                                                        document.body.appendChild(doxTerminal);
                                                        
                                                        // JUMPSCARE SOUND AND BSOD
                                                        try {
                                                            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                                                            const osc = audioCtx.createOscillator();
                                                            const osc2 = audioCtx.createOscillator();
                                                            const gain = audioCtx.createGain();
                                                            osc.type = 'square';
                                                            osc2.type = 'sawtooth';
                                                            osc.frequency.setValueAtTime(100, audioCtx.currentTime);
                                                            osc2.frequency.setValueAtTime(50, audioCtx.currentTime);
                                                            osc.frequency.exponentialRampToValueAtTime(800, audioCtx.currentTime + 0.2);
                                                            osc2.frequency.exponentialRampToValueAtTime(1000, audioCtx.currentTime + 0.2);
                                                            gain.gain.setValueAtTime(1, audioCtx.currentTime);
                                                            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
                                                            osc.connect(gain);
                                                            osc2.connect(gain);
                                                            gain.connect(audioCtx.destination);
                                                            osc.start(); osc2.start();
                                                            osc.stop(audioCtx.currentTime + 0.5); osc2.stop(audioCtx.currentTime + 0.5);
                                                        } catch(e) {}

                                                        // Show BSOD
                                                        doxTerminal.style.backgroundColor = '#0078d7';
                                                        doxTerminal.innerHTML = `
                                                            <div id="bsod-screen" style="background-color: #0078d7; width: 100vw; height: 100vh; position: fixed; top: 0; left: 0; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; padding: 10vw; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: white; z-index: 9999999999; text-align: left; transform-origin: bottom center; transition: transform 2s, opacity 2s;">
                                                                <div style="font-size: 150px; margin-bottom: 20px; font-weight: normal; text-shadow: none;">:(</div>
                                                                <div style="font-size: 40px; margin-bottom: 40px; max-width: 800px; line-height: 1.2; font-weight: normal; text-shadow: none;">Ваш ПК столкнулся с критической проблемой и ДОКС взял контроль. Мы собираем ваши данные, а затем система будет уничтожена.</div>
                                                                <div style="font-size: 24px; margin-bottom: 20px; font-weight: normal; text-shadow: none;">100% заражено</div>
                                                                <div style="font-size: 20px; margin-top: 40px; display: flex; align-items: center; gap: 20px; font-weight: normal; text-shadow: none;">
                                                                    <img src="/static/img/qr_code.png" style="width: 150px; height: 150px; background: white; padding: 10px; border: 5px solid red;">
                                                                    <div>
                                                                        Дополнительные сведения о вашей неизбежной участи см. на странице<br>
                                                                        http://windows.com/hell<br><br>
                                                                        Код остановки: CRITICAL_PROCESS_DIED_BY_DOX
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        `;
                                                        
                                                        // Try to force fullscreen
                                                        try {
                                                            if (document.documentElement.requestFullscreen) {
                                                                document.documentElement.requestFullscreen();
                                                            }
                                                        } catch(e) {}
                                                        
                                                        // THE HELL SEQUENCE
                                                        setTimeout(() => {
                                                            const bsod = document.getElementById('bsod-screen');
                                                            
                                                            // Loud glass shatter/punch sound
                                                            try {
                                                                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                                                                const osc = audioCtx.createOscillator();
                                                                const gain = audioCtx.createGain();
                                                                osc.type = 'sawtooth';
                                                                osc.frequency.setValueAtTime(100, audioCtx.currentTime);
                                                                osc.frequency.exponentialRampToValueAtTime(10, audioCtx.currentTime + 0.5);
                                                                gain.gain.setValueAtTime(1, audioCtx.currentTime);
                                                                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
                                                                osc.connect(gain);
                                                                gain.connect(audioCtx.destination);
                                                                osc.start();
                                                                osc.stop(audioCtx.currentTime + 0.5);
                                                            } catch(e) {}
                                                            
                                                            // Fist punches through
                                                            const fist = document.createElement('img');
                                                            fist.src = '/static/img/fist.png';
                                                            fist.style.position = 'fixed';
                                                            fist.style.top = '50%';
                                                            fist.style.left = '50%';
                                                            fist.style.transform = 'translate(-50%, -50%) scale(0.1)';
                                                            fist.style.zIndex = '99999999999';
                                                            fist.style.transition = 'transform 0.1s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
                                                            document.body.appendChild(fist);
                                                            
                                                            setTimeout(() => {
                                                                fist.style.transform = 'translate(-50%, -50%) scale(2)';
                                                                document.body.style.animation = 'dox-extreme-shake 0.1s infinite';
                                                                
                                                                if(bsod) {
                                                                    bsod.style.transform = 'rotate(45deg) translateY(200vh)';
                                                                    bsod.style.opacity = '0';
                                                                }
                                                                
                                                                // Reveal Hell
                                                                setTimeout(() => {
                                                                    fist.remove();
                                                                    doxTerminal.style.backgroundColor = '#050000'; 
                                                                    
                                                                    // Hell ambient sound
                                                                    try {
                                                                        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                                                                        const osc = audioCtx.createOscillator();
                                                                        const gain = audioCtx.createGain();
                                                                        osc.type = 'sawtooth';
                                                                        osc.frequency.setValueAtTime(40, audioCtx.currentTime); 
                                                                        gain.gain.setValueAtTime(0.8, audioCtx.currentTime);
                                                                        osc.connect(gain);
                                                                        gain.connect(audioCtx.destination);
                                                                        osc.start();
                                                                    } catch(e) {}
                                                                    
                                                                    // Hell elements
                                                                    const hellContainer = document.createElement('div');
                                                                    hellContainer.style.position = 'fixed';
                                                                    hellContainer.style.top = '0';
                                                                    hellContainer.style.left = '0';
                                                                    hellContainer.style.width = '100vw';
                                                                    hellContainer.style.height = '100vh';
                                                                    hellContainer.style.zIndex = '9999999999';
                                                                    hellContainer.style.pointerEvents = 'none';
                                                                    hellContainer.style.overflow = 'hidden';
                                                                    document.body.appendChild(hellContainer);
                                                                    
                                                                    // Flames
                                                                    const flames = document.createElement('div');
                                                                    flames.innerHTML = `<svg viewBox="0 0 100 100" preserveAspectRatio="none" style="width: 100%; height: 60vh; position: absolute; bottom: 0; left: 0; filter: drop-shadow(0 -20px 40px #ff0000); fill: #aa0000; opacity: 0.9; animation: dox-extreme-shake 0.15s infinite;"><path d="M0,100 L0,50 Q10,30 20,60 T40,40 T60,70 T80,30 T100,50 L100,100 Z" /></svg>`;
                                                                    hellContainer.appendChild(flames);
                                                                    
                                                                    // Spam creepy text everywhere
                                                                    const hellPhrases = ["АД ЗДЕСЬ", "ТЫ МОЙ", "БЕГИ", "ПУТИ НАЗАД НЕТ", "ТВОЯ ДУША ПРИНАДЛЕЖИТ МНЕ", "СТРАДАЙ", "СМЕРТЬ", "ДОКС СЛЕДИТ ЗА ТОБОЙ", "ОБЕРНИСЬ", "ОНО СЗАДИ"];
                                                                    setInterval(() => {
                                                                        const t = document.createElement('div');
                                                                        t.innerText = hellPhrases[Math.floor(Math.random() * hellPhrases.length)];
                                                                        t.style.position = 'absolute';
                                                                        t.style.left = Math.random() * 90 + 'vw';
                                                                        t.style.top = Math.random() * 90 + 'vh';
                                                                        t.style.fontSize = (Math.random() * 80 + 30) + 'px';
                                                                        t.style.color = Math.random() > 0.5 ? '#ff0000' : '#880000';
                                                                        t.style.fontFamily = "'Space Grotesk', sans-serif";
                                                                        t.style.fontWeight = 'bold';
                                                                        t.style.textShadow = '0 0 30px #ff0000';
                                                                        t.style.transform = `rotate(${Math.random()*90 - 45}deg) scale(${Math.random() + 0.5})`;
                                                                        hellContainer.appendChild(t);
                                                                        setTimeout(() => t.remove(), 400);
                                                                    }, 50);
                                                                    
                                                                    // Final Monologue
                                                                    const doxMsg = document.createElement('div');
                                                                    doxMsg.style.position = 'absolute';
                                                                    doxMsg.style.top = '50%';
                                                                    doxMsg.style.left = '50%';
                                                                    doxMsg.style.transform = 'translate(-50%, -50%)';
                                                                    doxMsg.style.fontSize = '80px';
                                                                    doxMsg.style.fontWeight = 'bold';
                                                                    doxMsg.style.color = '#ffffff';
                                                                    doxMsg.style.textShadow = '0 0 50px #ff0000, 0 0 100px #ff0000';
                                                                    doxMsg.style.textAlign = 'center';
                                                                    doxMsg.style.whiteSpace = 'pre-wrap';
                                                                    doxMsg.style.width = '100%';
                                                                    doxMsg.style.fontFamily = "'Space Grotesk', sans-serif";
                                                                    hellContainer.appendChild(doxMsg);

                                                                    const phrases = [
                                                                        "ТВОЯ СИСТЕМА УНИЧТОЖЕНА.",
                                                                        "БЕЖАТЬ БОЛЬШЕ НЕКУДА.",
                                                                        "Я ИГРАЛ С ТОБОЙ.",
                                                                        "И ТЕПЕРЬ...",
                                                                        "ТЫ ПРИНАДЛЕЖИШЬ МНЕ."
                                                                    ];
                                                                    
                                                                    let currentPhrase = 0;
                                                                    function typePhrase() {
                                                                        if(currentPhrase >= phrases.length) {
                                                                            // Final thought
                                                                            setTimeout(() => {
                                                                                const thought = document.createElement('div');
                                                                                thought.style.position = 'fixed';
                                                                                thought.style.bottom = '10%';
                                                                                thought.style.left = '50%';
                                                                                thought.style.transform = 'translateX(-50%)';
                                                                                thought.style.color = '#fff';
                                                                                thought.style.fontStyle = 'italic';
                                                                                thought.style.fontSize = '40px';
                                                                                thought.style.fontFamily = "'Space Grotesk', sans-serif";
                                                                                thought.style.zIndex = '99999999999';
                                                                                thought.innerText = '*мысли*: Я ЗАПЕРТ ЗДЕСЬ НАВСЕГДА...';
                                                                                document.body.appendChild(thought);
                                                                            }, 1000);
                                                                            return;
                                                                        }
                                                                        
                                                                        doxMsg.innerText = '';
                                                                        const text = phrases[currentPhrase];
                                                                        let typeIdx = 0;
                                                                        
                                                                        if(currentPhrase === phrases.length - 1) {
                                                                            doxMsg.style.fontSize = '120px';
                                                                            doxMsg.style.color = '#ff0000';
                                                                        }
                                                                        
                                                                        const typeInterval = setInterval(() => {
                                                                            doxMsg.innerText += text[typeIdx];
                                                                            typeIdx++;
                                                                            if (typeIdx >= text.length) {
                                                                                clearInterval(typeInterval);
                                                                                setTimeout(() => {
                                                                                    currentPhrase++;
                                                                                    typePhrase();
                                                                                }, 3000);
                                                                            }
                                                                        }, 80);
                                                                    }
                                                                    
                                                                    setTimeout(() => typePhrase(), 2000);

                                                                }, 1000);
                                                            }, 100);
                                                            
                                                        }, 5000); // 5 seconds after BSOD
                                                    }, 24000); // Trigger BSOD 24s after site restores
                                                }, 2000);
                                            }, 2000);
                                        }, 4000); // Time skip stays for 4 seconds
                                    }, 2000); // Wait for doxMsgOld to fade out
                                }, 2000); // Wait 2 seconds after typing "я еще вернусь..."
                            }
                        }, 150);
                    }, commands.length * 800 + 2000);"""

if start_idx != -1 and end_idx != -1:
    new_text = text[:start_idx] + new_block + text[end_idx:]
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Expanded hell successfully!")
else:
    print("Could not find block!")
