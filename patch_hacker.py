import re

with open('static/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Remove the constant glitch animation from .hacked-theme
css = css.replace('animation: screen-glitch 0.2s linear infinite;', '/* animation removed */')

# 2. Add falling code animation
falling_css = """
@keyframes falling-code {
    0% { transform: translateY(-10vh); opacity: 1; }
    80% { opacity: 0.8; }
    100% { transform: translateY(110vh); opacity: 0; }
}
.falling-code-line {
    position: fixed;
    color: #ff0000;
    font-family: monospace;
    font-size: 14px;
    pointer-events: none;
    z-index: 0;
    text-shadow: 0 0 5px red;
    white-space: pre;
    writing-mode: vertical-rl;
    text-orientation: upright;
    animation: falling-code linear forwards;
}
"""

if '.falling-code-line' not in css:
    css += falling_css

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(css)


with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the enableHackerMode function
new_hacker_mode = """function enableHackerMode() {
    if (!window.currentUser || !window.currentUser.is_admin) {
        showToast('ACCESS DENIED', 'error');
        changeTheme('matrix');
        return;
    }
    document.body.classList.add('hacked-theme');
    
    // Start generating falling code and occasional errors
    hackerModeInterval = setInterval(() => {
        // Falling code line
        const codeLine = document.createElement('div');
        codeLine.className = 'falling-code-line';
        codeLine.style.left = Math.random() * window.innerWidth + 'px';
        codeLine.style.top = '-100px';
        
        let chars = '0123456789ABCDEF!@#$%^&*()';
        let length = Math.floor(Math.random() * 20) + 10;
        let str = '';
        for(let i=0; i<length; i++) {
            str += chars.charAt(Math.floor(Math.random() * chars.length)) + '\\n';
        }
        codeLine.textContent = str;
        
        // Random duration between 2s and 6s
        let dur = 2 + Math.random() * 4;
        codeLine.style.animationDuration = dur + 's';
        
        // Z-index so it's in background
        codeLine.style.zIndex = '-1';
        
        document.body.appendChild(codeLine);
        setTimeout(() => { if (codeLine.parentNode) codeLine.remove(); }, dur * 1000);
        
        // Occasional red bug (10% chance)
        if (Math.random() < 0.1) {
            const bug = document.createElement('div');
            bug.className = 'fake-bug';
            bug.style.position = 'fixed';
            bug.style.top = Math.random() * window.innerHeight + 'px';
            bug.style.left = Math.random() * window.innerWidth + 'px';
            bug.style.color = 'red';
            bug.style.fontFamily = 'monospace';
            bug.style.fontSize = (Math.random() * 30 + 15) + 'px';
            bug.style.pointerEvents = 'none';
            bug.style.zIndex = '999999';
            bug.style.textShadow = '0 0 10px red';
            
            const msgs = ['[ERROR] SYSTEM CORRUPTED', 'NULL POINTER', 'FATAL EXCEPTION', 'STACK OVERFLOW', 'ACCESS VIOLATION'];
            bug.textContent = msgs[Math.floor(Math.random() * msgs.length)];
            
            document.body.appendChild(bug);
            setTimeout(() => { if (bug.parentNode) bug.remove(); }, 1500);
        }
    }, 100); // Generate a lot of code lines quickly
}"""

# regex replace enableHackerMode
js = re.sub(r'function enableHackerMode\(\) \{.*?(?=function disableHackerMode)', new_hacker_mode + '\n\n', js, flags=re.DOTALL)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
