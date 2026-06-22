import re

# 1. Update style.css for status dots
with open('static/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Make base dot no animation by default, or 5s for green
css = css.replace('.status-dot {\n    width: 10px;', '.status-dot {\n    width: 10px;')
# Find status-green animation
if '.status-green .status-dot {' in css:
    css = css.replace('.status-green .status-dot {\n    background: var(--neon-green);\n    box-shadow: 0 0 8px var(--neon-green);\n}',
                      '.status-green .status-dot {\n    background: var(--neon-green);\n    box-shadow: 0 0 8px var(--neon-green);\n    animation: blink 5s infinite;\n}')

# Add offline status class
if '.status-offline' not in css:
    css += '\n\n.status-offline .status-dot {\n    background: #5a3434;\n    box-shadow: none;\n    animation: none;\n}\n.status-offline {\n    color: #666;\n}\n'

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("Updated CSS")

# 2. Update AI prompt in server.py
with open('server.py', 'r', encoding='utf-8') as f:
    server = f.read()

old_prompt = 'system_prompt = "Ты - Aurex, ИИ-ассистент студии Aurexis Studio. Отвечай прямо, четко и по делу. Не используй огромное количество текста, если об этом не просят напрямую. Будь умным, классным, и немного загадочным."'
new_prompt = 'system_prompt = "Ты - Aurex, ИИ-ассистент студии Aurexis Studio. Отвечай прямо, четко и по делу. Не используй огромное количество текста, если об этом не просят напрямую. Будь умным, классным, и немного загадочным. ВАЖНО: Всегда отвечай исключительно на русском языке! Никогда не используй китайские, японские, вьетнамские или другие азиатские иероглифы."'

if old_prompt in server:
    server = server.replace(old_prompt, new_prompt)
else:
    # try regex
    server = re.sub(r'system_prompt = ".*?"', new_prompt, server)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(server)
print("Updated server.py")

# 3. Add short Preloader in index.html & script.js
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make welcome-screen visible again initially
if '<div id="welcome-screen" style="display: none;">' in html:
    html = html.replace('<div id="welcome-screen" style="display: none;">', '<div id="welcome-screen">')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html")

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update JS preloader logic to 1 second
old_preloader = """    // Instant load
    if (welcomeScreen) welcomeScreen.style.display = 'none';
    document.querySelector('.hero')?.classList.add('show');
    initScrollAnimations();"""

new_preloader = """    // Fast preloader
    if (welcomeScreen) {
        setTimeout(() => {
            welcomeScreen.style.opacity = '0';
            setTimeout(() => {
                welcomeScreen.style.display = 'none';
                document.querySelector('.hero')?.classList.add('show');
                initScrollAnimations();
            }, 300); // fade out duration
        }, 1000); // 1 second fast glitch show
    } else {
        document.querySelector('.hero')?.classList.add('show');
        initScrollAnimations();
    }"""

if old_preloader in js:
    js = js.replace(old_preloader, new_preloader)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated script.js")
