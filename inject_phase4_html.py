from bs4 import BeautifulSoup

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# 1. Add manifest
head = soup.find('head')
if head and not soup.find('link', href='/static/manifest.json'):
    manifest_link = soup.new_tag('link')
    manifest_link['rel'] = 'manifest'
    manifest_link['href'] = '/static/manifest.json'
    head.append(manifest_link)

# 2. Add Code Editor Window
editor_html = """
    <!-- Code Editor Window -->
    <div id="view-editor" class="window" style="width: 600px; height: 400px; border-color: #00a8ff; box-shadow: 0 0 20px rgba(0, 168, 255, 0.3);">
        <div class="window-header" onmousedown="startDrag(event, 'view-editor')" style="background: rgba(0, 168, 255, 0.1); border-bottom: 1px solid #00a8ff;">
            <div class="window-title" style="color: #00a8ff;">Live-Code Editor</div>
            <div class="window-controls">
                <button class="window-btn btn-min" onclick="minimizeWindow('view-editor')"></button>
                <button class="window-btn btn-max" onclick="maximizeWindow('view-editor')"></button>
                <button class="window-btn btn-close" onclick="closeWindow('view-editor')"></button>
            </div>
        </div>
        <div class="window-content" style="display: flex; flex-direction: column;">
            <div style="background: #111; border-bottom: 1px solid #333; padding: 5px;">
                <button onclick="runCode()" style="background: #2ed573; color: #000; border: none; padding: 5px 15px; border-radius: 3px; cursor: pointer; font-weight: bold;">▶ Run</button>
            </div>
            <textarea id="code-textarea" style="flex: 1; background: #000; color: #00a8ff; font-family: monospace; border: none; padding: 10px; outline: none; resize: none;" spellcheck="false"># Пиши код бота здесь...
def on_message(msg):
    if msg == 'ping':
        return 'pong'</textarea>
            <div id="code-output" style="height: 100px; background: #111; color: #fff; padding: 10px; font-family: monospace; overflow-y: auto; border-top: 1px solid #333;">Output will appear here...</div>
        </div>
    </div>
"""

main_tag = soup.find('main')
if main_tag and 'view-editor' not in html:
    main_tag.append(BeautifulSoup(editor_html, 'html.parser'))
    
# Add nav button for editor
nav_links = soup.find('div', class_='nav-links')
if nav_links and 'Редактор' not in html:
    a = soup.new_tag('a')
    a['href'] = '#'
    a['onclick'] = "switchView('view-editor')"
    a['class'] = 'nav-link'
    a.string = 'Редактор'
    nav_links.append(a)

# 3. Add Call button to messenger chat
chat_header = soup.find('div', class_='chat-header')
if chat_header and not chat_header.find('button', id='btn-call'):
    call_btn = soup.new_tag('button')
    call_btn['id'] = 'btn-call'
    call_btn['onclick'] = 'startCall()'
    call_btn['style'] = 'background: transparent; border: none; color: var(--neon-color); font-size: 20px; cursor: pointer; margin-left: 10px;'
    call_btn.string = '📞'
    
    # Also add Lock icon for E2EE
    lock_span = soup.new_tag('span')
    lock_span['id'] = 'e2ee-lock'
    lock_span['style'] = 'color: #2ed573; margin-left: 10px; font-size: 14px; cursor: help;'
    lock_span['title'] = 'Чат защищен сквозным шифрованием (E2EE)'
    lock_span.string = '🔐'
    
    chat_header.append(lock_span)
    chat_header.append(call_btn)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Injected Phase 4 HTML")
