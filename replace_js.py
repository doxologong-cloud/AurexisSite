import os

new_js = """
    // --- AI TERMINAL LOGIC ---
    const aiInput = document.getElementById('ai-input');
    const aiSendBtn = document.getElementById('ai-send-btn');
    const aiChatBox = document.getElementById('ai-chat-box');

    function escapeHTML(str) {
        return str.replace(/[&<>"'`]/g, function(m) {
            return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;", "`": "&#x60;" }[m];
        });
    }

    function addMessageToTerminal(role, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `ai-msg ${role === 'user' ? 'user-msg' : 'flora-msg'}`;
        
        let avatarSrc = '/static/assets/logo.png';
        let nameHTML = '<span class="flora-name">AUREXIS FLORA</span>';
        
        if (role === 'user') {
            avatarSrc = window.currentUser ? window.currentUser.avatar : '/static/assets/default-avatar.png';
            const name = window.currentUser ? window.currentUser.nickname : 'Гость';
            nameHTML = `<span class="user-name">${escapeHTML(name)}</span>`;
        }

        msgDiv.innerHTML = `
            <img src="${avatarSrc}" class="${role === 'user' ? 'user-avatar' : 'ai-avatar'}">
            <div class="ai-text">
                ${nameHTML}
                <div class="msg-content">${role === 'user' ? escapeHTML(text) : text}</div>
            </div>
        `;
        
        aiChatBox.appendChild(msgDiv);
        aiChatBox.scrollTop = aiChatBox.scrollHeight;
        return msgDiv.querySelector('.msg-content');
    }

    async function sendToAI() {
        if(!aiInput || !aiInput.value.trim()) return;
        const text = aiInput.value.trim();
        aiInput.value = '';
        
        // Add user msg
        addMessageToTerminal('user', text);
        
        // Add typing indicator
        const contentBox = addMessageToTerminal('ai', '<div class="typing-indicator"></div><div class="typing-indicator" style="animation-delay:0.2s"></div><div class="typing-indicator" style="animation-delay:0.4s"></div>');
        
        try {
            const res = await fetch('/api/ai/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            
            const data = await res.json();
            if (res.ok) {
                // Smooth typewriter effect
                contentBox.innerHTML = '';
                const reply = data.reply;
                let i = 0;
                const interval = setInterval(() => {
                    contentBox.innerHTML += reply.charAt(i);
                    i++;
                    aiChatBox.scrollTop = aiChatBox.scrollHeight;
                    if (i >= reply.length) {
                        clearInterval(interval);
                        // Optional formatting of bold text
                        contentBox.innerHTML = contentBox.innerHTML.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
                        contentBox.innerHTML = contentBox.innerHTML.replace(/\\n/g, '<br>');
                    }
                }, 15);
            } else {
                contentBox.innerHTML = `<span style="color:#ff4444">Ошибка связи с ИИ: ${data.error || 'Неизвестная ошибка'}</span>`;
            }
        } catch(e) {
            contentBox.innerHTML = '<span style="color:#ff4444">Ошибка сети при связи с ИИ-ядром.</span>';
        }
    }

    if (aiSendBtn) {
        aiSendBtn.addEventListener('click', sendToAI);
    }
    if (aiInput) {
        aiInput.addEventListener('keypress', (e) => {
            if(e.key === 'Enter') sendToAI();
        });
    }

});
"""

filepath = 'static/script.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('// --- BOT BUILDER LOGIC ---')
if idx != -1:
    content = content[:idx] + new_js
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Replaced bot builder logic with AI terminal logic.')
else:
    print('Logic not found.')
