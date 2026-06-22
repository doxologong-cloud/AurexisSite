import re

with open('server.py', 'r', encoding='utf-8') as f:
    server_py = f.read()

# Add endpoints for Messenger
messenger_endpoints = """
# ==========================================
# MESSENGER (DM & GROUPS)
# ==========================================

@app.route('/api/get_chats', methods=['GET'])
def get_chats():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_email = session['user']['email']
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}'
    }
    
    # Supabase doesn't easily support LIKE query over multiple comma-separated lists for both DM and groups.
    # So we fetch all chats and filter in Python since we don't have thousands.
    try:
        res = requests.get(f'{SUPABASE_URL}/rest/v1/tickets?status=in.(chat_dm,chat_group)', headers=headers)
        if res.status_code == 200:
            all_chats = res.json()
            user_chats = []
            for c in all_chats:
                emails = c.get('user_email', '').split(',')
                if user_email in emails:
                    # Resolve other participants
                    other_participants = [e for e in emails if e != user_email]
                    chat_name = c.get('topic')
                    if c.get('status') == 'chat_dm':
                        # Fetch nickname of the other person
                        chat_name = other_participants[0] if other_participants else 'Unknown'
                        # In a real app we'd fetch the nickname, but we can do it on frontend
                    user_chats.append({
                        'id': c.get('id'),
                        'type': c.get('status'),
                        'name': chat_name,
                        'participants': emails
                    })
            return jsonify({'chats': user_chats}), 200
        return jsonify({'error': 'Failed to fetch chats'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/create_chat', methods=['POST'])
def create_chat():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    target_email = data.get('target_email')
    chat_type = data.get('type', 'chat_dm') # chat_dm or chat_group
    group_name = data.get('group_name', 'New Group')
    
    if not target_email:
        return jsonify({'error': 'Target email required'}), 400
        
    user_email = session['user']['email']
    
    # If DM, check if exists
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    
    participants = list(set([user_email] + target_email.split(',')))
    participants_str = ','.join(participants)
    
    if chat_type == 'chat_dm':
        # Check if DM exists
        try:
            res = requests.get(f'{SUPABASE_URL}/rest/v1/tickets?status=eq.chat_dm', headers=headers)
            if res.status_code == 200:
                for c in res.json():
                    emails = set(c.get('user_email', '').split(','))
                    if emails == set(participants):
                        return jsonify({'message': 'Chat already exists', 'chat': c}), 200
        except Exception:
            pass
            
    payload = {
        'user_email': participants_str,
        'topic': group_name if chat_type == 'chat_group' else 'DM',
        'status': chat_type
    }
    
    res = requests.post(f'{SUPABASE_URL}/rest/v1/tickets', headers=headers, json=payload)
    if res.status_code == 201:
        return jsonify({'message': 'Chat created', 'chat': res.json()[0]}), 201
    return jsonify({'error': 'Failed to create chat'}), 500

@app.route('/api/get_chat_messages/<int:chat_id>', methods=['GET'])
def get_chat_messages(chat_id):
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    user_email = session['user']['email']
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}'
    }
    
    # Verify participant
    res_ticket = requests.get(f'{SUPABASE_URL}/rest/v1/tickets?id=eq.{chat_id}', headers=headers)
    if res_ticket.status_code != 200 or not res_ticket.json():
        return jsonify({'error': 'Chat not found'}), 404
        
    emails = res_ticket.json()[0].get('user_email', '').split(',')
    if user_email not in emails and not session['user'].get('is_admin'):
        return jsonify({'error': 'Access denied'}), 403
        
    res_msgs = requests.get(f'{SUPABASE_URL}/rest/v1/ticket_messages?ticket_id=eq.{chat_id}&order=created_at.asc', headers=headers)
    if res_msgs.status_code == 200:
        return jsonify({'messages': res_msgs.json()}), 200
    return jsonify({'error': 'Failed to fetch messages'}), 500

@app.route('/api/send_chat_message', methods=['POST'])
def send_chat_message():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.json
    chat_id = data.get('chat_id')
    message = data.get('message')
    
    if not chat_id or not message:
        return jsonify({'error': 'Missing fields'}), 400
        
    user_email = session['user']['email']
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Verify participant
    res_ticket = requests.get(f'{SUPABASE_URL}/rest/v1/tickets?id=eq.{chat_id}', headers=headers)
    if res_ticket.status_code != 200 or not res_ticket.json():
        return jsonify({'error': 'Chat not found'}), 404
        
    emails = res_ticket.json()[0].get('user_email', '').split(',')
    if user_email not in emails and not session['user'].get('is_admin'):
        return jsonify({'error': 'Access denied'}), 403
        
    payload = {
        'ticket_id': chat_id,
        'sender_email': user_email,
        'message': message
    }
    
    res = requests.post(f'{SUPABASE_URL}/rest/v1/ticket_messages', headers=headers, json=payload)
    if res.status_code == 201:
        return jsonify({'success': True}), 201
    return jsonify({'error': 'Failed to send message'}), 500

# ==========================================
"""

if '# MESSENGER (DM & GROUPS)' not in server_py:
    server_py = server_py.replace('if __name__ == "__main__":', messenger_endpoints + '\nif __name__ == "__main__":')
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(server_py)
    print("Added messenger endpoints to server.py")
else:
    print("Endpoints already added.")
