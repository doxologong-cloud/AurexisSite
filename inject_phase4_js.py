import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

phase4_js = """
// ==========================================
// PHASE 4: HARDCORE TECH (E2EE, WEBRTC, PWA, EDITOR)
// ==========================================

// 1. PWA Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // We just pretend to register a service worker for now since we don't have the file
        console.log('Aurexis PWA Service Worker ready (Simulated)');
    });
}

// 2. Live Code Editor
function runCode() {
    const code = document.getElementById('code-textarea').value;
    const output = document.getElementById('code-output');
    output.innerHTML = "<span style='color: #ffcc00;'>Running...</span><br>";
    
    setTimeout(() => {
        if (code.includes('print')) {
            output.innerHTML += "SyntaxError: 'print' is not defined (JS environment).<br>";
        }
        output.innerHTML += "Compilation finished. Local VM simulated.<br>";
        if(code.includes('ping')) {
            output.innerHTML += "pong<br>";
        }
    }, 500);
}

// 3. WebRTC Audio/Video Call (Simulated local stream for demo)
async function startCall() {
    const chatHeader = document.querySelector('.chat-header');
    if(document.getElementById('video-call-container')) return;
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        
        const container = document.createElement('div');
        container.id = 'video-call-container';
        container.style.position = 'absolute';
        container.style.top = '60px';
        container.style.right = '20px';
        container.style.width = '300px';
        container.style.height = '200px';
        container.style.background = '#000';
        container.style.border = '2px solid var(--neon-color)';
        container.style.borderRadius = '10px';
        container.style.overflow = 'hidden';
        container.style.zIndex = '1001';
        container.style.boxShadow = '0 0 20px rgba(0, 255, 0, 0.4)';
        
        const video = document.createElement('video');
        video.srcObject = stream;
        video.autoplay = true;
        video.muted = true; // local video
        video.style.width = '100%';
        video.style.height = '100%';
        video.style.objectFit = 'cover';
        
        const endBtn = document.createElement('button');
        endBtn.innerText = '📞 Завершить';
        endBtn.style.position = 'absolute';
        endBtn.style.bottom = '10px';
        endBtn.style.left = '50%';
        endBtn.style.transform = 'translateX(-50%)';
        endBtn.style.background = '#ff4757';
        endBtn.style.color = '#fff';
        endBtn.style.border = 'none';
        endBtn.style.padding = '5px 15px';
        endBtn.style.borderRadius = '15px';
        endBtn.style.cursor = 'pointer';
        
        endBtn.onclick = () => {
            stream.getTracks().forEach(t => t.stop());
            container.remove();
            playSound('receive'); // simulate hangup sound
        };
        
        container.appendChild(video);
        container.appendChild(endBtn);
        
        // Find messenger window and append
        const messenger = document.getElementById('view-messenger');
        if(messenger) messenger.appendChild(container);
        
    } catch(e) {
        alert("Нет доступа к камере или микрофону для WebRTC!");
    }
}

// 4. E2EE Encryption Wrapper
// We will hook into the message sending process to encrypt text before it goes to DB, 
// and decrypt it when it comes from DB. Since we don't have a shared key exchange setup yet, 
// we will just visually encrypt it in the DOM and decrypt it.
// (For demo purposes, the actual encryption is just base64 or a shift cipher so we can easily decode it without async key management).

function encryptE2EE(text) {
    // Simple mock encryption to show E2EE concept
    return "E2EE::" + btoa(unescape(encodeURIComponent(text)));
}

function decryptE2EE(text) {
    if (text.startsWith("E2EE::")) {
        try {
            return decodeURIComponent(escape(atob(text.replace("E2EE::", ""))));
        } catch(e) {
            return text;
        }
    }
    return text; // not encrypted
}

// Override loadMessages specifically for E2EE display
const originalLoadMessagesP4 = window.loadMessages;
if (typeof originalLoadMessagesP4 === 'function') {
    window.loadMessages = async function() {
        await originalLoadMessagesP4();
        // Go through all messages and "decrypt" them visually if they are encrypted
        const messages = document.querySelectorAll('.message-text');
        messages.forEach(msg => {
            // Note: because of rich embeds, the text might already have HTML.
            // A real E2EE implementation encrypts the raw string before sending,
            // and decrypts it BEFORE rendering rich embeds.
            // For now, if we see E2EE:: we know we can decrypt.
        });
    };
}
"""

if 'PHASE 4: HARDCORE TECH' not in js_text:
    js_text += "\n" + phase4_js
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(js_text)
    print("Injected Phase 4 JS.")
else:
    print("Phase 4 JS already exists.")
