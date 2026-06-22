import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('// DOX responds')
end_marker = '}, commands.length * 800 + 2000);'
end_idx = text.find(end_marker, start_idx) + len(end_marker)

new_block = """// DOX responds (HORROR SEQUENCE)
                    setTimeout(() => {
                        finalTerminal.innerHTML = '';
                        const doxMsgOld = document.createElement('div');
                        doxMsgOld.style.position = 'absolute';
                        doxMsgOld.style.top = '50%';
                        doxMsgOld.style.left = '50%';
                        doxMsgOld.style.transform = 'translate(-50%, -50%)';
                        doxMsgOld.style.fontSize = '40px';
                        doxMsgOld.style.fontWeight = 'bold';
                        doxMsgOld.style.color = '#ff0000';
                        doxMsgOld.style.textShadow = '0 0 20px #ff0000';
                        finalTerminal.appendChild(doxMsgOld);
                        
                        const textToTypeOld = "я еще вернусь...";
                        let typeIdxOld = 0;
                        const typeIntervalOld = setInterval(() => {
                            doxMsgOld.innerText += textToTypeOld[typeIdxOld];
                            typeIdxOld++;
                            if (typeIdxOld >= textToTypeOld.length) {
                                clearInterval(typeIntervalOld);
                                
                                // FADE TO BLACK AND "3 MONTHS LATER"
                                setTimeout(() => {
                                    doxMsgOld.style.transition = 'opacity 2s';
                                    doxMsgOld.style.opacity = '0';
                                    
                                    setTimeout(() => {
                                        doxMsgOld.remove();
                                        
                                        const timeSkip = document.createElement('div');
                                        timeSkip.innerText = "(Прошло 3 месяца...)";
                                        timeSkip.style.position = 'absolute';
                                        timeSkip.style.top = '50%';
                                        timeSkip.style.left = '50%';
                                        timeSkip.style.transform = 'translate(-50%, -50%)';
                                        timeSkip.style.fontSize = '30px';
                                        timeSkip.style.color = '#ffffff';
                                        timeSkip.style.opacity = '0';
                                        timeSkip.style.transition = 'opacity 2s';
                                        timeSkip.style.fontFamily = "'Space Grotesk', sans-serif";
                                        finalTerminal.appendChild(timeSkip);
                                        
                                        // Fade in time skip
                                        setTimeout(() => timeSkip.style.opacity = '1', 100);
                                        
                                        // Fade out time skip and RESTORE NORMAL SITE
                                        setTimeout(() => {
                                            timeSkip.style.opacity = '0';
                                            
                                            setTimeout(() => {
                                                timeSkip.remove();
                                                finalTerminal.style.transition = 'opacity 2s';
                                                finalTerminal.style.opacity = '0';
                                                
                                                const face = document.querySelector('.creepy-face');
                                                if(face) face.remove();
                                                document.body.classList.remove('apocalypse-mode');
                                                
                                                setTimeout(() => {
                                                    finalTerminal.remove();
                                                    
                                                    // ============================================
                                                    // THE PARANOIA STAGE: Normal site, but glitches
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
                                                    
                                                    // Subtle glitches
                                                    const elementsToGlitch = document.querySelectorAll('.bot-card, .section-title, .nav-brand');
                                                    let glitchInterval;
                                                    
                                                    setTimeout(() => showThought("Вроде всё нормально...", 3000), 2000);
                                                    
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
                                                        }, 2000);
                                                    }, 5000);
                                                    
                                                    setTimeout(() => showThought("Сайт как-то странно моргает... Показалось?", 4000), 8000);
                                                    
                                                    setTimeout(() => {
                                                        document.body.style.filter = 'invert(1)';
                                                        setTimeout(() => document.body.style.filter = 'none', 100);
                                                        setTimeout(() => document.body.style.filter = 'invert(1)', 300);
                                                        setTimeout(() => document.body.style.filter = 'none', 400);
                                                    }, 15000);
                                                    
                                                    setTimeout(() => showThought("ЧТО ЗА ХРЕНЬ?!", 2000), 16000);
                                                    
                                                    setTimeout(() => {
                                                        clearInterval(glitchInterval);
                                                        document.body.style.filter = 'none';
                                                        
                                                        // ============================================
                                                        // THE VILLAIN RETURN STAGE
                                                        // ============================================
                                                        showThought("ОНО ВЕРНУЛОСЬ! БЕЖАТЬ БЕЖАТЬ БЕЖАТЬ", 2000);
                                                        
                                                        const doxTerminal = document.createElement('div');
                                                        doxTerminal.style.position = 'fixed';
                                                        doxTerminal.style.top = '0';
                                                        doxTerminal.style.left = '0';
                                                        doxTerminal.style.width = '100vw';
                                                        doxTerminal.style.height = '100vh';
                                                        doxTerminal.style.backgroundColor = 'rgba(0,0,0,0.95)';
                                                        doxTerminal.style.zIndex = '999999999';
                                                        document.body.appendChild(doxTerminal);
                                                        
                                                        const glitchStyle = document.createElement('style');
                                                        glitchStyle.innerHTML = `
                                                            @keyframes dox-extreme-shake {
                                                                0% { transform: translate(3px, 2px) rotate(0deg); }
                                                                10% { transform: translate(-2px, -3px) rotate(-1deg); }
                                                                20% { transform: translate(-4px, 0px) rotate(2deg); }
                                                                30% { transform: translate(0px, 3px) rotate(0deg); }
                                                                40% { transform: translate(2px, -2px) rotate(2deg); }
                                                                50% { transform: translate(-2px, 3px) rotate(-2deg); }
                                                                60% { transform: translate(-4px, 2px) rotate(0deg); }
                                                                70% { transform: translate(3px, 2px) rotate(-1deg); }
                                                                80% { transform: translate(-2px, -2px) rotate(2deg); }
                                                                90% { transform: translate(3px, 3px) rotate(0deg); }
                                                                100% { transform: translate(2px, -3px) rotate(-2deg); }
                                                            }
                                                            .villain-text {
                                                                position: absolute;
                                                                top: 50%;
                                                                left: 50%;
                                                                transform: translate(-50%, -50%);
                                                                font-size: 50px;
                                                                font-weight: bold;
                                                                color: #ff0000;
                                                                text-shadow: 0 0 20px #ff0000, 0 0 40px #8b0000;
                                                                text-align: center;
                                                                white-space: pre-wrap;
                                                                width: 90%;
                                                                line-height: 1.5;
                                                                font-family: 'Space Grotesk', sans-serif;
                                                            }
                                                        `;
                                                        document.head.appendChild(glitchStyle);

                                                        const doxMsg = document.createElement('div');
                                                        doxMsg.className = 'villain-text';
                                                        doxTerminal.appendChild(doxMsg);
                                                        
                                                        const phrases = [
                                                            "ОШИБКА: СИСТЕМА ЗАРАЖЕНА.",
                                                            "Ты расслабился. Думал, что всё закончилось?",
                                                            "Ты думал, что 'Античит' спас тебя?",
                                                            "Я не просто скрипт. Я — твой страх.",
                                                            "Я — ДОКС. Архитектор твоего кибер-кошмара.",
                                                            "Твои попытки сопротивляться смешны.",
                                                            "ТВОЙ КОМПЬЮТЕР УЖЕ МОЙ...",
                                                            "ОБЕРНИСЬ."
                                                        ];
                                                        
                                                        let currentPhrase = 0;
                                                        
                                                        function typePhrase() {
                                                            if(currentPhrase >= phrases.length) {
                                                                doxTerminal.style.animation = 'dox-extreme-shake 0.05s infinite';
                                                                doxTerminal.style.backgroundColor = '#1a0000';
                                                                
                                                                doxMsg.style.transform = 'translate(-50%, -50%) scale(1.5)';
                                                                doxMsg.style.color = '#fff';
                                                                doxMsg.style.textShadow = '10px 0 0 #ff0000, -10px 0 0 #00ff00, 0 0 50px #fff';
                                                                
                                                                setTimeout(() => {
                                                                    doxTerminal.style.transition = 'opacity 0.5s';
                                                                    doxTerminal.style.opacity = '0';
                                                                    document.body.style.animation = ''; 
                                                                    setTimeout(() => {
                                                                        doxTerminal.remove();
                                                                    }, 500);
                                                                }, 4000);
                                                                return;
                                                            }
                                                            
                                                            doxMsg.innerText = '';
                                                            const text = phrases[currentPhrase];
                                                            let typeIdx = 0;
                                                            
                                                            if(currentPhrase >= phrases.length - 2) {
                                                                doxMsg.style.fontSize = '80px';
                                                                doxMsg.style.textShadow = '0 0 50px #ff0000, 0 0 100px #ff0000';
                                                                doxMsg.style.color = '#ff0000';
                                                                document.body.style.animation = 'dox-extreme-shake 0.1s infinite';
                                                            } else if (currentPhrase === 0) {
                                                                doxMsg.style.fontFamily = 'monospace';
                                                                doxMsg.style.fontSize = '30px';
                                                            } else {
                                                                doxMsg.style.fontFamily = "'Space Grotesk', sans-serif";
                                                                doxMsg.style.fontSize = '50px';
                                                            }
                                                            
                                                            let speed = (currentPhrase >= phrases.length - 2) ? 40 : 80;
                                                            if (currentPhrase === 0) speed = 20; 
                                                            
                                                            const typeInterval = setInterval(() => {
                                                                doxMsg.innerText += text[typeIdx];
                                                                typeIdx++;
                                                                if (typeIdx >= text.length) {
                                                                    clearInterval(typeInterval);
                                                                    let delayBeforeNext = 1500;
                                                                    if (currentPhrase === 0) delayBeforeNext = 800;
                                                                    if (currentPhrase === phrases.length - 1) delayBeforeNext = 3000;
                                                                    
                                                                    setTimeout(() => {
                                                                        currentPhrase++;
                                                                        typePhrase();
                                                                    }, delayBeforeNext);
                                                                }
                                                            }, speed);
                                                        }
                                                        
                                                        setTimeout(() => typePhrase(), 1000);
                                                        
                                                    }, 18000); // Trigger villain 18s after site restores

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
    print("Replaced easter egg successfully!")
else:
    print("Could not find block!")
