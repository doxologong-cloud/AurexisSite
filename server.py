from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = os.getenv("SECRET_KEY", "super-secret-key-3030")

DATA_FILE = 'telegram_profile.json'

def load_profile():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"name": "Неизвестный", "bio": "Я использую Telegram", "avatar": "/static/assets/default-avatar.png"}

def save_profile(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    password = data.get('password', '')
    if password == '3030':
        session['logged_in'] = True
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Неверный пароль"})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return jsonify({"success": True})

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/api/telegram', methods=['GET'])
def get_telegram():
    if not session.get('logged_in'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    return jsonify({"success": True, "profile": load_profile()})

@app.route('/api/telegram', methods=['POST'])
def update_telegram():
    if not session.get('logged_in'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    data = request.json
    profile = load_profile()
    if 'name' in data:
        profile['name'] = data['name']
    if 'bio' in data:
        profile['bio'] = data['bio']
    if 'avatar' in data:
        profile['avatar'] = data['avatar']
        
    save_profile(profile)
    return jsonify({"success": True, "profile": profile})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
