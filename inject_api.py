import re

with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

endpoints = """
# ==========================================
# MESSENGER & PROFILES API
# ==========================================

@app.route('/api/sync_profile', methods=['POST'])
def sync_profile():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.json
    username = data.get('username')
    email = session['user']['email']
    
    if not username:
        return jsonify({'error': 'Missing username'}), 400
        
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    
    # Check if profile exists
    try:
        res = requests.get(f'{SUPABASE_URL}/rest/v1/tickets?status=eq.user_profile&user_email=eq.{email}', headers=headers)
        if res.status_code == 200 and len(res.json()) > 0:
            profile = res.json()[0]
            if profile.get('topic') != username:
                # Update username
                payload = {'topic': username}
                requests.patch(f"{SUPABASE_URL}/rest/v1/tickets?id=eq.{profile['id']}", headers=headers, json=payload)
            return jsonify({'success': True})
            
        # Create profile
        payload = {
            'user_email': email,
            'topic': username,
            'status': 'user_profile'
        }
        requests.post(f'{SUPABASE_URL}/rest/v1/tickets', headers=headers, json=payload)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search_users', methods=['GET'])
def search_users():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    q = request.args.get('q', '').lower()
    if not q or len(q) < 2:
        return jsonify({'users': []}), 200
        
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}'
    }
    
    try:
        # Fetch all profiles and filter by topic (username)
        # We can't use ilike directly on topic if we want simple partial match without strict rules, but let's try ilike
        res = requests.get(f'{SUPABASE_URL}/rest/v1/tickets?status=eq.user_profile&topic=ilike.*{q}*', headers=headers)
        if res.status_code == 200:
            users = [{'email': p['user_email'], 'username': p['topic']} for p in res.json() if p['user_email'] != session['user']['email']]
            return jsonify({'users': users}), 200
        return jsonify({'error': 'Failed to search'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contacts', methods=['GET', 'POST'])
def manage_contacts():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    email = session['user']['email']
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    
    if request.method == 'GET':
        try:
            res = requests.get(f'{SUPABASE_URL}/rest/v1/tickets?status=eq.contact_list&user_email=eq.{email}', headers=headers)
            if res.status_code == 200 and len(res.json()) > 0:
                contacts = res.json()[0].get('topic', '')
                if contacts:
                    contact_emails = contacts.split(',')
                    # Fetch their usernames
                    profiles_res = requests.get(f'{SUPABASE_URL}/rest/v1/tickets?status=eq.user_profile', headers=headers)
                    profiles_map = {p['user_email']: p['topic'] for p in profiles_res.json()} if profiles_res.status_code == 200 else {}
                    
                    result = [{'email': e, 'username': profiles_map.get(e, e)} for e in contact_emails if e]
                    return jsonify({'contacts': result}), 200
            return jsonify({'contacts': []}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    if request.method == 'POST':
        data = request.json
        target_email = data.get('email')
        
        try:
            res = requests.get(f'{SUPABASE_URL}/rest/v1/tickets?status=eq.contact_list&user_email=eq.{email}', headers=headers)
            if res.status_code == 200 and len(res.json()) > 0:
                contact_list = res.json()[0]
                existing = contact_list.get('topic', '').split(',') if contact_list.get('topic') else []
                if target_email not in existing:
                    existing.append(target_email)
                    payload = {'topic': ','.join(existing)}
                    requests.patch(f"{SUPABASE_URL}/rest/v1/tickets?id=eq.{contact_list['id']}", headers=headers, json=payload)
                return jsonify({'success': True}), 200
            else:
                payload = {
                    'user_email': email,
                    'topic': target_email,
                    'status': 'contact_list'
                }
                requests.post(f'{SUPABASE_URL}/rest/v1/tickets', headers=headers, json=payload)
                return jsonify({'success': True}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/get_chats', methods=['GET'])
def get_chats():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_email = session['user']['email']
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}'
    }
    
    try:
        # Get user profiles map to show usernames instead of emails
        profiles_res = requests.get(f'{SUPABASE_URL}/rest/v1/tickets?status=eq.user_profile', headers=headers)
        profiles_map = {p['user_email']: p['topic'] for p in profiles_res.json()} if profiles_res.status_code == 200 else {}
        
        res = requests.get(f'{SUPABASE_URL}/rest/v1/tickets?status=in.(chat_dm,chat_group)', headers=headers)
        if res.status_code == 200:
            all_chats = res.json()
            user_chats = []
            for c in all_chats:
                emails = c.get('user_email', '').split(',')
                if user_email in emails:
                    other_participants = [e for e in emails if e != user_email]
                    chat_name = c.get('topic')
                    if c.get('status') == 'chat_dm':
                        other_email = other_participants[0] if other_participants else user_email
                        chat_name = profiles_map.get(other_email, other_email)
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
    chat_type = data.get('type', 'chat_dm')
    group_name = data.get('group_name', 'New Group')
    
    if not target_email:
        return jsonify({'error': 'Target email required'}), 400
        
    user_email = session['user']['email']
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    
    participants = list(set([user_email] + target_email.split(',')))
    participants_str = ','.join(participants)
    
    if chat_type == 'chat_dm':
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
    
    res_ticket = requests.get(f'{SUPABASE_URL}/rest/v1/tickets?id=eq.{chat_id}', headers=headers)
    if res_ticket.status_code != 200 or not res_ticket.json():
        return jsonify({'error': 'Chat not found'}), 404
        
    emails = res_ticket.json()[0].get('user_email', '').split(',')
    if user_email not in emails and not session['user'].get('is_admin'):
        return jsonify({'error': 'Access denied'}), 403
        
    res_msgs = requests.get(f'{SUPABASE_URL}/rest/v1/ticket_messages?ticket_id=eq.{chat_id}&order=created_at.asc', headers=headers)
    
    # Get user profiles map to show usernames instead of emails in messages
    profiles_res = requests.get(f'{SUPABASE_URL}/rest/v1/tickets?status=eq.user_profile', headers=headers)
    profiles_map = {p['user_email']: p['topic'] for p in profiles_res.json()} if profiles_res.status_code == 200 else {}
    
    if res_msgs.status_code == 200:
        msgs = res_msgs.json()
        for m in msgs:
            m['sender_username'] = profiles_map.get(m['sender_email'], m['sender_email'])
        return jsonify({'messages': msgs}), 200
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
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    
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
        # Return the created message so frontend can use exact timestamp if needed
        return jsonify({'success': True, 'message': res.json()[0]}), 201
    return jsonify({'error': 'Failed to send message'}), 500
"""

if 'def get_chats(' not in text:
    text = text.replace('if __name__ == "__main__":', endpoints + '\nif __name__ == "__main__":')
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Injected Messenger & Profiles API successfully.")
else:
    print("API already injected.")
