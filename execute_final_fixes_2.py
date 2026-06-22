import os

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix capitalization
html = html.replace('>ГЛАВНАЯ<', '>Главная<')
html = html.replace('>О НАС<', '>О нас<')
html = html.replace('>НАШИ УСЛУГИ<', '>Наши услуги<')

# 2. Check for emojis to replace
html = html.replace('👤', '<i class="fa-solid fa-user"></i>')
html = html.replace('⚙️', '<i class="fa-solid fa-gear"></i>')
html = html.replace('🚪', '<i class="fa-solid fa-door-open"></i>')
html = html.replace('🖼️', '<i class="fa-solid fa-image"></i>')
html = html.replace('✏️', '<i class="fa-solid fa-pen"></i>')
html = html.replace('🏠', '<i class="fa-solid fa-house"></i>')
html = html.replace('💬', '<i class="fa-solid fa-comment-dots"></i>')
html = html.replace('🤖', '<i class="fa-solid fa-robot"></i>')
html = html.replace('💳', '<i class="fa-solid fa-credit-card"></i>')
html = html.replace('🛒', '<i class="fa-solid fa-cart-shopping"></i>')

# Profile dropdown emojis (if they weren't matched above):
html = html.replace('Мой Профиль', '<i class="fa-solid fa-user"></i> Мой Профиль')
html = html.replace('Настройки', '<i class="fa-solid fa-gear"></i> Настройки')
html = html.replace('Сменить Аватар', '<i class="fa-solid fa-image"></i> Сменить Аватар')
html = html.replace('Выйти', '<i class="fa-solid fa-door-open"></i> Выйти')
html = html.replace('Админ-панель', '<i class="fa-solid fa-shield"></i> Админ-панель')


with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)


with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 3. Fix sendMessengerMessage bug (messenger-messages to active-chat-messages)
old_send = """    const msgsContainer = document.getElementById('messenger-messages');
    const msgDiv = document.createElement('div');
    msgDiv.className = 'msg-bubble msg-out';"""

new_send = """    const msgsContainer = document.getElementById('active-chat-messages');
    if (!msgsContainer) return;
    const msgDiv = document.createElement('div');
    msgDiv.className = 'chat-msg sent';"""

if old_send in js:
    js = js.replace(old_send, new_send)

# Wait, `sendMessengerMessage` has another `msgDiv.className` issue. In my previous code:
# `msgDiv.textContent = message;` for sent text. In `.chat-msg .sent`, text content works fine, but we also append `chat-msg-time`.
# Let's fix the innerHTML of msgDiv for optimistic UI.
old_msg_content = """    if(message.startsWith('STICKER:')) {
        const url = message.split('STICKER:')[1];
        msgDiv.innerHTML = `<img src="${url}" class="msg-sticker" style="max-width: 150px; border-radius: 10px;">`;
    } else {
        msgDiv.textContent = message;
    }
    msgsContainer.appendChild(msgDiv);"""

new_msg_content = """    const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    if(message.startsWith('STICKER:')) {
        msgDiv.classList.add('chat-msg-sticker');
        const url = message.split('STICKER:')[1];
        msgDiv.innerHTML = `<img src="${url}" alt="sticker"><span class="chat-msg-time">${time}</span>`;
    } else {
        msgDiv.innerHTML = `${escapeHTML(message)}<span class="chat-msg-time">${time}</span>`;
    }
    msgsContainer.appendChild(msgDiv);"""

if old_msg_content in js:
    js = js.replace(old_msg_content, new_msg_content)


with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

with open('templates/admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

# 4. Fix Admin Bot Status Selects
bots = ['aurexis_support', 'aurexis_economy', 'aurexis_mafia', 'aurexis_flora']
for bot in bots:
    old_input = f'<input type="text" id="status-{bot}-text" value="Online" style="padding:5px; background: transparent; color: white; border: 1px solid var(--neon-primary);">'
    old_input_alt = f'<input type="text" id="status-{bot}-text" value="Active" style="padding:5px; background: transparent; color: white; border: 1px solid var(--neon-primary);">'
    
    new_select = f'''<select id="status-{bot}-text" style="padding:5px; background: #111; color: white; border: 1px solid var(--neon-primary);" onchange="
        const c = document.getElementById('status-{bot}-color');
        if(this.value === 'Online') c.value = '#00ffaa';
        else if(this.value === 'Active') c.value = '#ff0055';
        else if(this.value === 'Offline') c.value = '#555555';
    ">
        <option value="Online">Online</option>
        <option value="Active">Active</option>
        <option value="Offline">Offline</option>
    </select>'''
    
    admin_html = admin_html.replace(old_input, new_select).replace(old_input_alt, new_select)


# 5. Add Delete Button to Tickets in admin.html
old_ticket_row = "<td><button class=\"flora-toggle\" onclick=\"openAdminTicket(${t.id}, '${t.topic}', '${t.status}')\">Открыть чат</button></td>"
new_ticket_row = "<td><button class=\"flora-toggle\" onclick=\"openAdminTicket(${t.id}, '${t.topic}', '${t.status}')\">Открыть чат</button> <button class=\"flora-toggle\" style=\"color: #ff4444; border-color: #ff4444; margin-left: 5px;\" onclick=\"deleteAdminTicket(${t.id})\">Удалить</button></td>"
admin_html = admin_html.replace(old_ticket_row, new_ticket_row)

# Make sure deleteAdminTicket function exists in admin.html
if "function deleteAdminTicket" not in admin_html:
    delete_func = """
        window.deleteAdminTicket = async function(id) {
            if(!confirm('Удалить тикет?')) return;
            try {
                const res = await fetch(`/api/admin/tickets/${id}`, {method: 'DELETE'});
                if(res.ok) loadAdminTickets();
            } catch(e) {}
        }
        """
    admin_html = admin_html.replace("loadUsers();", delete_func + "\n        loadUsers();")


with open('templates/admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_html)

print("Done!")
