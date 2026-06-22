import re

# 1. Update Cursor in HTML files
cursor_old = r'const hackerCursor = `data:image/svg\+xml;utf8,<svg.*?`;'
cursor_new = r'const hackerCursor = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><filter id="glow"><feDropShadow dx="0" dy="0" stdDeviation="2" flood-color="%23ff0000" flood-opacity="1"/></filter></defs><path d="M 4 4 L 12 28 L 16 16 L 28 12 Z" fill="%23ff0000" filter="url(%23glow)"/></svg>`;'

for path in ['templates/index.html', 'templates/admin.html']:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = re.sub(cursor_old, cursor_new, html)
        # Update cache buster
        html = re.sub(r'\?v=\d+', '?v=82', html)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    except FileNotFoundError:
        pass

# 2. Update CSS
css_additions = """
/* Hacker 3D Grid */
.hacker-3d-grid-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    perspective: 600px;
    z-index: -6;
    pointer-events: none;
    background: radial-gradient(circle at center 30%, #1a0000 0%, #000 70%);
    overflow: hidden;
}

.hacker-3d-grid {
    position: absolute;
    width: 200%;
    height: 150%;
    bottom: -30%;
    left: -50%;
    background-image: 
        linear-gradient(rgba(255, 0, 0, 0.4) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 0, 0, 0.4) 1px, transparent 1px);
    background-size: 50px 50px;
    transform: rotateX(75deg);
    transform-origin: top center;
    animation: grid-move 2s linear infinite;
    mask-image: linear-gradient(to bottom, transparent 0%, black 40%);
    -webkit-mask-image: linear-gradient(to bottom, transparent 0%, black 40%);
}

@keyframes grid-move {
    0% { transform: rotateX(75deg) translateY(0); }
    100% { transform: rotateX(75deg) translateY(50px); }
}

.hacker-error-window {
    position: fixed;
    background: rgba(10, 0, 0, 0.95);
    border: 1px solid #ff0000;
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.4);
    color: #ff0000;
    font-family: 'Courier New', Courier, monospace;
    z-index: 999999;
    pointer-events: none;
    animation: hacker-glitch 0.2s 3;
    min-width: 300px;
}
.hacker-error-header {
    background: #ff0000;
    color: #000;
    font-weight: bold;
    padding: 4px 10px;
    font-size: 14px;
    display: flex;
    justify-content: space-between;
}
.hacker-error-body {
    padding: 15px;
    font-size: 16px;
    white-space: pre-wrap;
    text-shadow: 0 0 5px red;
}

@keyframes hacker-glitch {
    0% { transform: translate(0) }
    20% { transform: translate(-2px, 2px) }
    40% { transform: translate(-2px, -2px) }
    60% { transform: translate(2px, 2px) }
    80% { transform: translate(2px, -2px) }
    100% { transform: translate(0) }
}
"""
with open('static/style.css', 'r', encoding='utf-8') as f:
    css = f.read()
if '.hacker-3d-grid' not in css:
    css += css_additions
    with open('static/style.css', 'w', encoding='utf-8') as f:
        f.write(css)

# 3. Update JS
with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update Cursor in JS
js = re.sub(cursor_old, cursor_new, js)

# Replace enableHackerMode
hacker_js_old_pattern = r'function enableHackerMode\(\) \{.*?(?=function toggleAnimations)'

hacker_js_new = """function enableHackerMode() {
    if (window.currentUser === undefined) {
        document.body.classList.add('hacked-theme');
        return; // wait for checkSession
    }
    if (!window.currentUser || !window.currentUser.is_admin) {
        showToast('ACCESS DENIED', 'error');
        changeTheme('matrix');
        return;
    }
    document.body.classList.add('hacked-theme');
    
    // Create 3D Grid Background
    let gridContainer = document.getElementById('hacker-grid-overlay');
    if (!gridContainer) {
        gridContainer = document.createElement('div');
        gridContainer.id = 'hacker-grid-overlay';
        gridContainer.className = 'hacker-3d-grid-container';
        
        let grid = document.createElement('div');
        grid.className = 'hacker-3d-grid';
        gridContainer.appendChild(grid);
        document.body.appendChild(gridContainer);
        
        // Add CRT scanlines
        let crt = document.createElement('div');
        crt.id = 'hacker-crt-overlay';
        crt.style.position = 'fixed';
        crt.style.top = '0';
        crt.style.left = '0';
        crt.style.width = '100vw';
        crt.style.height = '100vh';
        crt.style.background = 'linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.4) 50%)';
        crt.style.backgroundSize = '100% 4px';
        crt.style.pointerEvents = 'none';
        crt.style.zIndex = '999998';
        crt.style.opacity = '0.6';
        document.body.appendChild(crt);
    }
    
    const sysErrors = [
        "SYSTEM OVERRIDE INITIATED\\nBYPASSING FIREWALL...", 
        "FATAL EXCEPTION 0x0000005\\nDATA CORRUPTION IN SECTOR 7", 
        "SECURITY BREACH DETECTED\\nUNAUTHORIZED ROOT ACCESS",
        "CONNECTING TO UNKNOWN HOST...\\nDOWNLOADING PAYLOAD...", 
        "WARNING: PROTOCOL OVERRIDE\\nMEMORY LEAK DETECTED",
        "ACCESS GRANTED: ROOT\\nDELETING LOGS..."
    ];
    
    // Generate occasional system error windows
    hackerModeInterval = setInterval(() => {
        if (Math.random() < 0.3) {
            const win = document.createElement('div');
            win.className = 'hacker-error-window';
            
            // Random position but keep it generally visible
            const top = Math.max(10, Math.random() * (window.innerHeight - 200));
            const left = Math.max(10, Math.random() * (window.innerWidth - 400));
            
            win.style.top = top + 'px';
            win.style.left = left + 'px';
            
            const header = document.createElement('div');
            header.className = 'hacker-error-header';
            header.innerHTML = '<span>SYSTEM ALERT</span><span>X</span>';
            
            const body = document.createElement('div');
            body.className = 'hacker-error-body';
            body.textContent = sysErrors[Math.floor(Math.random() * sysErrors.length)];
            
            win.appendChild(header);
            win.appendChild(body);
            document.body.appendChild(win);
            
            // Remove after 2-4 seconds
            setTimeout(() => { if (win.parentNode) win.remove(); }, 2000 + Math.random() * 2000);
        }
    }, 2000); // Check every 2 seconds
}

function disableHackerMode() {
    document.body.classList.remove('hacked-theme');
    if (hackerModeInterval) clearInterval(hackerModeInterval);
    document.querySelectorAll('.hacker-error-window').forEach(e => e.remove());
    const grid = document.getElementById('hacker-grid-overlay');
    if (grid) grid.remove();
    const crt = document.getElementById('hacker-crt-overlay');
    if (crt) crt.remove();
    const oldBg = document.getElementById('hacker-bg-overlay');
    if (oldBg) oldBg.remove();
}
"""

js = re.sub(hacker_js_old_pattern, hacker_js_new, js, flags=re.DOTALL)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
