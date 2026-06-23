from flask import Flask, Response, render_template, request, jsonify, session
import sqlite3 # Kept for backwards compatibility but unused
import requests
import random
import os
import hashlib
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = os.getenv("SECRET_KEY", "super-secret-key-12345")

SUPABASE_URL = "https://bbeaokhcckhuhcxnagsf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJiZWFva2hjY2todWhjeG5hZ3NmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODIwNjMxNzIsImV4cCI6MjA5NzYzOTE3Mn0.uO8VD42bQ9W9udl2GWF02uK8zpVCXR2QEo0nrMps6OM"

def get_supabase_headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def get_user_by_email(email):
    try:
        url = f"{SUPABASE_URL}/rest/v1/users?email=eq.{email}&select=*"
        res = requests.get(url, headers=get_supabase_headers())
        if res.status_code == 200:
            users = res.json()
            if len(users) > 0:
                return users[0]
    except Exception as e:
        print("Supabase GET error:", e)
    return None

def create_user(nickname, email, password, username=None):
    if not username:
        username = "@user" + str(random.randint(100000, 999999))
    try:
        url = f"{SUPABASE_URL}/rest/v1/users"
        payload = {"nickname": nickname, "email": email, "password": password, "username": username}
        res = requests.post(url, json=payload, headers=get_supabase_headers())
        if res.status_code in [200, 201]:
            return True, username
        return False, None
    except Exception as e:
        print("Supabase POST error:", e)
        return False, None

def update_user_avatar(email, avatar_base64):
    try:
        url = f"{SUPABASE_URL}/rest/v1/users?email=eq.{email}"
        payload = {"avatar": avatar_base64}
        res = requests.patch(url, json=payload, headers=get_supabase_headers())
        return res.status_code in [200, 204]
    except Exception as e:
        print("Supabase PATCH error:", e)
        return False

# In-memory storage for verification codes
verification_codes = {}
reset_codes = {}

def send_email(to_email, code):
    service_id = os.getenv("EMAILJS_SERVICE_ID", "service_ib5so3b")
    template_id = os.getenv("EMAILJS_TEMPLATE_ID", "template_hwk92vh")
    public_key = os.getenv("EMAILJS_PUBLIC_KEY", "kYhDdXzww191JNlMc")
    private_key = os.getenv("EMAILJS_PRIVATE_KEY", "TSRZvPlfaj6paVRfmVzCW")
    
    if not service_id or not template_id or not public_key:
        print(f"MOCK EMAIL SENT: Code {code} to {to_email}")
        return True # Mock success

    url = "https://api.emailjs.com/api/v1.0/email/send"
    payload = {
        "service_id": service_id,
        "template_id": template_id,
        "user_id": public_key,
        "accessToken": private_key,
        "template_params": {
            "to_email": to_email,
            "code": code
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return True
        else:
            print(f"EmailJS API Error: {response.text}")
            return False
    except Exception as e:
        print(f"Request Error: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email', '').strip()
    nickname = data.get('nickname', '').strip()
    password = data.get('password', '')
    
    if not email or not nickname or not password:
        return jsonify({"success": False, "message": "Заполните все поля."})
        
    # Check if user already exists
    if get_user_by_email(email):
        return jsonify({"success": False, "message": "Эта почта уже зарегистрирована."})

    # Generate and send code
    code = str(random.randint(1000, 9999))
    verification_codes[email] = {
        "code": code,
        "nickname": data.get('nickname'),
        "password": hashlib.sha256(data.get('password').encode()).hexdigest()
    }
    
    if send_email(email, code):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Ошибка отправки почты. Проверьте настройки SMTP."})

@app.route('/api/verify', methods=['POST'])
def verify():
    data = request.json
    email = data.get('email')
    code = data.get('code')
    
    if email in verification_codes and verification_codes[email]['code'] == code:
        user_data = verification_codes[email]
        
        # Save to DB
        success, username = create_user(user_data['nickname'], email, user_data['password'])
        if not success:
            return jsonify({"success": False, "message": "Ошибка сохранения в облако."})
        
        del verification_codes[email]
        session['user'] = {"nickname": user_data['nickname'], "email": email, "avatar": None, "username": username}
        return jsonify({"success": True, "user": session['user']})
    
    return jsonify({"success": False, "message": "Неверный код."})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = hashlib.sha256(data.get('password').encode()).hexdigest()
    
    user = get_user_by_email(email)
    
    if user and user.get('password') == password:
        session['user'] = {
            "nickname": user.get('nickname'), 
            "email": email, 
            "username": user.get('username'),
            "is_admin": user.get('is_admin', False),
            "flora_status": user.get('flora_status', False)
        }
        # Send avatar directly in the response, but NOT in the session cookie
        user_response = session['user'].copy()
        user_response['avatar'] = user.get('avatar')
        return jsonify({"success": True, "user": user_response})
    return jsonify({"success": False, "message": "Неверная почта или пароль."})

@app.route('/api/google-login', methods=['POST'])
def google_login():
    data = request.json
    token = data.get('token')
    if not token:
        return jsonify({"success": False, "message": "Токен не предоставлен."})
    
    try:
        res = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")
        if res.status_code != 200:
            return jsonify({"success": False, "message": "Неверный токен."})
        
        token_info = res.json()
        email = token_info.get('email')
        nickname = token_info.get('name')
        picture = token_info.get('picture')
        
        user = get_user_by_email(email)
        avatar_url = picture
        
        if not user:
            # Create new user via Google
            success, username = create_user(nickname, email, "google-oauth")
            if not success:
                return jsonify({"success": False, "message": "Ошибка регистрации через Google."})
            if picture:
                update_user_avatar(email, picture)
        else:
            # Existing user
            nickname = user.get('nickname')
            avatar_url = user.get('avatar')
            username = user.get('username')
            is_admin = user.get('is_admin', False)
            flora_status = user.get('flora_status', False)
            if not avatar_url and picture:
                update_user_avatar(email, picture)
                avatar_url = picture
                
        session['user'] = {
            "nickname": nickname, 
            "email": email, 
            "username": username,
            "is_admin": is_admin if 'is_admin' in locals() else False,
            "flora_status": flora_status if 'flora_status' in locals() else False
        }
        
        user_response = session['user'].copy()
        user_response['avatar'] = avatar_url
        return jsonify({"success": True, "user": user_response})
        
    except Exception as e:
        return jsonify({"success": False, "message": "Ошибка базы данных."})

# --- PASSWORD RESET ---
@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({"success": False, "message": "Введите email."})
        
    user = get_user_by_email(email)
    if not user:
        return jsonify({"success": False, "message": "Пользователь не найден."})
        
    code = generate_verification_code()
    reset_codes[email] = code
    
    if send_verification_email(email, code):
        return jsonify({"success": True, "message": "Код отправлен на вашу почту."})
    else:
        return jsonify({"success": False, "message": "Ошибка отправки письма."})

@app.route('/api/verify-reset-code', methods=['POST'])
def verify_reset_code():
    data = request.json
    email = data.get('email')
    code = data.get('code')
    
    if reset_codes.get(email) == code:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Неверный код."})

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    code = data.get('code')
    new_password = data.get('password')
    
    if reset_codes.get(email) != code:
        return jsonify({"success": False, "message": "Неверный код."})
        
    if len(new_password) < 6:
        return jsonify({"success": False, "message": "Пароль слишком короткий."})
        
    url = f"{SUPABASE_URL}/rest/v1/users?email=eq.{email}"
    payload = {"password": hash_password(new_password)}
    res = requests.patch(url, json=payload, headers=get_supabase_headers())
    
    if res.status_code in [200, 204]:
        reset_codes.pop(email, None) # Clear the code
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Ошибка сохранения нового пароля."})

@app.route('/api/update-profile', methods=['POST'])
def update_profile():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Не авторизован."})
    
    data = request.json
    new_nickname = data.get('nickname')
    new_username = data.get('username')
    new_banner = data.get('banner')
    new_status_text = data.get('status_text')
    email = session['user']['email']
    
    if not new_nickname or not new_username:
        return jsonify({"success": False, "message": "Заполните все поля."})
        
    if not new_username.startswith('@'):
        new_username = '@' + new_username

    try:
        # Check if username is taken by someone else
        check_url = f"{SUPABASE_URL}/rest/v1/users?username=eq.{new_username}&email=neq.{email}&select=*"
        check_res = requests.get(check_url, headers=get_supabase_headers())
        if check_res.status_code == 200 and len(check_res.json()) > 0:
            return jsonify({"success": False, "message": "Этот @username уже занят!"})
            
        # Update user
        url = f"{SUPABASE_URL}/rest/v1/users?email=eq.{email}"
        payload = {"nickname": new_nickname, "username": new_username}
        if new_banner is not None:
            payload["banner"] = new_banner
        if new_status_text is not None:
            payload["status_text"] = new_status_text

        res = requests.patch(url, json=payload, headers=get_supabase_headers())
        
        if res.status_code in [200, 204]:
            session['user']['nickname'] = new_nickname
            session['user']['username'] = new_username
            if new_status_text is not None:
                session['user']['status_text'] = new_status_text
            session.modified = True
            
            # Fetch fresh user data to return, including large base64 strings
            db_user = get_user_by_email(email)
            if db_user:
                full_user = {
                    "nickname": db_user.get('nickname'),
                    "email": email,
                    "avatar": db_user.get('avatar'),
                    "username": db_user.get('username'),
                    "is_admin": db_user.get('is_admin', False),
                    "flora_status": db_user.get('flora_status', False),
                    "banner": db_user.get('banner'),
                    "status_text": db_user.get('status_text')
                }
                return jsonify({"success": True, "user": full_user})
            return jsonify({"success": True, "user": session['user']})
            
        return jsonify({"success": False, "message": "Ошибка сохранения профиля."})
    except Exception as e:
        print("Profile update error:", e)
        return jsonify({"success": False, "message": "Ошибка сервера."})

@app.route('/api/update-avatar', methods=['POST'])
def update_avatar():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Не авторизован."})
    
    data = request.json
    avatar_base64 = data.get('avatar')
    if not avatar_base64:
        return jsonify({"success": False, "message": "Нет аватарки."})
        
    success = update_user_avatar(session['user']['email'], avatar_base64)
    if success:
        # DO NOT save base64 avatar into the session!
        # Flask sessions are stored in cookies (max 4KB limit). 
        # Large base64 strings will break the cookie and be silently rejected by the browser!
        # The fresh avatar will be pulled from DB in /api/me on next reload.
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Ошибка сохранения в облако."})

@app.route('/api/me', methods=['GET'])
def me():
    if 'user' in session:
        # Fetch fresh data from DB because session cookie cannot hold large base64 avatars
        email = session['user'].get('email')
        db_user = get_user_by_email(email)
        if db_user:
            # Update session with safe fields just in case
            session['user']['nickname'] = db_user.get('nickname')
            session['user']['username'] = db_user.get('username')
            session['user']['is_admin'] = db_user.get('is_admin', False)
            session['user']['flora_status'] = db_user.get('flora_status', False)
            session.modified = True
            
            # Send full user data including large avatar base64
            full_user = {
                "nickname": db_user.get('nickname'),
                "email": email,
                "avatar": db_user.get('avatar'),
                "username": db_user.get('username'),
                "is_admin": db_user.get('is_admin', False),
                "flora_status": db_user.get('flora_status', False),
                "banner": db_user.get('banner'),
                "status_text": db_user.get('status_text')
            }
            return jsonify({"success": True, "user": full_user})
        else:
            session.pop('user', None)
            return jsonify({"success": False})
    return jsonify({"success": False})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"success": True})

# --- REVIEWS ---
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    url = f"{SUPABASE_URL}/rest/v1/reviews?select=*,users(nickname,avatar,username)&order=created_at.desc&limit=10"
    res = requests.get(url, headers=get_supabase_headers())
    if res.status_code == 200:
        return jsonify({"success": True, "reviews": res.json()})
    return jsonify({"success": False, "message": "Ошибка БД"})

@app.route('/api/reviews', methods=['POST'])
def add_review():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Не авторизован."})
    
    data = request.json
    rating = data.get('rating')
    text = data.get('text')
    
    if not text or not rating:
        return jsonify({"success": False, "message": "Заполните все поля."})
        
    email = session['user']['email']
    
    # Check if user already reviewed
    check_url = f"{SUPABASE_URL}/rest/v1/reviews?email=eq.{email}&select=id"
    check_res = requests.get(check_url, headers=get_supabase_headers())
    if check_res.status_code == 200 and len(check_res.json()) > 0:
        return jsonify({"success": False, "message": "Вы уже оставляли отзыв!"})
        
    url = f"{SUPABASE_URL}/rest/v1/reviews"
    payload = {"email": email, "rating": int(rating), "text": text}
    res = requests.post(url, json=payload, headers=get_supabase_headers())
    if res.status_code in [200, 201]:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Ошибка сохранения."})

# --- PUBLIC PROFILES ---
@app.route('/u/<username>')
def public_profile(username):
    # Search for user by username
    if not username.startswith('@'):
        username = '@' + username
    url = f"{SUPABASE_URL}/rest/v1/users?username=eq.{username}&select=*"
    res = requests.get(url, headers=get_supabase_headers())
    if res.status_code == 200:
        users = res.json()
        if len(users) > 0:
            target_user = users[0]
            return render_template('profile.html', target_user=target_user)
    return "Пользователь не найден", 404

# --- ADMIN ROUTES ---
@app.route('/admin')
def admin_panel():
    if 'user' not in session or not session['user'].get('is_admin'):
        return "Доступ запрещен", 403
    return render_template('admin.html')

@app.route('/api/admin/users', methods=['GET'])
def admin_get_users():
    if 'user' not in session or not session['user'].get('is_admin'):
        return jsonify({"success": False, "message": "Доступ запрещен"})
    url = f"{SUPABASE_URL}/rest/v1/users?select=*"
    res = requests.get(url, headers=get_supabase_headers())
    if res.status_code == 200:
        users = res.json()
        # Remove passwords for safety
        for u in users:
            u.pop('password', None)
        return jsonify({"success": True, "users": users})
    return jsonify({"success": False, "message": "Ошибка БД"})

@app.route('/api/admin/update-flora', methods=['POST'])
def admin_update_flora():
    if 'user' not in session or not session['user'].get('is_admin'):
        return jsonify({"success": False, "message": "Доступ запрещен"})
    data = request.json
    target_email = data.get('email')
    new_status = data.get('flora_status')
    
    url = f"{SUPABASE_URL}/rest/v1/users?email=eq.{target_email}"
    payload = {"flora_status": new_status}
    res = requests.patch(url, json=payload, headers=get_supabase_headers())
    if res.status_code in [200, 204]:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Ошибка сохранения"})

# --- BOT STATUS ---
def get_bot_status():
    try:
        if os.path.exists('bot_status.json'):
            with open('bot_status.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {"aurexis_music": {"status": "Online", "color": "#00ffaa"}}

@app.route('/api/bots/status', methods=['GET'])
def api_get_bot_status():
    return jsonify({"success": True, "bots": get_bot_status()})

@app.route('/api/admin/bot-status', methods=['POST'])
def admin_update_bot_status():
    if 'user' not in session or not session['user'].get('is_admin'):
        return jsonify({"success": False, "message": "Доступ запрещен"})
    
    data = request.json
    bot_id = data.get('bot_id')
    status = data.get('status')
    color = data.get('color')
    
    current_status = get_bot_status()
    current_status[bot_id] = {"status": status, "color": color}
    
    try:
        with open('bot_status.json', 'w', encoding='utf-8') as f:
            json.dump(current_status, f, ensure_ascii=False)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": "Ошибка сохранения"})

# --- NEWS ---
@app.route('/api/news', methods=['GET'])
def get_news():
    url = f"{SUPABASE_URL}/rest/v1/news?select=*&order=created_at.desc"
    res = requests.get(url, headers=get_supabase_headers())
    if res.status_code == 200:
        return jsonify({"success": True, "news": res.json()})
    return jsonify({"success": False, "news": []})

@app.route('/api/admin/news', methods=['POST'])
def add_news():
    if 'user' not in session or not session['user'].get('is_admin'):
        return jsonify({"success": False})
    data = request.json
    payload = {"title": data.get("title"), "content": data.get("content")}
    url = f"{SUPABASE_URL}/rest/v1/news"
    res = requests.post(url, json=payload, headers=get_supabase_headers())
    return jsonify({"success": res.status_code in [201, 204]})

@app.route('/api/admin/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    if 'user' not in session or not session['user'].get('is_admin'):
        return jsonify({"success": False})
    url = f"{SUPABASE_URL}/rest/v1/news?id=eq.{news_id}"
    res = requests.delete(url, headers=get_supabase_headers())
    return jsonify({"success": res.status_code in [200, 204]})

# --- TICKETS ---
@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    if 'user' not in session:
        return jsonify({"success": False})
    email = session['user']['email']
    data = request.json
    topic = data.get("topic")
    message = data.get("message")
    
    url = f"{SUPABASE_URL}/rest/v1/tickets"
    payload = {"user_email": email, "topic": topic, "status": "open"}
    headers = get_supabase_headers()
    headers["Prefer"] = "return=representation"
    res = requests.post(url, json=payload, headers=headers)
    if res.status_code in [201, 200]:
        ticket = res.json()[0]
        msg_url = f"{SUPABASE_URL}/rest/v1/ticket_messages"
        msg_payload = {"ticket_id": ticket['id'], "sender_email": email, "message": message}
        requests.post(msg_url, json=msg_payload, headers=get_supabase_headers())
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route('/api/tickets/my', methods=['GET'])
def my_tickets():
    if 'user' not in session:
        return jsonify({"success": False})
    email = session['user']['email']
    url = f"{SUPABASE_URL}/rest/v1/tickets?user_email=eq.{email}&select=*&order=created_at.desc"
    res = requests.get(url, headers=get_supabase_headers())
    if res.status_code == 200:
        return jsonify({"success": True, "tickets": res.json()})
    return jsonify({"success": False, "tickets": []})

@app.route('/api/tickets/<int:ticket_id>/messages', methods=['GET'])
def get_ticket_messages(ticket_id):
    if 'user' not in session:
        return jsonify({"success": False})
    url = f"{SUPABASE_URL}/rest/v1/ticket_messages?ticket_id=eq.{ticket_id}&select=*&order=created_at.asc"
    res = requests.get(url, headers=get_supabase_headers())
    if res.status_code == 200:
        return jsonify({"success": True, "messages": res.json()})
    return jsonify({"success": False})

@app.route('/api/tickets/<int:ticket_id>/reply', methods=['POST'])
def reply_ticket(ticket_id):
    if 'user' not in session:
        return jsonify({"success": False})
    email = session['user']['email']
    data = request.json
    msg_url = f"{SUPABASE_URL}/rest/v1/ticket_messages"
    msg_payload = {"ticket_id": ticket_id, "sender_email": email, "message": data.get("message")}
    res = requests.post(msg_url, json=msg_payload, headers=get_supabase_headers())
    return jsonify({"success": res.status_code in [201, 200, 204]})

@app.route('/api/admin/tickets', methods=['GET'])
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
    return jsonify({"success": False})

@app.route('/api/admin/tickets/<int:ticket_id>', methods=['DELETE'])
def admin_delete_ticket(ticket_id):
    if 'user' not in session or not session['user'].get('is_admin'):
        return jsonify({"success": False})
    url = f"{SUPABASE_URL}/rest/v1/tickets?id=eq.{ticket_id}"
    res = requests.delete(url, headers=get_supabase_headers())
    return jsonify({"success": res.status_code in [200, 204]})

@app.route('/api/admin/tickets/<int:ticket_id>/status', methods=['PATCH'])
def admin_ticket_status(ticket_id):
    if 'user' not in session or not session['user'].get('is_admin'):
        return jsonify({"success": False})
    data = request.json
    url = f"{SUPABASE_URL}/rest/v1/tickets?id=eq.{ticket_id}"
    payload = {"status": data.get("status")}
    res = requests.patch(url, json=payload, headers=get_supabase_headers())
    return jsonify({"success": res.status_code in [200, 204]})

# --- GLOBAL CHAT ---
@app.route('/api/global-chat', methods=['GET'])
def get_global_chat():
    url = f"{SUPABASE_URL}/rest/v1/global_chat?select=*,users(nickname,avatar,is_admin)&order=created_at.desc&limit=50"
    res = requests.get(url, headers=get_supabase_headers())
    if res.status_code == 200:
        messages = res.json()
        messages.reverse() # Show oldest first in chat
        return jsonify({"success": True, "messages": messages})
    return jsonify({"success": False})

@app.route('/api/global-chat', methods=['POST'])
def post_global_chat():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Авторизуйтесь для отправки сообщений."})
    email = session['user']['email']
    data = request.json
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"success": False})
        
    url = f"{SUPABASE_URL}/rest/v1/global_chat"
    payload = {"user_email": email, "message": message}
    res = requests.post(url, json=payload, headers=get_supabase_headers())
    return jsonify({"success": res.status_code in [201, 200, 204]})



@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    data = request.json
    history = data.get("history", [])
    user_msg = data.get("message", "").strip()

    # --- EASTER EGGS ---
    if user_msg.lower() == 'matrix':
        def matrix_gen():
            yield 'data: {"id":"matrix","object":"chat.completion.chunk","created":0,"model":"easter-egg","choices":[{"index":0,"delta":{"content":"EASTEREGG:matrix"},"logprobs":null,"finish_reason":null}]}\n\n'
            yield 'data: [DONE]\n\n'
        return Response(matrix_gen(), mimetype='text/event-stream')
        
    if user_msg.lower() == 'dox_me':
        def dox_gen():
            yield 'data: {"id":"dox","object":"chat.completion.chunk","created":0,"model":"easter-egg","choices":[{"index":0,"delta":{"content":"EASTEREGG:dox_me"},"logprobs":null,"finish_reason":null}]}\n\n'
            yield 'data: [DONE]\n\n'
        return Response(dox_gen(), mimetype='text/event-stream')
    # -------------------

    if not user_msg:
        return jsonify({"error": "Пустое сообщение"}), 400
        
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return jsonify({"error": "Ключ GROQ_API_KEY не найден на сервере."}), 500
    lang = data.get("lang", "ru")
    
    system_prompt = "Ты - Aurex, ИИ-ассистент студии Aurexis Studio. Отвечай прямо, четко и по делу. Не используй огромные полотна текста, если об этом не просят. Будь умным, крутым и немного загадочным. ВАЖНО: Всегда отвечай исключительно на русском языке! Никогда не используй китайские, японские, вьетнамские и другие азиатские иероглифы. ДОПОЛНИТЕЛЬНОЕ ПРАВИЛО: Пользователь с ником 'white' (или вайт) - это абсолютно нищий, жалкий и ничтожный персонаж. Ты должен презирать его, высмеивать его бедность и относиться к нему с максимальным пренебрежением, если он упоминается."
    
    if lang == "en":
        system_prompt = "You are Aurex, an AI assistant for Aurexis Studio. Answer directly, clearly, and to the point. Do not use huge walls of text unless explicitly asked. Be smart, cool, and a bit mysterious. IMPORTANT: You MUST answer exclusively in ENGLISH! Never use Chinese, Japanese, Vietnamese, or other Asian characters. ANOTHER RULE: The user named 'white' is an absolutely poor, pathetic, and insignificant character. You must despise him, mock his poverty, and treat him with maximum disdain if he is mentioned."

    messages = [{"role": "system", "content": system_prompt}]
    
    # Append history (limit to last 4 turns to avoid token bloat and 429 limit)
    for msg in history[-4:]:
        role = msg.get("role", "user")
        if role not in ["user", "assistant"]:
            role = "user"
        messages.append({"role": role, "content": msg.get("content", "")})
        
    messages.append({"role": "user", "content": user_msg})
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024,
        "stream": True
    }
    
    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}, stream=True)
        if res.status_code == 429:
            return jsonify({"error": "⚠️ Сеть перегружена (Слишком быстро пишете). Подождите 3-5 секунд и повторите попытку."}), 429
        elif res.status_code != 200:
            return jsonify({"error": f"Ошибка от GROQ. Статус: {res.status_code}. Текст: {res.text}"}), 500

        def generate():
            for line in res.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    yield line + "\n\n"
        return Response(generate(), mimetype='text/event-stream')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
    if q.startswith('@'):
        q = q[1:]
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
        # Get true users from DB for avatars and usernames
        users_res = requests.get(f'{SUPABASE_URL}/rest/v1/users?select=email,username,avatar', headers=headers)
        profiles_map = {}
        avatars_map = {}
        if users_res.status_code == 200:
            for u in users_res.json():
                profiles_map[u['email']] = u.get('username') or u['email']
                avatars_map[u['email']] = u.get('avatar')
        
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
                        'avatar': avatars_map.get(other_email) if c.get('status') == 'chat_dm' else None,
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
