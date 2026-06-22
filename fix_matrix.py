import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

matrix_js = """
        printHacker("Initializing matrix protocol...");
        document.body.innerHTML += '<canvas id="matrix-canvas" style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:9999;pointer-events:none;"></canvas>';
        const c = document.getElementById('matrix-canvas');
        const ctx = c.getContext('2d');
        c.width = window.innerWidth;
        c.height = window.innerHeight;
        const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*'.split('');
        const fontSize = 16;
        const columns = c.width / fontSize;
        const drops = [];
        for(let x = 0; x < columns; x++) drops[x] = 1;
        function drawMatrix() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, c.width, c.height);
            ctx.fillStyle = '#0f0';
            ctx.font = fontSize + 'px monospace';
            for(let i = 0; i < drops.length; i++) {
                const text = letters[Math.floor(Math.random() * letters.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if(drops[i] * fontSize > c.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        window.matrixInterval = setInterval(drawMatrix, 33);
        setTimeout(() => {
            clearInterval(window.matrixInterval);
            c.remove();
            printHacker("Matrix protocol terminated.");
        }, 10000);
"""

# Replace the old matrix logic
old_matrix = """printHacker("Initializing matrix protocol...");
        switchView('view-home');
        document.body.style.animation = 'glitch 0.2s infinite';
        setTimeout(() => document.body.style.animation = 'none', 2000);"""

if old_matrix in js_text:
    js_text = js_text.replace(old_matrix, matrix_js)
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(js_text)
    print('Fixed matrix command')
else:
    print('Old matrix logic not found')
