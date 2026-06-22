import os

js_code = """
// --- DOX APOCALYPSE EASTER EGG ---
let typedKeys = '';
const doxCode = 'dox';
document.addEventListener('keydown', (e) => {
    typedKeys += e.key.toLowerCase();
    if (typedKeys.length > doxCode.length) {
        typedKeys = typedKeys.slice(-doxCode.length);
    }
    if (typedKeys === doxCode) {
        triggerApocalypse();
    }
});

function triggerApocalypse() {
    if(document.body.classList.contains('apocalypse-mode')) return;
    
    document.body.classList.add('apocalypse-mode');
    
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    
    // Play a low ominous drone or glitch sound using simple oscillator
    function playGlitch() {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(50, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(10, audioCtx.currentTime + 1);
        gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 1);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 1);
    }
    playGlitch();
    
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
    
    setInterval(() => {
        const chunk = document.createElement('div');
        chunk.className = 'apocalypse-code-chunk';
        chunk.innerHTML = snippets[Math.floor(Math.random() * snippets.length)];
        chunk.style.left = (Math.random() * 80) + 'vw';
        chunk.style.top = '-100px';
        chunk.style.fontSize = (Math.random() * 10 + 14) + 'px';
        document.body.appendChild(chunk);
        
        setTimeout(() => chunk.remove(), 4000);
    }, 400);
    
    setTimeout(() => {
        alert("ВНИМАНИЕ: СИСТЕМА УНИЧТОЖЕНА ПОЛЬЗОВАТЕЛЕМ DOX. ВОССТАНОВЛЕНИЕ НЕВОЗМОЖНО.");
    }, 2000);
}
"""

with open('static/script.js', 'a', encoding='utf-8') as f:
    f.write(js_code)
print("Apocalypse JS appended.")
