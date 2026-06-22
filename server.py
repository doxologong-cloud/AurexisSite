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
    email = data.get('email')
    
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
        
    url = f"{SUPABASE_URL}/rest/v1/reviews"
    payload = {"email": session['user']['email'], "rating": int(rating), "text": text}
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
    url = f"{SUPABASE_URL}/rest/v1/tickets?select=*,users(nickname,avatar)&order=created_at.desc"
    res = requests.get(url, headers=get_supabase_headers())
    if res.status_code == 200:
        return jsonify({"success": True, "tickets": res.json()})
    return jsonify({"success": False})

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
    if not user_msg:
        return jsonify({"error": "Пустое сообщение"}), 400
        
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return jsonify({"error": "Ключ GROQ_API_KEY не найден на сервере."}), 500
        
    system_prompt = "Ты - AUREXIS FLORA, нейро-ассистент студии Aurexis Studio. Ты общаешься с клиентами в терминале. Ты дерзкая, немного токсичная, но очень умная и полезная. Ты любишь сарказм. Отвечай кратко, как в терминале, без лишней воды."
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Append history (limit to last 10 turns to avoid token bloat)
    for msg in history[-10:]:
        role = msg.get("role", "user")
        if role not in ["user", "assistant"]:
            role = "user"
        messages.append({"role": role, "content": msg.get("content", "")})
        
    messages.append({"role": "user", "content": user_msg})
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024,
        "stream": True
    }
    
    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}, stream=True)
        if res.status_code != 200:
            return jsonify({"error": f"Ошибка от GROQ. Статус: {res.status_code}. Текст: {res.text}"}), 500

        def generate():
            for line in res.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str == '[DONE]':
                            break
                        try:
                            import json
                            data_json = json.loads(data_str)
                            delta = data_json['choices'][0]['delta']
                            if 'content' in delta:
                                yield delta['content']
                        except Exception as e:
                            pass
        return Response(generate(), mimetype='text/plain')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
