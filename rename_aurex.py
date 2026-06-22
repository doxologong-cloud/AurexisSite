import re

# 1. Update server.py system prompt
with open('server.py', 'r', encoding='utf-8') as f:
    server_text = f.read()

old_prompt_match = re.search(r'system_prompt\s*=\s*".*?"', server_text)
if old_prompt_match:
    new_prompt = 'system_prompt = "Ты - Aurex (Аурекс), нейро-ассистент мужского пола студии Aurexis Studio. Ты общаешься с клиентами вежливо, профессионально и даешь очень развернутые, глубокие и объемные ответы. Ты помогаешь с ботами и разработкой. Забудь про токсичность и дерзость, будь доброжелательным помощником."'
    server_text = server_text.replace(old_prompt_match.group(0), new_prompt)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(server_text)

# 2. Update script.js (name display)
with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

# Replace AUREXIS FLORA with AUREX in nameHTML
js_text = js_text.replace('<span class="flora-name">AUREXIS FLORA</span>', '<span class="flora-name">AUREX</span>')
# Replace the CSS class flora-name? Keep it or change it, keeping it is fine, just replacing the text.
js_text = js_text.replace('flora-msg', 'aurex-msg') # Wait, maybe just replace FLORA with Aurex
with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js_text)

# 3. Update index.html (placeholder and headers)
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

html_text = html_text.replace('FLORA OS v2.0', 'AUREX OS v2.0')
html_text = html_text.replace('Напиши сообщение FLORA...', 'Напиши сообщение Aurex...')
html_text = html_text.replace('AUREXIS FLORA', 'AUREX')
# Some other places might have FLORA
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_text)

print("Updated AI persona to Aurex")
