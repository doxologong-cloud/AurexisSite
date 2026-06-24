import os
import re

base_dir = r"C:\Users\user\Desktop\сайт"
index_path = os.path.join(base_dir, "templates", "index.html")
vault_path = os.path.join(base_dir, "templates", "vault.html")
server_path = os.path.join(base_dir, "server.py")

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Create vault.html
# Duplicate index.html, but remove fake-front and login logic, and make secret-vault display: flex
vault_html = html
vault_html = re.sub(r'<!-- Фейковый фасад -->.*?</div>\s*</div>', '', vault_html, flags=re.DOTALL) # Need to be careful here
# Let's use string manipulation for vault.html
# Remove fake-front
fake_front_start = vault_html.find('<!-- Фейковый фасад -->')
fake_front_end = vault_html.find('<!-- Dynamic Canvas Background -->')
if fake_front_start != -1 and fake_front_end != -1:
    vault_html = vault_html[:fake_front_start] + vault_html[fake_front_end:]

# Make UI Overlay visible immediately (it was pointer-events: none, wait)
# Remove the key-sequence logic
vault_html = re.sub(r'// --- LOGIN LOGIC ---.*?function unlockVault\(\) \{.*?\}', '', vault_html, flags=re.DOTALL)
# It's actually safer to just write a focused regex for index.html login logic rewrite.

# Let's prepare a clean vault.html
vault_html = vault_html.replace('style="display: none;" id="secret-vault"', 'id="secret-vault"')
vault_html = vault_html.replace("const vault = document.getElementById('secret-vault');", "")
with open(vault_path, 'w', encoding='utf-8') as f:
    f.write(vault_html)

# 2. Rewrite index.html
# index.html should ONLY contain the head, the fake front, and the login script.
index_clean = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Aurexis Studio | Наши Боты</title>
    <style>
        body, html { margin: 0; padding: 0; height: 100%; background: #000; overflow: hidden; }
    </style>
</head>
<body>
    <!-- Фейковый фасад -->
    <div id="fake-front" style="display: flex; justify-content: center; align-items: center; height: 100vh; width: 100vw; background: #000; color: #ff0000; font-family: 'Space Grotesk', sans-serif; font-size: 3rem; text-shadow: 0 0 20px #ff0000; position: fixed; top: 0; left: 0; z-index: 9999; transition: opacity 1s, filter 1s;">
        (Ведутся РАБОТЫ)
    </div>

    <script>
        let keySequence = "";
        const secretCode = "3030";

        document.addEventListener('keydown', function(e) {
            keySequence += e.key.toLowerCase();
            if (keySequence.length > secretCode.length) {
                keySequence = keySequence.substring(1, keySequence.length);
            }
            if (keySequence === secretCode) {
                unlockVault();
            }
        });

        function unlockVault() {
            const fakeFront = document.getElementById('fake-front');
            fakeFront.style.filter = "blur(10px) hue-rotate(90deg)";
            fakeFront.style.transform = "scale(1.1)";
            
            // Authenticate with server
            fetch('/api/auth', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: secretCode })
            })
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    window.location.href = '/vault';
                } else {
                    alert('Access Denied');
                    fakeFront.style.filter = "none";
                    fakeFront.style.transform = "scale(1)";
                }
            });
        }
    </script>
</body>
</html>
"""
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index_clean)

# 3. Update server.py
with open(server_path, 'r', encoding='utf-8') as f:
    server_code = f.read()

new_routes = """
@app.route('/api/auth', methods=['POST'])
def api_auth():
    data = request.json
    if data and data.get('code') == '3030':
        session['authenticated'] = True
        return jsonify({"success": True})
    return jsonify({"success": False}), 403

@app.route('/vault')
def vault():
    if not session.get('authenticated'):
        return "Access Denied. Nice try F12 hacker.", 403
    return render_template('vault.html')
"""

if "@app.route('/api/auth')" not in server_code:
    server_code = server_code.replace("if __name__ == '__main__':", new_routes + "\nif __name__ == '__main__':")

# Secure the console route as well
console_route_old = """@app.route('/console')
def console():
    return render_template('console.html')"""

console_route_new = """@app.route('/console')
def console():
    if not session.get('authenticated'):
        return "Access Denied. Nice try F12 hacker.", 403
    return render_template('console.html')"""

server_code = server_code.replace(console_route_old, console_route_new)

with open(server_path, 'w', encoding='utf-8') as f:
    f.write(server_code)

print("Server-side auth implemented successfully.")
