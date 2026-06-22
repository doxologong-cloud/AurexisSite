import re

with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Protect /api/register
old_reg = """def register():
    data = request.json
    email = data.get('email')
    
    # Check if user already exists"""

new_reg = """def register():
    data = request.json
    email = data.get('email', '').strip()
    nickname = data.get('nickname', '').strip()
    password = data.get('password', '')
    
    if not email or not nickname or not password:
        return jsonify({"success": False, "message": "Заполните все поля."})
        
    # Check if user already exists"""

if old_reg in text:
    text = text.replace(old_reg, new_reg)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Patched server.py successfully!")
else:
    print("Could not find old register code in server.py")
