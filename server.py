from flask import Flask, render_template, request, jsonify, session
import sqlite3
import requests
import random
import os
import hashlib
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super-secret-key-12345")

# Database initialization
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Temporary store for verification codes
verification_codes = {}

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

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    
    # Check if user already exists
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email=?", (email,))
    if c.fetchone():
        conn.close()
        return jsonify({"success": False, "message": "Эта почта уже зарегистрирована."})
    conn.close()

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
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (nickname, email, password) VALUES (?, ?, ?)",
                  (user_data['nickname'], email, user_data['password']))
        conn.commit()
        conn.close()
        
        del verification_codes[email]
        session['user'] = {"nickname": user_data['nickname'], "email": email}
        return jsonify({"success": True, "user": session['user']})
    
    return jsonify({"success": False, "message": "Неверный код."})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = hashlib.sha256(data.get('password').encode()).hexdigest()
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT nickname, email FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()
    
    if user:
        session['user'] = {"nickname": user[0], "email": user[1]}
        return jsonify({"success": True, "user": session['user']})
    return jsonify({"success": False, "message": "Неверная почта или пароль."})

@app.route('/api/me', methods=['GET'])
def me():
    if 'user' in session:
        return jsonify({"success": True, "user": session['user']})
    return jsonify({"success": False})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
