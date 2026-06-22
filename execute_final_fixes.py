import re
import os

# 1. Update index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove Global Chat Widget completely
idx1 = html.find('<!-- Global Chat Widget -->')
idx2 = html.find('<!-- Styles for settings switch -->')
if idx1 != -1 and idx2 != -1:
    html = html[:idx1] + html[idx2:]

# Replace Emoji icons with FontAwesome
if '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">' not in html:
    html = html.replace('<link rel="stylesheet" href="static/style.css?v=', '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">\n    <link rel="stylesheet" href="static/style.css?v=')

html = html.replace('??', '<i class="fa-solid fa-house"></i>')
html = html.replace('??', '<i class="fa-solid fa-comment-dots"></i>')
html = html.replace('??', '<i class="fa-solid fa-robot"></i>')
html = html.replace('??', '<i class="fa-solid fa-credit-card"></i>')
html = html.replace('??', '<i class="fa-solid fa-cart-shopping"></i>')
html = html.replace('??', '<i class="fa-solid fa-user"></i>') # For account if any

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html")


# 2. Update script.js
with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix 2 second block (pointer-events)
old_preloader = """    // Fast preloader
    if (welcomeScreen) {
        setTimeout(() => {
            welcomeScreen.style.opacity = '0';
            setTimeout(() => {
                welcomeScreen.style.display = 'none';
                document.querySelector('.hero')?.classList.add('show');
                initScrollAnimations();
            }, 300); // fade out duration
        }, 1000); // 1 second fast glitch show
    } else {"""

new_preloader = """    // Ultra-Fast preloader without blocking clicks
    if (welcomeScreen) {
        welcomeScreen.style.pointerEvents = 'none'; // Fix 2 second block
        setTimeout(() => {
            welcomeScreen.style.opacity = '0';
            setTimeout(() => {
                welcomeScreen.style.display = 'none';
                document.querySelector('.hero')?.classList.add('show');
                initScrollAnimations();
            }, 300); // fade out duration
        }, 300); // 0.3 second very fast glitch show
    } else {"""

if old_preloader in js:
    js = js.replace(old_preloader, new_preloader)

# Remove loadChats() from openChat
js = js.replace("    loadChats();\n    \n    loadChatMessages();", "    // loadChats(); removed to prevent reload glitch\n    \n    loadChatMessages();")

# Add avatars to chat list
old_avatar = """                const initial = chat.name.charAt(0).toUpperCase();
                
                el.innerHTML = `
                    <div class="chat-item-avatar">${initial}</div>"""

new_avatar = """                const initial = chat.name.charAt(0).toUpperCase();
                let avatarHtml = `<div class="chat-item-avatar">${initial}</div>`;
                if(chat.avatar) {
                    avatarHtml = `<img src="${chat.avatar}" class="chat-item-avatar" style="object-fit:cover;">`;
                }
                
                el.innerHTML = `
                    ${avatarHtml}"""

if old_avatar in js:
    js = js.replace(old_avatar, new_avatar)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated script.js")


# 3. Update server.py to include avatars in chats & admin tickets
with open('server.py', 'r', encoding='utf-8') as f:
    server = f.read()

old_get_chats = """        # Get user profiles map to show usernames instead of emails
        profiles_res = requests.get(f'{SUPABASE_URL}/rest/v1/tickets?status=eq.user_profile', headers=headers)
        profiles_map = {p['user_email']: p['topic'] for p in profiles_res.json()} if profiles_res.status_code == 200 else {}"""

new_get_chats = """        # Get true users from DB for avatars and usernames
        users_res = requests.get(f'{SUPABASE_URL}/rest/v1/users?select=email,username,avatar', headers=headers)
        profiles_map = {}
        avatars_map = {}
        if users_res.status_code == 200:
            for u in users_res.json():
                profiles_map[u['email']] = u.get('username') or u['email']
                avatars_map[u['email']] = u.get('avatar')"""

if old_get_chats in server:
    server = server.replace(old_get_chats, new_get_chats)

old_chat_dict = """                    user_chats.append({
                        'id': c.get('id'),
                        'type': c.get('status'),
                        'name': chat_name,
                        'participants': emails
                    })"""

new_chat_dict = """                    user_chats.append({
                        'id': c.get('id'),
                        'type': c.get('status'),
                        'name': chat_name,
                        'avatar': avatars_map.get(other_email) if c.get('status') == 'chat_dm' else None,
                        'participants': emails
                    })"""

if old_chat_dict in server:
    server = server.replace(old_chat_dict, new_chat_dict)


# Admin Tickets Avatar fix
old_admin_tickets = """@app.route('/api/admin/tickets', methods=['GET'])
def admin_tickets():
    if 'user' not in session or not session['user'].get('is_admin'):
        return jsonify({"success": False})
    url = f"{SUPABASE_URL}/rest/v1/tickets?select=*&order=created_at.desc"
    res = requests.get(url, headers=get_supabase_headers())
    if res.status_code == 200:
        return jsonify({"success": True, "tickets": res.json()})
    return jsonify({"success": False})"""

new_admin_tickets = """@app.route('/api/admin/tickets', methods=['GET'])
def admin_tickets():
    if 'user' not in session or not session['user'].get('is_admin'):
        return jsonify({"success": False})
    url = f"{SUPABASE_URL}/rest/v1/tickets?select=*&order=created_at.desc"
    headers = get_supabase_headers()
    res = requests.get(url, headers=headers)
    
    users_res = requests.get(f'{SUPABASE_URL}/rest/v1/users?select=email,username,avatar', headers=headers)
    avatars_map = {}
    if users_res.status_code == 200:
        avatars_map = {u['email']: u.get('avatar') for u in users_res.json()}
        
    if res.status_code == 200:
        tickets = res.json()
        for t in tickets:
            t['user_avatar'] = avatars_map.get(t.get('user_email'))
        return jsonify({"success": True, "tickets": tickets})
    return jsonify({"success": False})"""

if old_admin_tickets in server:
    server = server.replace(old_admin_tickets, new_admin_tickets)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(server)
print("Updated server.py")


# 4. Update admin.html to show avatar instead of icon
with open('templates/admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

old_admin_ticket_ui = """                div.innerHTML = `
                    <div class="ticket-icon">??</div>
                    <div class="ticket-info">"""

new_admin_ticket_ui = """                const avHtml = t.user_avatar ? `<img src="${t.user_avatar}" class="ticket-icon" style="object-fit:cover; padding:0; background:transparent;">` : `<div class="ticket-icon"><i class="fa-solid fa-ticket"></i></div>`;
                div.innerHTML = `
                    ${avHtml}
                    <div class="ticket-info">"""

if old_admin_ticket_ui in admin_html:
    admin_html = admin_html.replace(old_admin_ticket_ui, new_admin_ticket_ui)
    
with open('templates/admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_html)
print("Updated admin.html")
