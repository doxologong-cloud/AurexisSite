import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Fix Syntax Error
error_pattern = r'const sysErrors = \[\s*"(.*?)"\s*,\s*"(.*?)"\s*,\s*"(.*?)"\s*,\s*"(.*?)"\s*,\s*"(.*?)"\s*,\s*"(.*?)"\s*\];'
new_errors = """const sysErrors = [
        `SYSTEM OVERRIDE INITIATED\\nBYPASSING FIREWALL...`, 
        `FATAL EXCEPTION 0x0000005\\nDATA CORRUPTION IN SECTOR 7`, 
        `SECURITY BREACH DETECTED\\nUNAUTHORIZED ROOT ACCESS`,
        `CONNECTING TO UNKNOWN HOST...\\nDOWNLOADING PAYLOAD...`, 
        `WARNING: PROTOCOL OVERRIDE\\nMEMORY LEAK DETECTED`,
        `ACCESS GRANTED: ROOT\\nDELETING LOGS...`
    ];"""

js = re.sub(error_pattern, new_errors, js, flags=re.DOTALL)

# Wait, the error pattern might fail if Python already wrote literal newlines.
# Let's just replace the exact block.

block_to_replace = """    const sysErrors = [
        "SYSTEM OVERRIDE INITIATED
BYPASSING FIREWALL...", 
        "FATAL EXCEPTION 0x0000005
DATA CORRUPTION IN SECTOR 7", 
        "SECURITY BREACH DETECTED
UNAUTHORIZED ROOT ACCESS",
        "CONNECTING TO UNKNOWN HOST...
DOWNLOADING PAYLOAD...", 
        "WARNING: PROTOCOL OVERRIDE
MEMORY LEAK DETECTED",
        "ACCESS GRANTED: ROOT
DELETING LOGS..."
    ];"""

js = js.replace(block_to_replace, new_errors)

# 2. Fix Preloader
preloader_old = """    // Preloader Logic
    const welcomeScreen = document.getElementById('welcome-screen');
    
    // Simulate loading time (e.g. 2.5 seconds)
    setTimeout(() => {
        welcomeScreen.style.opacity = '0';
        setTimeout(() => {
            welcomeScreen.style.visibility = 'hidden';
            // Show main elements after preloader finishes
            document.querySelector('.hero').classList.add('show');
            document.querySelectorAll('.feature-card').forEach(card => card.classList.add('show'));
        }, 500);
    }, 2500);"""

preloader_new = """    // Preloader Logic
    const welcomeScreen = document.getElementById('welcome-screen');
    
    if (sessionStorage.getItem('aurex_welcomed')) {
        // Skip preloader on reload
        welcomeScreen.style.display = 'none';
        document.querySelector('.hero') && document.querySelector('.hero').classList.add('show');
        document.querySelectorAll('.feature-card').forEach(card => card.classList.add('show'));
    } else {
        // Simulate loading time (e.g. 2.5 seconds)
        setTimeout(() => {
            welcomeScreen.style.opacity = '0';
            setTimeout(() => {
                welcomeScreen.style.display = 'none';
                sessionStorage.setItem('aurex_welcomed', 'true');
                // Show main elements after preloader finishes
                document.querySelector('.hero') && document.querySelector('.hero').classList.add('show');
                document.querySelectorAll('.feature-card').forEach(card => card.classList.add('show'));
            }, 500);
        }, 2000);
    }"""

js = js.replace(preloader_old, preloader_new)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
