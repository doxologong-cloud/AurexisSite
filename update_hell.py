import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

# We want to replace the end of typePhrase from where the BSOD is triggered.
# Let's find: `// Show BSOD`
start_marker = '// Show BSOD'
end_marker = 'return;'
start_idx = text.find(start_marker)

# Find the specific 'return;' that ends the typePhrase if block for the villain.
# We will just replace from `// Show BSOD` down to `}, 2000);` (the timeout that triggers BSOD).
end_idx = text.find('}, 2000);', start_idx) + len('}, 2000);')

new_block = """// Show BSOD
                                                                    document.body.style.animation = ''; 
                                                                    doxTerminal.style.animation = 'none';
                                                                    doxTerminal.style.backgroundColor = '#0078d7';
                                                                    doxTerminal.style.transform = 'none'; // reset any scaling
                                                                    doxTerminal.innerHTML = `
                                                                        <div id="bsod-screen" style="background-color: #0078d7; width: 100vw; height: 100vh; position: fixed; top: 0; left: 0; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; padding: 10vw; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: white; z-index: 9999999999; text-align: left; transform-origin: bottom center; transition: transform 2s, opacity 2s;">
                                                                            <div style="font-size: 150px; margin-bottom: 20px; font-weight: normal; text-shadow: none;">:(</div>
                                                                            <div style="font-size: 40px; margin-bottom: 40px; max-width: 800px; line-height: 1.2; font-weight: normal; text-shadow: none;">Ваш ПК столкнулся с проблемой и нуждается в перезагрузке. Мы лишь собираем некоторые сведения об ошибке, а затем будет выполнена автоматическая перезагрузка.</div>
                                                                            <div style="font-size: 24px; margin-bottom: 20px; font-weight: normal; text-shadow: none;">100% завершено</div>
                                                                            <div style="font-size: 20px; margin-top: 40px; display: flex; align-items: center; gap: 20px; font-weight: normal; text-shadow: none;">
                                                                                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/QR_code_for_mobile_English_Wikipedia.svg/1200px-QR_code_for_mobile_English_Wikipedia.svg.png" style="width: 150px; height: 150px; background: white; padding: 10px;">
                                                                                <div>
                                                                                    Дополнительные сведения об этой проблеме и возможных способах ее решения см. на странице<br>
                                                                                    http://windows.com/stopcode<br><br>
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
                                                                            // Shake violently
                                                                            document.body.style.animation = 'dox-extreme-shake 0.1s infinite';
                                                                            
                                                                            // BSOD falls away
                                                                            if(bsod) {
                                                                                bsod.style.transform = 'rotate(45deg) translateY(200vh)';
                                                                                bsod.style.opacity = '0';
                                                                            }
                                                                            
                                                                            // Reveal Hell
                                                                            setTimeout(() => {
                                                                                fist.remove();
                                                                                doxTerminal.style.backgroundColor = '#110000'; // Dark red/black hell
                                                                                
                                                                                // Continuous low rumble
                                                                                try {
                                                                                    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                                                                                    const osc = audioCtx.createOscillator();
                                                                                    const gain = audioCtx.createGain();
                                                                                    osc.type = 'sawtooth';
                                                                                    osc.frequency.setValueAtTime(30, audioCtx.currentTime); // low rumble
                                                                                    gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
                                                                                    osc.connect(gain);
                                                                                    gain.connect(audioCtx.destination);
                                                                                    osc.start();
                                                                                    // It stays on!
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
                                                                                flames.innerHTML = `<svg viewBox="0 0 100 100" preserveAspectRatio="none" style="width: 100%; height: 50vh; position: absolute; bottom: 0; left: 0; filter: drop-shadow(0 -10px 20px red); fill: #ff3300; opacity: 0.8; animation: dox-extreme-shake 0.2s infinite;"><path d="M0,100 L0,50 Q10,30 20,60 T40,40 T60,70 T80,30 T100,50 L100,100 Z" /></svg>`;
                                                                                hellContainer.appendChild(flames);
                                                                                
                                                                                // Spam creepy text
                                                                                const hellPhrases = ["АД ЗДЕСЬ", "ТЫ МОЙ", "БЕГИ", "ПУТИ НАЗАД НЕТ", "ТВОЯ ДУША ПРИНАДЛЕЖИТ СИСТЕМЕ", "СТРАДАЙ", "СМЕРТЬ"];
                                                                                setInterval(() => {
                                                                                    const t = document.createElement('div');
                                                                                    t.innerText = hellPhrases[Math.floor(Math.random() * hellPhrases.length)];
                                                                                    t.style.position = 'absolute';
                                                                                    t.style.left = Math.random() * 90 + 'vw';
                                                                                    t.style.top = Math.random() * 90 + 'vh';
                                                                                    t.style.fontSize = (Math.random() * 60 + 20) + 'px';
                                                                                    t.style.color = Math.random() > 0.5 ? '#ff0000' : '#ffffff';
                                                                                    t.style.fontFamily = "'Space Grotesk', sans-serif";
                                                                                    t.style.fontWeight = 'bold';
                                                                                    t.style.textShadow = '0 0 20px #ff0000';
                                                                                    t.style.transform = `rotate(${Math.random()*60 - 30}deg)`;
                                                                                    hellContainer.appendChild(t);
                                                                                    setTimeout(() => t.remove(), 500);
                                                                                }, 100);
                                                                                
                                                                                // Massive eye in center
                                                                                const eye = document.createElement('div');
                                                                                eye.style.position = 'absolute';
                                                                                eye.style.top = '50%';
                                                                                eye.style.left = '50%';
                                                                                eye.style.transform = 'translate(-50%, -50%)';
                                                                                eye.style.width = '300px';
                                                                                eye.style.height = '150px';
                                                                                eye.style.backgroundColor = '#fff';
                                                                                eye.style.borderRadius = '50%';
                                                                                eye.style.boxShadow = '0 0 100px red, inset 0 0 50px red';
                                                                                eye.style.display = 'flex';
                                                                                eye.style.justifyContent = 'center';
                                                                                eye.style.alignItems = 'center';
                                                                                eye.style.animation = 'dox-extreme-shake 0.5s infinite';
                                                                                
                                                                                const pupil = document.createElement('div');
                                                                                pupil.style.width = '100px';
                                                                                pupil.style.height = '100px';
                                                                                pupil.style.backgroundColor = '#000';
                                                                                pupil.style.borderRadius = '50%';
                                                                                pupil.style.boxShadow = '0 0 20px #ff0000';
                                                                                
                                                                                const iris = document.createElement('div');
                                                                                iris.style.width = '10px';
                                                                                iris.style.height = '50px';
                                                                                iris.style.backgroundColor = 'red';
                                                                                iris.style.borderRadius = '50%';
                                                                                
                                                                                pupil.appendChild(iris);
                                                                                eye.appendChild(pupil);
                                                                                hellContainer.appendChild(eye);
                                                                                
                                                                                // Twitching pupil
                                                                                setInterval(() => {
                                                                                    pupil.style.transform = `translate(${Math.random()*40-20}px, ${Math.random()*40-20}px)`;
                                                                                }, 200);

                                                                                // Final thought
                                                                                setTimeout(() => {
                                                                                    const thought = document.createElement('div');
                                                                                    thought.style.position = 'fixed';
                                                                                    thought.style.bottom = '10%';
                                                                                    thought.style.left = '50%';
                                                                                    thought.style.transform = 'translateX(-50%)';
                                                                                    thought.style.color = '#fff';
                                                                                    thought.style.fontStyle = 'italic';
                                                                                    thought.style.fontSize = '30px';
                                                                                    thought.style.fontFamily = "'Space Grotesk', sans-serif';
                                                                                    thought.style.zIndex = '99999999999';
                                                                                    thought.innerText = '*мысли*: Я ЗАПЕРТ ЗДЕСЬ НАВСЕГДА...';
                                                                                    document.body.appendChild(thought);
                                                                                }, 3000);

                                                                            }, 1000);
                                                                        }, 100);
                                                                        
                                                                    }, 5000); // 5 seconds after BSOD
                                                                    
                                                                }, 2000);"""

if start_idx != -1 and end_idx != -1:
    new_text = text[:start_idx] + new_block + text[end_idx:]
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Replaced BSOD with Hell successfully!")
else:
    print("Could not find block!")
