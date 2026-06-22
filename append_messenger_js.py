import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

messenger_js = """
// ==========================================
// MESSENGER LOGIC
// ==========================================

let activeChatId = null;
let messagePollingInterval = null;
let lastMessageTime = 0;

document.addEventListener('DOMContentLoaded', () => {
    // Navigation
    document.querySelector('.nav-feed-link')?.addEventListener('click', (e) => {
        if(!window.currentUser) {
            e.preventDefault();
            showToast('Войдите, чтобы открыть Ленту', 'error');
            return;
        }
        showView('view-messenger');
        loadChats();
    });

    // New Chat Modal
    const newChatModal = document.getElementById('new-chat-modal');
    document.getElementById('new-chat-btn')?.addEventListener('click', () => {
        newChatModal.style.display = 'flex';
    });
    document.getElementById('close-chat-modal')?.addEventListener('click', () => {
        newChatModal.style.display = 'none';
    });

    // Tabs
    const tabDm = document.getElementById('tab-dm');
    const tabGroup = document.getElementById('tab-group');
    const dmForm = document.getElementById('dm-form');
    const groupForm = document.getElementById('group-form');
    let createChatType = 'chat_dm';

    tabDm?.addEventListener('click', () => {
        createChatType = 'chat_dm';
        tabDm.style.opacity = '1';
        tabGroup.style.opacity = '0.5';
        dmForm.style.display = 'block';
        groupForm.style.display = 'none';
    });

    tabGroup?.addEventListener('click', () => {
        createChatType = 'chat_group';
        tabGroup.style.opacity = '1';
        tabDm.style.opacity = '0.5';
        groupForm.style.display = 'block';
        dmForm.style.display = 'none';
    });

    // Create Chat Submit
    document.getElementById('create-chat-submit')?.addEventListener('click', async () => {
        const payload = { type: createChatType };
        if(createChatType === 'chat_dm') {
            payload.target_email = document.getElementById('dm-email').value.trim();
        } else {
            payload.target_email = document.getElementById('group-emails').value.trim();
            payload.group_name = document.getElementById('group-name').value.trim();
        }

        if(!payload.target_email) return showToast('Введите email', 'error');

        try {
            const res = await fetch('/api/create_chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if(res.ok) {
                showToast('Чат создан!', 'success');
                newChatModal.style.display = 'none';
                loadChats();
            } else {
                showToast(data.error || 'Ошибка', 'error');
            }
        } catch (e) {
            console.error(e);
        }
    });

    // Send Message
    document.getElementById('messenger-send-btn')?.addEventListener('click', sendMessengerMessage);
    document.getElementById('messenger-input')?.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') sendMessengerMessage();
    });

    // Stickers Panel
    const stickersBtn = document.getElementById('stickers-btn');
    const stickersPanel = document.getElementById('stickers-panel');
    stickersBtn?.addEventListener('click', () => {
        stickersPanel.style.display = stickersPanel.style.display === 'none' ? 'grid' : 'none';
    });
    
    document.querySelectorAll('.sticker-item').forEach(sticker => {
        sticker.addEventListener('click', () => {
            const url = sticker.src;
            sendMessengerMessage(`STICKER:${url}`);
            stickersPanel.style.display = 'none';
        });
    });
});

async function loadChats() {
    const chatsList = document.getElementById('chats-list');
    chatsList.innerHTML = '<div style="text-align: center; color: #888; margin-top: 20px;">Загрузка...</div>';
    
    try {
        const res = await fetch('/api/get_chats');
        const data = await res.json();
        
        if(res.ok) {
            chatsList.innerHTML = '';
            if(data.chats.length === 0) {
                chatsList.innerHTML = '<div style="padding: 20px; color: #888; text-align:center;">У вас пока нет чатов</div>';
                return;
            }
            
            data.chats.forEach(chat => {
                const el = document.createElement('div');
                el.className = `chat-item ${activeChatId === chat.id ? 'active' : ''}`;
                el.onclick = () => openChat(chat);
                
                const initial = chat.name.charAt(0).toUpperCase();
                
                el.innerHTML = `
                    <div class="chat-item-avatar">${initial}</div>
                    <div class="chat-item-info">
                        <span class="chat-item-name">${chat.name}</span>
                        <span class="chat-item-type">${chat.type === 'chat_group' ? 'Группа' : 'Личный'}</span>
                    </div>
                `;
                chatsList.appendChild(el);
            });
        }
    } catch(e) {
        console.error(e);
    }
}

async function openChat(chat) {
    activeChatId = chat.id;
    document.getElementById('no-chat-selected').style.display = 'none';
    document.getElementById('active-chat').style.display = 'flex';
    document.getElementById('active-chat-name').textContent = chat.name;
    
    // Highlight in list
    document.querySelectorAll('.chat-item').forEach(el => el.classList.remove('active'));
    // Since we re-render chats often, precise highlighting might require loadChats re-run or DOM traversal
    loadChats();
    
    loadChatMessages();
    
    // Setup polling
    if(messagePollingInterval) clearInterval(messagePollingInterval);
    messagePollingInterval = setInterval(loadChatMessages, 3000);
}

async function loadChatMessages() {
    if(!activeChatId) return;
    
    try {
        const res = await fetch(`/api/get_chat_messages/${activeChatId}`);
        const data = await res.json();
        
        if(res.ok) {
            const container = document.getElementById('active-chat-messages');
            container.innerHTML = '';
            
            data.messages.forEach(msg => {
                const isSentByMe = msg.sender_email === window.currentUser.email;
                const el = document.createElement('div');
                el.className = `chat-msg ${isSentByMe ? 'sent' : 'received'}`;
                
                let contentHTML = escapeHTML(msg.message);
                if(msg.message.startsWith('STICKER:')) {
                    el.classList.add('chat-msg-sticker');
                    contentHTML = `<img src="${escapeHTML(msg.message.replace('STICKER:', ''))}" alt="sticker">`;
                }
                
                const time = new Date(msg.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                
                el.innerHTML = `
                    ${!isSentByMe ? `<span class="chat-msg-sender">${escapeHTML(msg.sender_email.split('@')[0])}</span>` : ''}
                    ${contentHTML}
                    <span class="chat-msg-time">${time}</span>
                `;
                container.appendChild(el);
            });
            
            container.scrollTop = container.scrollHeight;
        }
    } catch(e) {
        console.error(e);
    }
}

async function sendMessengerMessage(forceMessage = null) {
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
}

// Utility to escape HTML to prevent XSS
function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag)
    );
}
"""

if 'MESSENGER LOGIC' not in js_text:
    with open('static/script.js', 'a', encoding='utf-8') as f:
        f.write('\n' + messenger_js)
    print("Added Messenger JS")
else:
    print("Messenger JS already exists")
