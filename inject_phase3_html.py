from bs4 import BeautifulSoup

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# 1. Add hacker terminal window
hacker_html = """
    <!-- Hacker Terminal -->
    <div id="view-hacker" class="window" style="border-color: #0f0; box-shadow: 0 0 20px rgba(0,255,0,0.3);">
        <div class="window-header" onmousedown="startDrag(event, 'view-hacker')" style="background: rgba(0,255,0,0.1); border-bottom: 1px solid #0f0;">
            <div class="window-title" style="color: #0f0;">AUREX_ROOT_TERMINAL</div>
            <div class="window-controls">
                <button class="window-btn btn-close" onclick="closeWindow('view-hacker')"></button>
            </div>
        </div>
        <div class="window-content" style="background: #000; color: #0f0; font-family: monospace; padding: 10px; font-size: 14px; overflow-y: auto;">
            <div id="hacker-output"></div>
            <div style="display: flex;">
                <span style="color: #0f0; margin-right: 5px;">root@aurexis:~#</span>
                <input type="text" id="hacker-input" style="background: transparent; border: none; color: #0f0; outline: none; flex: 1; font-family: monospace;">
            </div>
        </div>
    </div>
"""

# Append hacker terminal to main
main_tag = soup.find('main')
if main_tag and 'view-hacker' not in html:
    main_tag.append(BeautifulSoup(hacker_html, 'html.parser'))

# 2. Add buttons to messenger
chat_input_div = soup.find('div', class_='chat-input')
if chat_input_div:
    # Check if tools already exist
    if not chat_input_div.find('button', id='btn-voice'):
        voice_btn = soup.new_tag('button')
        voice_btn['id'] = 'btn-voice'
        voice_btn['style'] = 'background: transparent; border: 1px solid var(--neon-color); color: var(--neon-color); padding: 10px; border-radius: 5px; cursor: pointer; margin-right: 5px;'
        voice_btn['onclick'] = 'toggleVoiceRecord()'
        voice_btn.string = '🎤'
        
        screen_btn = soup.new_tag('button')
        screen_btn['id'] = 'btn-screen'
        screen_btn['style'] = 'background: transparent; border: 1px solid var(--neon-color); color: var(--neon-color); padding: 10px; border-radius: 5px; cursor: pointer; margin-right: 5px;'
        screen_btn['onclick'] = 'captureScreen()'
        screen_btn.string = '📸'
        
        # insert before the input field
        input_field = chat_input_div.find('input', id='message-input')
        if input_field:
            input_field.insert_before(voice_btn)
            input_field.insert_before(screen_btn)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Injected Phase 3 HTML")
