import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Easter egg for WpSt nuke
old_easter = """    let keySequence = '';
    const secretWord = 'flora';
    let easterEggActive = false;"""

new_easter = """    let keySequence = '';
    const secretWord = 'flora';
    const nukeWord = 'wpst';
    let easterEggActive = false;"""

if old_easter in js:
    js = js.replace(old_easter, new_easter)

old_check = """        if (keySequence === secretWord) {
            triggerEasterEgg();
        }"""

new_check = """        if (keySequence.includes(secretWord)) {
            triggerEasterEgg();
            keySequence = '';
        }
        if (keySequence.includes(nukeWord)) {
            triggerNuke();
            keySequence = '';
        }"""

if old_check in js:
    js = js.replace(old_check, new_check)

nuke_function = """
    function triggerNuke() {
        easterEggActive = true;
        
        // Nuke styles
        const style = document.createElement('style');
        style.innerHTML = `
            @keyframes nukeShake {
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
            .nuke-active {
                animation: nukeShake 0.1s infinite;
                filter: invert(1) hue-rotate(180deg) brightness(2) contrast(1.5) !important;
                background: red !important;
                color: black !important;
            }
            .nuke-flash {
                position: fixed;
                top:0; left:0; width:100vw; height:100vh;
                background: white;
                z-index: 999999;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.1s;
            }
            .nuke-mushroom {
                position: fixed;
                bottom: -20vh;
                left: 50%;
                transform: translateX(-50%);
                width: 100vw;
                height: 120vh;
                background: radial-gradient(circle, rgba(255,100,0,1) 0%, rgba(200,0,0,0.8) 40%, transparent 70%);
                z-index: 999998;
                opacity: 0;
                transition: opacity 1s, transform 3s;
                border-radius: 50% 50% 0 0;
                pointer-events: none;
            }
        `;
        document.head.appendChild(style);
        
        document.body.classList.add('nuke-active');
        
        const flash = document.createElement('div');
        flash.className = 'nuke-flash';
        document.body.appendChild(flash);
        
        const mushroom = document.createElement('div');
        mushroom.className = 'nuke-mushroom';
        document.body.appendChild(mushroom);
        
        // Sounds (simulated via Web Audio API)
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        function playSiren() {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.type = 'square';
            osc.frequency.setValueAtTime(400, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(800, audioCtx.currentTime + 1);
            osc.frequency.linearRampToValueAtTime(400, audioCtx.currentTime + 2);
            gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
            osc.start();
            osc.stop(audioCtx.currentTime + 2);
            return osc;
        }
        
        let sirenInterval = setInterval(playSiren, 2000);
        playSiren();
        
        setTimeout(() => {
            clearInterval(sirenInterval);
            
            // Explosion sound
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(100, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 3);
            gain.gain.setValueAtTime(1, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 3);
            osc.start();
            osc.stop(audioCtx.currentTime + 3);
            
            // Visual explosion
            flash.style.opacity = '1';
            mushroom.style.opacity = '1';
            mushroom.style.transform = 'translateX(-50%) scale(1.5)';
            
            setTimeout(() => {
                document.body.innerHTML = '<div style="background:black; color:red; height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; font-family:monospace; font-size: 2rem;"><h1>SITE DESTROYED.</h1><p>WpSt NUKE PROTOCOL EXECUTED.</p></div>';
            }, 500);
        }, 3000); // 3 seconds of siren before boom
    }
"""

if 'function triggerNuke' not in js:
    # insert before function triggerEasterEgg
    idx = js.find('function triggerEasterEgg() {')
    if idx != -1:
        js = js[:idx] + nuke_function + js[idx:]

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Added nuke easter egg!")
