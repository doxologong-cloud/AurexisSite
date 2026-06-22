import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

easter_egg_js = """
// ==========================================
// EASTER EGGS
// ==========================================

function handleEasterEgg(eggCode) {
    if(eggCode === 'matrix') {
        const matrixCanvas = document.createElement('canvas');
        matrixCanvas.id = 'matrix-canvas';
        matrixCanvas.style.position = 'fixed';
        matrixCanvas.style.top = '0';
        matrixCanvas.style.left = '0';
        matrixCanvas.style.width = '100vw';
        matrixCanvas.style.height = '100vh';
        matrixCanvas.style.zIndex = '9999';
        matrixCanvas.style.pointerEvents = 'none';
        document.body.appendChild(matrixCanvas);
        
        const ctx = matrixCanvas.getContext('2d');
        matrixCanvas.width = window.innerWidth;
        matrixCanvas.height = window.innerHeight;
        
        const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレゲゼデベペオォコソトノホモヨョロゴゾドボポヴッン';
        const latin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        const nums = '0123456789';
        const alphabet = katakana + latin + nums;
        
        const fontSize = 16;
        const columns = matrixCanvas.width / fontSize;
        const drops = [];
        for(let x = 0; x < columns; x++) drops[x] = 1;
        
        const matrixInterval = setInterval(() => {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, matrixCanvas.width, matrixCanvas.height);
            
            ctx.fillStyle = '#0F0';
            ctx.font = fontSize + 'px monospace';
            
            for(let i = 0; i < drops.length; i++) {
                const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                
                if(drops[i] * fontSize > matrixCanvas.height && Math.random() > 0.975)
                    drops[i] = 0;
                
                drops[i]++;
            }
        }, 30);
        
        setTimeout(() => {
            clearInterval(matrixInterval);
            matrixCanvas.style.transition = 'opacity 2s';
            matrixCanvas.style.opacity = '0';
            setTimeout(() => matrixCanvas.remove(), 2000);
        }, 5000);
    }
    
    if(eggCode === 'dox_me') {
        document.body.style.animation = 'shake 0.5s infinite';
        setTimeout(() => {
            document.body.style.animation = '';
        }, 2000);
        
        if(!document.getElementById('shake-style')) {
            const style = document.createElement('style');
            style.id = 'shake-style';
            style.innerHTML = `
                @keyframes shake {
                    0% { transform: translate(1px, 1px) rotate(0deg); }
                    10% { transform: translate(-1px, -2px) rotate(-1deg); }
                    20% { transform: translate(-3px, 0px) rotate(1deg); }
                    30% { transform: translate(3px, 2px) rotate(0deg); }
                    40% { transform: translate(1px, -1px) rotate(1deg); }
                    50% { transform: translate(-1px, 2px) rotate(-1deg); }
                    60% { transform: translate(-3px, 1px) rotate(0deg); }
                    70% { transform: translate(3px, 1px) rotate(-1deg); }
                    80% { transform: translate(-1px, -1px) rotate(1deg); }
                    90% { transform: translate(1px, 2px) rotate(0deg); }
                    100% { transform: translate(1px, -2px) rotate(-1deg); }
                }
            `;
            document.head.appendChild(style);
        }
    }
}
"""

if 'EASTER EGGS' not in text:
    with open('static/script.js', 'a', encoding='utf-8') as f:
        f.write('\n' + easter_egg_js)
    print("Added Easter Eggs JS")

# Now we need to modify the update_frontend_stream.py script's logic to catch "EASTEREGG:"
with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_stream_handler = """        const textChunk = data.choices[0]?.delta?.content || '';
        if(textChunk) {
            fullResponse += textChunk;
            msgEl.innerHTML = DOMPurify.sanitize(marked.parse(fullResponse));
            aiChatHistoryContainer.scrollTop = aiChatHistoryContainer.scrollHeight;
        }"""

new_stream_handler = """        const textChunk = data.choices[0]?.delta?.content || '';
        if(textChunk) {
            if(textChunk.startsWith('EASTEREGG:')) {
                const eggCode = textChunk.split(':')[1];
                msgEl.innerHTML = '<span style="color:var(--neon-primary)">[ СИСТЕМНАЯ АНОМАЛИЯ ОБНАРУЖЕНА ]</span>';
                handleEasterEgg(eggCode);
                continue;
            }
            fullResponse += textChunk;
            msgEl.innerHTML = DOMPurify.sanitize(marked.parse(fullResponse));
            aiChatHistoryContainer.scrollTop = aiChatHistoryContainer.scrollHeight;
        }"""

if old_stream_handler in text:
    text = text.replace(old_stream_handler, new_stream_handler)
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated stream handler for Easter Eggs")
else:
    print("Could not find stream handler to replace")
