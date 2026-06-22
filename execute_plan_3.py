import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_send = """async function sendMessengerMessage(forceMessage = null) {
    if(!activeChatId) return;
    
    const input = document.getElementById('messenger-input');
    const message = typeof forceMessage === 'string' ? forceMessage : input.value.trim();
    if(!message) return;
    
    input.value = '';
    
    // Optimistic UI could be added here, but simple fetch is fine
    try {
        await fetch('/api/send_chat_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: activeChatId, message })
        });
        loadChatMessages();
    } catch(e) {
        console.error(e);
    }
}"""

new_send = """async function sendMessengerMessage(forceMessage = null) {
    if(!activeChatId) return;
    
    const input = document.getElementById('messenger-input');
    const message = typeof forceMessage === 'string' ? forceMessage : input.value.trim();
    if(!message) return;
    
    input.value = '';
    
    // Optimistic UI
    const msgsContainer = document.getElementById('messenger-messages');
    const msgDiv = document.createElement('div');
    msgDiv.className = 'msg-bubble msg-out';
    msgDiv.style.opacity = '0.7';
    if(message.startsWith('STICKER:')) {
        const url = message.split('STICKER:')[1];
        msgDiv.innerHTML = `<img src="${url}" class="msg-sticker" style="max-width: 150px; border-radius: 10px;">`;
    } else {
        msgDiv.textContent = message;
    }
    msgsContainer.appendChild(msgDiv);
    msgsContainer.scrollTop = msgsContainer.scrollHeight;
    
    try {
        await fetch('/api/send_chat_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: activeChatId, message })
        });
        msgDiv.style.opacity = '1';
        loadChatMessages();
    } catch(e) {
        console.error(e);
        msgDiv.style.color = 'red';
    }
}"""

if old_send in js:
    js = js.replace(old_send, new_send)
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Patched sendMessengerMessage!")
else:
    print("Could not find old_send in script.js")
