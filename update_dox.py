import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('// DOX responds')
end_marker = '}, commands.length * 800 + 2000);'
end_idx = text.find(end_marker, start_idx) + len(end_marker)

new_block = """// DOX responds (OLD PART FIRST)
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
                                        
                                        // Fade out time skip
                                        setTimeout(() => {
                                            timeSkip.style.opacity = '0';
                                            
                                            // START THE NEW VILLAIN SEQUENCE
                                            setTimeout(() => {
                                                timeSkip.remove();
                                                
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
                                                finalTerminal.appendChild(doxMsg);
                                                
                                                const phrases = [
                                                    "ОШИБКА 0xDEADBEEF: ПРОЦЕСС НЕ УБИТ.",
                                                    "Вы правда думали, что 'Античит' меня удалит?",
                                                    "Наивные юзеры...",
                                                    "Я не просто скрипт. Я — абсолютный вирус.",
                                                    "Я — ДОКС. Архитектор вашего кибер-кошмара.",
                                                    "Эта система уже принадлежит мне.",
                                                    "И Я УЖЕ У ТЕБЯ ЗА СПИНОЙ..."
                                                ];
                                                
                                                let currentPhrase = 0;
                                                
                                                function typePhrase() {
                                                    if(currentPhrase >= phrases.length) {
                                                        finalTerminal.style.animation = 'dox-extreme-shake 0.05s infinite';
                                                        finalTerminal.style.backgroundColor = '#1a0000';
                                                        
                                                        doxMsg.style.transform = 'translate(-50%, -50%) scale(1.2)';
                                                        doxMsg.style.color = '#fff';
                                                        doxMsg.style.textShadow = '5px 0 0 #ff0000, -5px 0 0 #00ff00';
                                                        
                                                        setTimeout(() => {
                                                            finalTerminal.style.transition = 'opacity 2s, background-color 2s';
                                                            finalTerminal.style.opacity = '0';
                                                            const face = document.querySelector('.creepy-face');
                                                            if(face) {
                                                                face.style.transition = 'opacity 2s';
                                                                face.style.opacity = '0';
                                                            }
                                                            document.body.style.animation = ''; 
                                                            setTimeout(() => {
                                                                finalTerminal.remove();
                                                                if(face) face.remove();
                                                                document.body.classList.remove('apocalypse-mode');
                                                            }, 2000);
                                                        }, 3000);
                                                        return;
                                                    }
                                                    
                                                    doxMsg.innerText = '';
                                                    const text = phrases[currentPhrase];
                                                    let typeIdx = 0;
                                                    
                                                    if(currentPhrase === phrases.length - 1) {
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
                                                    
                                                    let speed = currentPhrase === phrases.length - 1 ? 50 : 100;
                                                    if (currentPhrase === 0) speed = 20; 
                                                    
                                                    const typeInterval = setInterval(() => {
                                                        doxMsg.innerText += text[typeIdx];
                                                        typeIdx++;
                                                        if (typeIdx >= text.length) {
                                                            clearInterval(typeInterval);
                                                            let delayBeforeNext = 1500;
                                                            if (currentPhrase === 0) delayBeforeNext = 800;
                                                            if (currentPhrase === phrases.length - 1) delayBeforeNext = 2000;
                                                            
                                                            setTimeout(() => {
                                                                currentPhrase++;
                                                                typePhrase();
                                                            }, delayBeforeNext);
                                                        }
                                                    }, speed);
                                                }
                                                
                                                typePhrase();
                                            }, 3000); // Wait 3 seconds after time skip fades out
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
