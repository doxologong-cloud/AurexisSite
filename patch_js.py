import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add hacker mode globals
hacker_globals = """
// ==========================================
// HACKER MODE LOGIC
// ==========================================
let hackerModeInterval = null;

function enableHackerMode() {
    if (!window.currentUser || !window.currentUser.is_admin) {
        showToast('ACCESS DENIED', 'error');
        changeTheme('matrix');
        return;
    }
    document.body.classList.add('hacked-theme');
    
    // Start generating fake bugs
    hackerModeInterval = setInterval(() => {
        const bug = document.createElement('div');
        bug.className = 'fake-bug';
        bug.style.position = 'fixed';
        bug.style.top = Math.random() * window.innerHeight + 'px';
        bug.style.left = Math.random() * window.innerWidth + 'px';
        bug.style.color = 'red';
        bug.style.fontFamily = 'monospace';
        bug.style.fontSize = (Math.random() * 20 + 10) + 'px';
        bug.style.pointerEvents = 'none';
        bug.style.zIndex = '999999';
        bug.style.textShadow = '0 0 10px red';
        bug.style.opacity = '0.8';
        
        const msgs = ['[ERROR] MEMORY LEAK', 'SYSTEM CORRUPTED', 'NULL POINTER', 'FATAL EXCEPTION', 'STACK OVERFLOW'];
        bug.textContent = msgs[Math.floor(Math.random() * msgs.length)];
        
        document.body.appendChild(bug);
        
        setTimeout(() => {
            if (bug.parentNode) bug.parentNode.removeChild(bug);
        }, 2000 + Math.random() * 3000);
    }, 1000);
}

function disableHackerMode() {
    document.body.classList.remove('hacked-theme');
    if (hackerModeInterval) clearInterval(hackerModeInterval);
    document.querySelectorAll('.fake-bug').forEach(e => e.remove());
}

function toggleAnimations(enabled) {
    if (!enabled) {
        document.body.classList.add('no-animations');
    } else {
        document.body.classList.remove('no-animations');
    }
    localStorage.setItem('aurexis_animations', enabled);
}

// Ensure settings toggles are synced on load
document.addEventListener('DOMContentLoaded', () => {
    const animEnabled = localStorage.getItem('aurexis_animations') !== 'false';
    const animToggle = document.getElementById('anim-toggle');
    if (animToggle) animToggle.checked = animEnabled;
    toggleAnimations(animEnabled);
});

function changeTheme(themeName) {"""

js = js.replace("function changeTheme(themeName) {", hacker_globals)

# 2. Add new themes to changeTheme
new_themes = """    } else if (themeName === 'vampire') {
        root.style.setProperty('--neon-color', '#ff0000');
        root.style.setProperty('--bg-color', '#1a0000');
        root.style.setProperty('--glow-color', 'rgba(255, 0, 0, 0.5)');
        root.style.setProperty('--neon-primary', '#ff0000');
        color1 = 'ff4d4d'; color2 = 'cc0000'; ptrColor1 = 'ffffff'; ptrColor2 = 'ff4d4d';
    } else if (themeName === 'ocean') {
        root.style.setProperty('--neon-color', '#00ffff');
        root.style.setProperty('--bg-color', '#000a1a');
        root.style.setProperty('--glow-color', 'rgba(0, 255, 255, 0.5)');
        root.style.setProperty('--neon-primary', '#0088ff');
        color1 = '66ffff'; color2 = '0088ff'; ptrColor1 = 'ffffff'; ptrColor2 = '66ffff';
    } else if (themeName === 'hacked') {
        root.style.setProperty('--neon-color', '#ff0000');
        root.style.setProperty('--bg-color', '#000000');
        root.style.setProperty('--glow-color', 'rgba(255, 0, 0, 0.8)');
        root.style.setProperty('--neon-primary', '#ff0000');
        color1 = 'ff0000'; color2 = '8b0000'; ptrColor1 = 'ff0000'; ptrColor2 = 'ff0000';
    }
"""

js = js.replace("color1 = '66ffeb'; color2 = '00ffcc'; ptrColor1 = 'ffffff'; ptrColor2 = '66ffeb';\n    }", "color1 = '66ffeb'; color2 = '00ffcc'; ptrColor1 = 'ffffff'; ptrColor2 = '66ffeb';\n" + new_themes)

# 3. Handle hacker mode toggle inside changeTheme
change_theme_end = """
    // Update active card
    document.querySelectorAll('.theme-card').forEach(c => c.classList.remove('active'));
    const activeCard = document.getElementById('card-' + themeName);
    if(activeCard) activeCard.classList.add('active');
    
    if (themeName === 'hacked') {
        enableHackerMode();
    } else {
        disableHackerMode();
    }
}"""

js = re.sub(r"// Update active card.*?if\(activeCard\) activeCard\.classList\.add\('active'\);\n}", change_theme_end, js, flags=re.DOTALL)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
