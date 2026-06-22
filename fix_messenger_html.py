with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_header = '''                    <div class="messenger-header">
                        <h2>Лента</h2>
                        <button id="new-chat-btn" class="glow-btn small-btn">Новый чат</button>
                    </div>'''

new_header = '''                    <div class="messenger-header" style="flex-direction: column; gap: 10px; align-items: stretch; padding: 15px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h2 style="margin: 0;">Лента</h2>
                        </div>
                        <div style="position: relative;">
                            <input type="text" id="user-search-input" placeholder="Поиск юзернейма..." style="width: 100%; padding: 8px 12px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.3); color: white; box-sizing: border-box;">
                            <div id="search-results-container" style="display: none; position: absolute; top: 100%; left: 0; right: 0; background: rgba(15,15,20,0.95); border: 1px solid var(--neon-primary); border-radius: 10px; margin-top: 5px; max-height: 200px; overflow-y: auto; z-index: 100;">
                            </div>
                        </div>
                        <div class="messenger-tabs" style="display: flex; gap: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px;">
                            <span class="msgr-tab active" id="tab-chats" style="cursor: pointer; font-size: 0.9rem; color: var(--neon-primary);">Чаты</span>
                            <span class="msgr-tab" id="tab-contacts" style="cursor: pointer; font-size: 0.9rem; color: #888;">Контакты</span>
                        </div>
                    </div>'''

old_chat_header = '''                        <div class="chat-header">
                            <h3 id="active-chat-name">Имя Чата</h3>
                            <span id="active-chat-status">В сети</span>
                        </div>'''

new_chat_header = '''                        <div class="chat-header" style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h3 id="active-chat-name" style="margin: 0;">Имя Чата</h3>
                                <span id="active-chat-status" style="font-size: 0.8rem; color: var(--neon-primary);">В сети</span>
                            </div>
                            <button id="add-to-contacts-btn" class="glow-btn small-btn" style="display: none;">+ В контакты</button>
                        </div>'''

if 'id="user-search-input"' not in text:
    text = text.replace(old_header, new_header)
    text = text.replace(old_chat_header, new_chat_header)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed HTML for search and contacts.")
else:
    print("HTML already fixed.")
