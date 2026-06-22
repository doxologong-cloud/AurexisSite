import re

# 1. Update server.py
with open('server.py', 'r', encoding='utf-8') as f:
    server = f.read()

# Fix admin tickets query
old_admin_tickets = """@app.route('/api/admin/tickets', methods=['GET'])
def admin_tickets():
    if 'user' not in session or not session['user'].get('is_admin'):
        return jsonify({"success": False})
    url = f"{SUPABASE_URL}/rest/v1/tickets?select=*,users(nickname,avatar)&order=created_at.desc\""""

new_admin_tickets = """@app.route('/api/admin/tickets', methods=['GET'])
def admin_tickets():
    if 'user' not in session or not session['user'].get('is_admin'):
        return jsonify({"success": False})
    url = f"{SUPABASE_URL}/rest/v1/tickets?select=*&order=created_at.desc\""""

if old_admin_tickets in server:
    server = server.replace(old_admin_tickets, new_admin_tickets)

# Remove Global Chat API
old_global_chat = """# --- GLOBAL CHAT ---
@app.route('/api/global-chat', methods=['GET'])
def get_global_chat():
    url = f"{SUPABASE_URL}/rest/v1/global_chat?select=*,users(nickname,avatar,is_admin)&order=created_at.desc&limit=50"
    res = requests.get(url, headers=get_supabase_headers())
    if res.status_code == 200:
        msgs = res.json()
        msgs.reverse()
        return jsonify({"success": True, "messages": msgs})
    return jsonify({"success": False})

@app.route('/api/global-chat', methods=['POST'])
def post_global_chat():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Не авторизован"})
    
    data = request.json
    text = data.get('text', '').strip()
    if not text:
        return jsonify({"success": False})
        
    payload = {
        "user_email": session['user']['email'],
        "message": text
    }
    url = f"{SUPABASE_URL}/rest/v1/global_chat"
    res = requests.post(url, json=payload, headers=get_supabase_headers())
    return jsonify({"success": res.status_code == 201})"""

if old_global_chat in server:
    server = server.replace(old_global_chat, "")

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(server)
print("Updated server.py")

# 2. Update index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_html_global_chat_tab = """        <div class="chat-tab" data-tab="global">Global Chat</div>"""
if old_html_global_chat_tab in html:
    html = html.replace(old_html_global_chat_tab, "")

old_html_global_chat_list = """        <div id="global-chat-list" style="display:none; height:100%; align-items:center; justify-content:center; color:#555; text-align:center; padding:20px;">
            <p>Welcome to Global Chat.<br>Select a chat to begin.</p>
        </div>"""
if old_html_global_chat_list in html:
    html = html.replace(old_html_global_chat_list, "")

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html")
