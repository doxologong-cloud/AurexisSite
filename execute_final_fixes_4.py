import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix capitalization of ГЛАВНАЯ and О НАС properly
html = html.replace('ГЛАВНАЯ', 'Главная')
html = html.replace('О НАС', 'О нас')
html = html.replace('Нейро-Ассистент 🧠', 'Нейро-Ассистент <i class="fa-solid fa-brain"></i>')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)


with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 2. Fix ticket chat modal id typo
old_ticket_open = "document.getElementById('ticket-chat-modal').style.display = 'flex';"
new_ticket_open = "document.getElementById('ticket-modal').style.display = 'flex';"
if old_ticket_open in js:
    js = js.replace(old_ticket_open, new_ticket_open)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

with open('static/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 3. Fix messenger squished layout
old_messenger_css = """.messenger-container {
    display: flex;
    height: 80vh;"""

new_messenger_css = """.messenger-container {
    display: flex;
    width: 100%;
    height: 80vh;"""

if old_messenger_css in css:
    css = css.replace(old_messenger_css, new_messenger_css)
else:
    # Fallback if already modified
    pass

# Ensure active-chat takes full width too, just in case
old_active_chat = """.active-chat {
    flex: 1;
    display: flex;
    flex-direction: column;
}"""

new_active_chat = """.active-chat {
    flex: 1;
    display: flex;
    width: 100%;
    flex-direction: column;
}"""

if old_active_chat in css:
    css = css.replace(old_active_chat, new_active_chat)

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Fixes applied successfully!")
