import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

ux_js = """
// ==========================================
// UX & SOUND EFFECTS (WEB AUDIO API)
// ==========================================

const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playSound(type) {
    if (audioCtx.state === 'suspended') audioCtx.resume();
    
    const osc = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    
    osc.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    
    if (type === 'send') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(600, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.1);
        gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.1);
    } else if (type === 'receive') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(800, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(400, audioCtx.currentTime + 0.15);
        gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.15);
    }
}

// ==========================================
// CUSTOM CONTEXT MENU & REACTIONS
// ==========================================

document.addEventListener('contextmenu', function(e) {
    const msg = e.target.closest('.message');
    if (msg) {
        e.preventDefault();
        showContextMenu(e.pageX, e.pageY, msg);
    } else {
        hideContextMenu();
    }
});

document.addEventListener('click', hideContextMenu);

function showContextMenu(x, y, msgElem) {
    hideContextMenu();
    const menu = document.createElement('div');
    menu.id = 'custom-context-menu';
    menu.style.position = 'absolute';
    menu.style.left = x + 'px';
    menu.style.top = y + 'px';
    menu.style.background = 'rgba(10, 10, 10, 0.95)';
    menu.style.border = '1px solid var(--neon-color)';
    menu.style.borderRadius = '5px';
    menu.style.padding = '5px 0';
    menu.style.zIndex = '1000';
    menu.style.boxShadow = '0 0 15px var(--glow-color)';
    
    const isMine = msgElem.classList.contains('my-message');
    
    menu.innerHTML = `
        <div class="menu-item" onclick="replyToMessage('${msgElem.innerText}')">↩️ Ответить</div>
        ${isMine ? `<div class="menu-item" style="color: #ff4757;" onclick="deleteMessage(this)">🗑️ Удалить</div>` : ''}
        <div class="menu-item" onclick="addReaction(this, '❤️')">❤️ Сердечко</div>
        <div class="menu-item" onclick="addReaction(this, '🔥')">🔥 Огонь</div>
    `;
    
    document.body.appendChild(menu);
}

function hideContextMenu() {
    const menu = document.getElementById('custom-context-menu');
    if (menu) menu.remove();
}

function replyToMessage(text) {
    const input = document.getElementById('message-input');
    if (input) {
        input.value = `> ${text.substring(0, 20)}...\n\n`;
        input.focus();
    }
}

function deleteMessage(btn) {
    // Optimistic delete for now
    alert("Сообщение визуально удалено! (БД интеграция в след. фазе)");
}

function addReaction(btn, emoji) {
    alert("Добавлена реакция " + emoji + " ! (БД интеграция в след. фазе)");
}

// Hook into existing sendMessage to play sound
const originalSendMessage = window.sendMessage;
if (typeof originalSendMessage === 'function') {
    window.sendMessage = async function() {
        playSound('send');
        await originalSendMessage();
    };
}
"""

if 'WEB AUDIO API' not in js_text:
    js_text += "\n" + ux_js
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(js_text)
    print("Injected UX JS.")
else:
    print("UX JS already exists.")
