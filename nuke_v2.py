import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

idx_start = js.find('function triggerNuke() {')
idx_end = js.find('function triggerEasterEgg() {')

if idx_start != -1 and idx_end != -1:
    old_nuke = js[idx_start:idx_end]
    
    new_nuke = """function triggerNuke() {
        easterEggActive = true;
        
        const style = document.createElement('style');
        style.innerHTML = `
            @keyframes nukeShake {
                0% { transform: translate(2px, 2px) rotate(0deg); }
                10% { transform: translate(-2px, -4px) rotate(-1deg); }
                20% { transform: translate(-6px, 0px) rotate(1deg); }
                30% { transform: translate(6px, 4px) rotate(0deg); }
                40% { transform: translate(2px, -2px) rotate(1deg); }
                50% { transform: translate(-2px, 4px) rotate(-1deg); }
                60% { transform: translate(-6px, 2px) rotate(0deg); }
                70% { transform: translate(6px, 2px) rotate(-1deg); }
                80% { transform: translate(-2px, -2px) rotate(1deg); }
                90% { transform: translate(2px, 4px) rotate(0deg); }
                100% { transform: translate(2px, -4px) rotate(-1deg); }
            }
            @keyframes missileDrop {
                0% { transform: translate(-50%, -100vh) rotate(180deg) scale(0.5); }
                100% { transform: translate(-50%, 50vh) rotate(180deg) scale(3); }
            }
            .nuke-missile {
                position: fixed;
                top: 0; left: 50%;
                font-size: 5rem;
                z-index: 999999;
                animation: missileDrop 2.5s cubic-bezier(0.5, 0, 1, 1) forwards;
                pointer-events: none;
            }
            .nuke-active {
                animation: nukeShake 0.1s infinite;
                filter: invert(1) hue-rotate(180deg) brightness(2) contrast(1.5) !important;
                background: red !important;
                color: black !important;
            }
            .fly-apart {
                transition: transform 1.5s cubic-bezier(0.1, 0.8, 0.2, 1), opacity 1s;
                opacity: 0;
            }
            .nuke-flash {
                position: fixed; top:0; left:0; width:100vw; height:100vh;
                background: white; z-index: 999999; pointer-events: none; opacity: 0; transition: opacity 0.1s;
            }
            .nuke-mushroom {
                position: fixed; bottom: -20vh; left: 50%; transform: translateX(-50%); width: 100vw; height: 120vh;
                background: radial-gradient(circle, rgba(255,100,0,1) 0%, rgba(200,0,0,0.8) 40%, rgba(50,0,0,0.9) 70%, transparent 80%);
                z-index: 999998; opacity: 0; transition: opacity 0.5s, transform 4s cubic-bezier(0.1, 0.8, 0.2, 1);
                border-radius: 50% 50% 0 0; pointer-events: none;
            }
        `;
        document.head.appendChild(style);
        
        document.body.classList.add('nuke-active');
        
        const missile = document.createElement('div');
        missile.className = 'nuke-missile';
        missile.innerHTML = '🚀';
        document.body.appendChild(missile);
        
        const flash = document.createElement('div');
        flash.className = 'nuke-flash';
        document.body.appendChild(flash);
        
        const mushroom = document.createElement('div');
        mushroom.className = 'nuke-mushroom';
        document.body.appendChild(mushroom);
        
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        // Loud Siren
        function playSiren() {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.type = 'square';
            osc.frequency.setValueAtTime(400, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(800, audioCtx.currentTime + 1);
            osc.frequency.linearRampToValueAtTime(400, audioCtx.currentTime + 2);
            gain.gain.setValueAtTime(0.3, audioCtx.currentTime); // LOUD
            osc.start();
            osc.stop(audioCtx.currentTime + 2);
        }
        
        let sirenInterval = setInterval(playSiren, 2000);
        playSiren();
        
        setTimeout(() => {
            clearInterval(sirenInterval);
            
            // VERY LOUD BOOM (Noise + Sub Bass)
            const bufferSize = audioCtx.sampleRate * 3; 
            const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) {
                data[i] = Math.random() * 2 - 1;
            }
            
            const noise = audioCtx.createBufferSource();
            noise.buffer = buffer;
            const noiseFilter = audioCtx.createBiquadFilter();
            noiseFilter.type = 'lowpass';
            noiseFilter.frequency.setValueAtTime(1000, audioCtx.currentTime);
            noiseFilter.frequency.exponentialRampToValueAtTime(10, audioCtx.currentTime + 3);
            
            const noiseGain = audioCtx.createGain();
            noiseGain.gain.setValueAtTime(5, audioCtx.currentTime); // CRANK IT
            noiseGain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 3);
            
            noise.connect(noiseFilter);
            noiseFilter.connect(noiseGain);
            noiseGain.connect(audioCtx.destination);
            noise.start();
            
            const subOsc = audioCtx.createOscillator();
            const subGain = audioCtx.createGain();
            subOsc.connect(subGain);
            subGain.connect(audioCtx.destination);
            subOsc.type = 'sine';
            subOsc.frequency.setValueAtTime(100, audioCtx.currentTime);
            subOsc.frequency.exponentialRampToValueAtTime(10, audioCtx.currentTime + 3);
            subGain.gain.setValueAtTime(10, audioCtx.currentTime); // CRANK IT MORE
            subGain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 3);
            subOsc.start();
            subOsc.stop(audioCtx.currentTime + 3);

            // Visual explosion
            flash.style.opacity = '1';
            mushroom.style.opacity = '1';
            mushroom.style.transform = 'translateX(-50%) scale(2) translateY(-20%)';
            missile.style.display = 'none';
            
            // Fly apart
            document.querySelectorAll('section, nav, footer, .hero-content, .bot-list, .chat-item').forEach(el => {
                el.classList.add('fly-apart');
                const rx = (Math.random() - 0.5) * 4000;
                const ry = (Math.random() - 0.5) * 4000;
                const rz = (Math.random() - 0.5) * 1440;
                el.style.transform = `translate3d(${rx}px, ${ry}px, 500px) rotateZ(${rz}deg)`;
            });
            
            setTimeout(() => {
                document.body.innerHTML = '<div style="background:black; color:red; height:100vh; width:100vw; display:flex; flex-direction:column; align-items:center; justify-content:center; font-family:monospace; font-size: 3rem; text-align:center; z-index:9999999; position:fixed; top:0; left:0;"><h1>SITE OBLITERATED.</h1><p>WpSt MAXIMUM YIELD NUKE DETONATED.</p></div>';
            }, 1000);
        }, 2500);
    }
"""

    js = js.replace(old_nuke, new_nuke)
    
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Replaced triggerNuke!")
else:
    print("Could not find triggerNuke boundaries.")
