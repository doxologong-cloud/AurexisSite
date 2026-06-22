import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

new_js = """
// ==========================================
// SEARCH, CONTACTS & OPTIMISTIC UI
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('user-search-input');
    const searchResults = document.getElementById('search-results-container');
    const tabChats = document.getElementById('tab-chats');
    const tabContacts = document.getElementById('tab-contacts');
    
    let searchTimeout;
    
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            const q = e.target.value.trim();
            if (q.length < 2) {
                searchResults.style.display = 'none';
                return;
            }
            
            searchTimeout = setTimeout(async () => {
                try {
                    const res = await fetch(`/api/search_users?q=${encodeURIComponent(q)}`);
                    const data = await res.json();
                    
                    searchResults.innerHTML = '';
                    if (data.users && data.users.length > 0) {
                        data.users.forEach(u => {
                            const div = document.createElement('div');
                            div.style.padding = '10px';
                            div.style.cursor = 'pointer';
                            div.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
                            div.innerHTML = `<span style="color: white; font-weight: bold;">${u.username}</span> <br><span style="color: gray; font-size: 0.8rem;">${u.email}</span>`;
                            
                            // On click, start chat
                            div.addEventListener('click', async () => {
                                searchResults.style.display = 'none';
                                searchInput.value = '';
                                
                                // Call create_chat
                                try {
                                    const cRes = await fetch('/api/create_chat', {
                                        method: 'POST',
                                        headers: {'Content-Type': 'application/json'},
                                        body: JSON.stringify({target_email: u.email, type: 'chat_dm'})
                                    });
                                    if (cRes.ok) {
                                        loadChats();
                                        // Wait a moment then open chat
                                        setTimeout(() => {
                                            const chatEl = Array.from(document.querySelectorAll('.chat-item')).find(el => el.textContent.includes(u.username));
                                            if (chatEl) chatEl.click();
                                        }, 500);
                                    }
                                } catch (e) {}
                            });
                            
                            searchResults.appendChild(div);
                        });
                        searchResults.style.display = 'block';
                    } else {
                        searchResults.innerHTML = '<div style="padding: 10px; color: gray;">Ничего не найдено</div>';
                        searchResults.style.display = 'block';
                    }
                } catch(e) {}
            }, 500);
        });
    }

    // Hide search results on click outside
    document.addEventListener('click', (e) => {
        if (searchResults && !searchResults.contains(e.target) && e.target !== searchInput) {
            searchResults.style.display = 'none';
        }
    });
    
    // Tab switching
    if (tabChats && tabContacts) {
        tabChats.addEventListener('click', () => {
            tabChats.classList.add('active');
            tabChats.style.color = 'var(--neon-primary)';
            tabContacts.classList.remove('active');
            tabContacts.style.color = '#888';
            loadChats();
        });
        
        tabContacts.addEventListener('click', () => {
            tabContacts.classList.add('active');
            tabContacts.style.color = 'var(--neon-primary)';
            tabChats.classList.remove('active');
            tabChats.style.color = '#888';
            loadContacts();
        });
    }
});

async function loadContacts() {
    const list = document.getElementById('chat-list');
    if (!list) return;
    list.innerHTML = '<div style="text-align:center; padding: 20px; color: gray;">Загрузка контактов...</div>';
    
    try {
        const res = await fetch('/api/contacts');
        const data = await res.json();
        
        list.innerHTML = '';
        if (data.contacts && data.contacts.length > 0) {
            data.contacts.forEach(c => {
                const div = document.createElement('div');
                div.className = 'chat-item';
                div.innerHTML = `
                    <div class="chat-avatar" style="background: var(--neon-secondary);">👤</div>
                    <div class="chat-info">
                        <div class="chat-name">${c.username}</div>
                        <div class="chat-preview">${c.email}</div>
                    </div>
                `;
                div.addEventListener('click', async () => {
                    // Start chat with contact
                    try {
                        const cRes = await fetch('/api/create_chat', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({target_email: c.email, type: 'chat_dm'})
                        });
                        if (cRes.ok) {
                            document.getElementById('tab-chats').click(); // switch back to chats
                            setTimeout(() => {
                                const chatEl = Array.from(document.querySelectorAll('.chat-item')).find(el => el.textContent.includes(c.username));
                                if (chatEl) chatEl.click();
                            }, 500);
                        }
                    } catch (e) {}
                });
                list.appendChild(div);
            });
        } else {
            list.innerHTML = '<div style="text-align:center; padding: 20px; color: gray;">Нет контактов. Найдите друзей через поиск!</div>';
        }
    } catch(e) {}
}

async function addContact(email) {
    try {
        await fetch('/api/contacts', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email: email})
        });
        showToast('Добавлен в контакты', 'success');
    } catch(e) {}
}

// Add sync profile call to loadChats wrapper
const originalLoadChats = window.loadChats;
window.loadChats = async function() {
    if (window.currentUser && document.getElementById('nav-username')) {
        // Sync profile implicitly
        const username = document.getElementById('nav-username').textContent;
        fetch('/api/sync_profile', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username})
        }).catch(e => {});
    }
    
    // Check which tab is active
    const tabChats = document.getElementById('tab-chats');
    if (tabChats && !tabChats.classList.contains('active')) {
        return; // Contacts tab is active
    }
    
    if (originalLoadChats) {
        originalLoadChats.apply(this, arguments);
    }
}
"""

# Override the sendMessage function to implement Optimistic UI
optimistic_ui_patch = """
        // OPTIMISTIC UI: Append immediately
        const container = document.getElementById('chat-messages');
        const username = document.getElementById('nav-username') ? document.getElementById('nav-username').textContent : 'Я';
        const isSticker = msg.startsWith('STICKER:');
        
        let msgHtml = '';
        if (isSticker) {
            const stickerUrl = msg.replace('STICKER:', '');
            msgHtml = `<img src="${stickerUrl}" style="max-width: 100px; max-height: 100px; border-radius: 10px;">`;
        } else {
            msgHtml = msg;
        }
        
        const myMsgDiv = document.createElement('div');
        myMsgDiv.className = 'message message-mine optimistic';
        myMsgDiv.innerHTML = `
            <div class="message-sender">${username}</div>
            <div class="message-bubble">${msgHtml}</div>
        `;
        container.appendChild(myMsgDiv);
        container.scrollTop = container.scrollHeight;
"""

if 'SEARCH, CONTACTS & OPTIMISTIC UI' not in text:
    text = text + '\n' + new_js
    text = text.replace("sendBtn.disabled = true;", optimistic_ui_patch + "\n            sendBtn.disabled = true;")
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(text)
    
    print("Added Search, Contacts, and Optimistic UI logic.")
else:
    print("Logic already exists.")
