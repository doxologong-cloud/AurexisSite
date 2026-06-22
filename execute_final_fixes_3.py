import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix capitalization of ГЛАВНАЯ and О НАС properly
html = re.sub(r'ГЛАВНАЯ', 'Главная', html)
html = re.sub(r'О НАС', 'О нас', html)
html = re.sub(r'НАШИ УСЛУГИ', 'Наши услуги', html)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)


with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 2. Fix infinite feed refresh and auto-scroll
old_load_chat = """            data.messages.forEach(msg => {
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
            
            container.scrollTop = container.scrollHeight;"""

new_load_chat = """            let newHtml = '';
            data.messages.forEach(msg => {
                const isSentByMe = msg.sender_email === window.currentUser.email;
                let contentHTML = escapeHTML(msg.message);
                let extraClass = '';
                if(msg.message.startsWith('STICKER:')) {
                    extraClass = 'chat-msg-sticker';
                    contentHTML = `<img src="${escapeHTML(msg.message.replace('STICKER:', ''))}" alt="sticker">`;
                }
                const time = new Date(msg.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                
                newHtml += `
                <div class="chat-msg ${isSentByMe ? 'sent' : 'received'} ${extraClass}">
                    ${!isSentByMe ? `<span class="chat-msg-sender">${escapeHTML(msg.sender_email.split('@')[0])}</span>` : ''}
                    ${contentHTML}
                    <span class="chat-msg-time">${time}</span>
                </div>
                `;
            });
            
            if (container.getAttribute('data-last-html') !== newHtml) {
                container.innerHTML = newHtml;
                container.setAttribute('data-last-html', newHtml);
                container.scrollTop = container.scrollHeight;
            }"""

if old_load_chat in js:
    js = js.replace(old_load_chat, new_load_chat)


# 3. Fix bot statuses animation
old_bot_update = """                        el.innerHTML = `<span class="status-dot" style="background: ${botData.color}; box-shadow: 0 0 10px ${botData.color}"></span> <span style="color: ${botData.color}">${botData.status}</span>`;"""
new_bot_update = """                        const anim = botData.status === 'Offline' ? 'none' : (botData.status === 'Active' ? 'blink 5s infinite' : 'blink 0.5s infinite');
                        el.innerHTML = `<span class="status-dot" style="background: ${botData.color}; box-shadow: ${botData.status === 'Offline' ? 'none' : `0 0 10px ${botData.color}`}; animation: ${anim}"></span> <span style="color: ${botData.color}">${botData.status}</span>`;"""

if old_bot_update in js:
    js = js.replace(old_bot_update, new_bot_update)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)


with open('templates/admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

# 4. Fix Admin Tickets Avatar and Instant Delete
old_admin_tickets = """                        const user = t.users || {};
                        const avatar = user.avatar || '/static/assets/default-avatar.png';
                        const nickname = user.nickname || t.user_email;
                        const statusStr = t.status === 'open' ? '<span style="color:#00ffaa;">Открыт</span>' : '<span style="color:#ff4444;">Закрыт</span>';
                        tbody.innerHTML += `<tr>"""

new_admin_tickets = """                        const avatar = t.user_avatar || '/static/assets/default-avatar.png';
                        const nickname = t.user_email;
                        const statusStr = t.status === 'open' ? '<span style="color:#00ffaa;">Открыт</span>' : '<span style="color:#ff4444;">Закрыт</span>';
                        tbody.innerHTML += `<tr id="ticket-row-${t.id}">"""

if old_admin_tickets in admin_html:
    admin_html = admin_html.replace(old_admin_tickets, new_admin_tickets)

old_delete = """        window.deleteAdminTicket = async function(id) {
            if(!confirm('Удалить тикет?')) return;
            try {
                const res = await fetch(`/api/admin/tickets/${id}`, {method: 'DELETE'});
                if(res.ok) loadAdminTickets();
            } catch(e) {}
        }"""

new_delete = """        window.deleteAdminTicket = async function(id) {
            if(!confirm('Удалить тикет?')) return;
            try {
                const row = document.getElementById('ticket-row-' + id);
                if(row) row.remove(); // optimistic delete
                
                const res = await fetch(`/api/admin/tickets/${id}`, {method: 'DELETE'});
                if(!res.ok) loadAdminTickets(); // fallback if failed
            } catch(e) {}
        }"""

if old_delete in admin_html:
    admin_html = admin_html.replace(old_delete, new_delete)

with open('templates/admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_html)

print("Fixes applied successfully!")
