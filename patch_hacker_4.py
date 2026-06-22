import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace enableHackerMode and disableHackerMode completely
hacker_old_pattern = r'function enableHackerMode\(\) \{.*?(?=function toggleAnimations)'

new_hacker_mode = """function enableHackerMode() {
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
    
    // Create the scary background overlay
    let hackerBg = document.getElementById('hacker-bg-overlay');
    if (!hackerBg) {
        hackerBg = document.createElement('div');
        hackerBg.id = 'hacker-bg-overlay';
        hackerBg.style.position = 'fixed';
        hackerBg.style.top = '0';
        hackerBg.style.left = '0';
        hackerBg.style.width = '100vw';
        hackerBg.style.height = '100vh';
        hackerBg.style.background = 'radial-gradient(ellipse at center, #1a0505 0%, #000000 100%)';
        hackerBg.style.fontFamily = 'monospace';
        hackerBg.style.fontSize = '13px';
        hackerBg.style.lineHeight = '1.3';
        hackerBg.style.overflow = 'hidden';
        hackerBg.style.zIndex = '-5';
        hackerBg.style.pointerEvents = 'none';
        hackerBg.style.opacity = '0.45';
        hackerBg.style.wordBreak = 'break-all';
        hackerBg.style.whiteSpace = 'pre-wrap';
        document.body.appendChild(hackerBg);
        
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
        crt.style.zIndex = '999998'; // Just below bugs
        crt.style.opacity = '0.6';
        document.body.appendChild(crt);
    }
    
    const scaryPhrases = [
        "SYSTEM OVERRIDE INITIATED", "NULL_POINTER_EXCEPTION AT 0xDEADBEEF", "THEY ARE WATCHING",
        "DON'T LOOK BEHIND YOU", "I CAN SEE YOU", "DATA CORRUPTION DETECTED", "FATAL ERROR",
        "CONNECTING TO UNKNOWN HOST...", "DOWNLOADING SOUL...", "SECURITY BREACH", "ACCESS GRANTED: ROOT",
        "FORMATTING DRIVE C:", "RUN", "01010100 01010010 01010101 01010011 01010100", "DELETING PROTOCOLS"
    ];
    
    const colors = ['#ff3333', '#880000', '#555555', '#444444', '#ffffff', '#cc0000'];
    
    // Start generating ton of text
    hackerModeInterval = setInterval(() => {
        // Append a massive chunk of text
        let chunk = "";
        for (let i = 0; i < 5; i++) {
            let col = colors[Math.floor(Math.random() * colors.length)];
            let text = "";
            if (Math.random() > 0.8) {
                text = scaryPhrases[Math.floor(Math.random() * scaryPhrases.length)];
            } else {
                let hex = "";
                for(let j=0; j<8; j++) hex += Math.floor(Math.random()*16).toString(16).toUpperCase();
                text = "0x" + hex;
            }
            // Add a little glow if it's white or bright red
            let shadow = (col === '#ffffff' || col === '#ff3333') ? `text-shadow: 0 0 5px ${col};` : '';
            chunk += `<span style="color: ${col}; ${shadow}">${text} </span>`;
        }
        hackerBg.innerHTML += chunk + (Math.random() > 0.5 ? "<br>" : "");
        
        // Keep the text from becoming too huge in DOM to avoid lag
        if (hackerBg.innerHTML.length > 6000) {
            hackerBg.innerHTML = hackerBg.innerHTML.substring(1500);
        }
        
        // Occasional big red bug (5% chance)
        if (Math.random() < 0.05) {
            const bug = document.createElement('div');
            bug.className = 'fake-bug';
            bug.style.position = 'fixed';
            bug.style.top = Math.random() * window.innerHeight + 'px';
            bug.style.left = Math.random() * window.innerWidth + 'px';
            bug.style.color = '#ff0000';
            bug.style.fontFamily = 'monospace';
            bug.style.fontWeight = 'bold';
            bug.style.fontSize = (Math.random() * 40 + 20) + 'px';
            bug.style.pointerEvents = 'none';
            bug.style.zIndex = '999999';
            bug.style.textShadow = '0 0 20px red, 0 0 10px red';
            
            bug.textContent = scaryPhrases[Math.floor(Math.random() * scaryPhrases.length)];
            
            document.body.appendChild(bug);
            setTimeout(() => { if (bug.parentNode) bug.remove(); }, 800 + Math.random() * 1000);
        }
    }, 50); // Very fast interval to simulate pouring text
}

function disableHackerMode() {
    document.body.classList.remove('hacked-theme');
    if (hackerModeInterval) clearInterval(hackerModeInterval);
    document.querySelectorAll('.fake-bug').forEach(e => e.remove());
    document.querySelectorAll('.falling-code-line').forEach(e => e.remove());
    const bg = document.getElementById('hacker-bg-overlay');
    if (bg) bg.remove();
    const crt = document.getElementById('hacker-crt-overlay');
    if (crt) crt.remove();
}
"""

js = re.sub(hacker_old_pattern, new_hacker_mode, js, flags=re.DOTALL)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
