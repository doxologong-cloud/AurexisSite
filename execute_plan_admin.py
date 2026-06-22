import re

# 1. Update server.py
with open('server.py', 'r', encoding='utf-8') as f:
    server = f.read()

delete_api = """@app.route('/api/admin/tickets/<int:ticket_id>', methods=['DELETE'])
def admin_delete_ticket(ticket_id):
    if 'user' not in session or not session['user'].get('is_admin'):
        return jsonify({"success": False})
    url = f"{SUPABASE_URL}/rest/v1/tickets?id=eq.{ticket_id}"
    res = requests.delete(url, headers=get_supabase_headers())
    return jsonify({"success": res.status_code in [200, 204]})

@app.route('/api/admin/tickets/<int:ticket_id>/status', methods=['PATCH'])"""

if '@app.route(\'/api/admin/tickets/<int:ticket_id>\', methods=[\'DELETE\'])' not in server:
    server = server.replace("@app.route('/api/admin/tickets/<int:ticket_id>/status', methods=['PATCH'])", delete_api)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(server)
print("Updated server.py")

# 2. Update admin.html
with open('templates/admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_html_buttons = """        <div style="display:flex; justify-content: flex-end; gap:10px; margin-top:20px;">
            <button class="btn" style="background:#ff4444; border:none; padding:10px 20px;" onclick="closeAdminTicketStatus()">Close Ticket</button>
            <button class="btn btn-primary" onclick="closeAdminTicket()">Back</button>
        </div>"""

new_html_buttons = """        <div style="display:flex; justify-content: space-between; align-items:center; margin-top:20px;">
            <button class="btn" style="background:#8b0000; border:1px solid #ff4444; color:white; padding:10px 20px;" onclick="deleteAdminTicket()">Delete Ticket</button>
            <div style="display:flex; gap:10px;">
                <button class="btn" style="background:#ff4444; border:none; padding:10px 20px;" onclick="closeAdminTicketStatus()">Close Ticket</button>
                <button class="btn btn-primary" onclick="closeAdminTicket()">Back</button>
            </div>
        </div>"""

if old_html_buttons in html:
    html = html.replace(old_html_buttons, new_html_buttons)

js_delete_logic = """        window.closeAdminTicketStatus = async function() {
            try {
                const res = await fetch(`/api/admin/tickets/${currentAdminTicketId}/status`, {
                    method: 'PATCH',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({status: 'closed'})
                });
                if(res.ok) {
                    closeAdminTicket();
                    loadAdminTickets();
                }
            } catch(e) {}
        }

        window.deleteAdminTicket = async function() {
            if(!confirm('Are you sure you want to completely delete this ticket?')) return;
            try {
                const res = await fetch(`/api/admin/tickets/${currentAdminTicketId}`, {
                    method: 'DELETE'
                });
                if(res.ok) {
                    closeAdminTicket();
                    loadAdminTickets();
                }
            } catch(e) {}
        }"""

if 'window.deleteAdminTicket = ' not in html:
    idx = html.find('window.closeAdminTicketStatus = async function() {')
    if idx != -1:
        end_idx = html.find('}', html.find('} catch(e) {}', idx)) + 1
        old_js = html[idx:end_idx]
        html = html.replace(old_js, js_delete_logic)

with open('templates/admin.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated admin.html")
