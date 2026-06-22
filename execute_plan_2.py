import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update Polling Interval
js = js.replace('messagePollingInterval = setInterval(loadChatMessages, 3000);', 'messagePollingInterval = setInterval(loadChatMessages, 2000);')
js = js.replace('messagePollingInterval = setInterval(loadChatMessages, 5000);', 'messagePollingInterval = setInterval(loadChatMessages, 2000);')

# 2. Fix sendMessage for optimistic UI
old_send_msg = """    chatSendBtn.addEventListener('click', async () => {
        if(!window.currentUser) {
            showToast('  <a onclick=\"switchAuthTab(\\'login\\')\">ਧ</a>   <a onclick=\"switchAuthTab(\\'register\\')\">ॣ஢</a>. ,   , ⮡   !', 'error');
            return;
        }
        const text = chatInput.value.trim();
        if(!text) return;
        chatInput.value = '';
        
        try {
            let url = currentChatTab === 'global' ? '/api/global-chat' : `/api/chats/${activeChatId}/messages`;
            const res = await fetch(url, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text})
            });
            if(res.ok) {
                if(currentChatTab === 'global') loadGlobalChat();
                else loadChatMessages();
            }
        } catch(e) {
            console.error(e);
        }
    });"""

new_send_msg = """    chatSendBtn.addEventListener('click', async () => {
        if(!window.currentUser) {
            showToast('Нет доступа, вы не зарегистрированы!', 'error');
            return;
        }
        const text = chatInput.value.trim();
        if(!text) return;
        chatInput.value = '';
        
        // Optimistic UI update
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message right';
        msgDiv.innerHTML = `
            <div class="message-content" style="opacity: 0.7;">
                ${text.replace(/</g, "&lt;").replace(/>/g, "&gt;")}
                <div class="message-time">Sending...</div>
            </div>
            <img src="${window.currentUser.avatar || '/static/assets/default-avatar.png'}" class="message-avatar">
        `;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        try {
            const url = `/api/chats/${activeChatId}/messages`;
            const res = await fetch(url, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text})
            });
            if(res.ok) {
                loadChatMessages(); // Actual server update
            }
        } catch(e) {
            console.error(e);
        }
    });"""

# Because of encoding issues with Russian text in the replace block, I will use regex or find to replace the listener
import sys

idx = js.find("chatSendBtn.addEventListener('click', async () => {")
end_idx = js.find("});", idx) + 3

if idx != -1:
    old_listener = js[idx:end_idx]
    if "const text = chatInput.value.trim();" in old_listener:
        js = js.replace(old_listener, new_send_msg)
        print("Replaced send message listener!")

# 3. Voice Call Permissions fix
old_voice = """        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            isRecording = true;
            btn.style.color = '#ff4757';
            btn.style.animation = 'pulse 1s infinite alternate';
            
            mediaRecorder.ondataavailable = e => {
                audioChunks.push(e.data);
            };
            
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioChunks = [];
                // Simulate sending audio
                alert("ᮢ ᮮ饭 ᠭ! (⥣    ᫥. 䠧)");
                // Usually we'd upload to Supabase Storage and send the URL
            };
        } catch(e) {
            alert(" 㯠  䮭!");
        }"""

new_voice = """        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            isRecording = true;
            btn.style.color = '#ff4757';
            btn.style.animation = 'pulse 1s infinite alternate';
            
            mediaRecorder.ondataavailable = e => {
                audioChunks.push(e.data);
            };
            
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioChunks = [];
                // Simulate sending audio
                showToast("Голосовое сообщение отправлено! (интеграция в след. фазе)", "success");
            };
        } catch(e) {
            showToast("Нет доступа к микрофону. Нажмите на значок замка в адресной строке и разрешите доступ!", "error");
        }"""

idx_voice = js.find("const stream = await navigator.mediaDevices.getUserMedia({ audio: true });")
if idx_voice != -1:
    start_try = js.rfind("try {", 0, idx_voice)
    end_catch = js.find("}", js.find("catch(e) {", start_try)) + 1
    js = js[:start_try] + new_voice + js[end_catch:]
    print("Replaced voice recording logic!")

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
