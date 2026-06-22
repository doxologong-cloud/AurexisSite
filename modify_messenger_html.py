import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the New Chat button with Search Bar and Contacts Tab
old_sidebar_header = """<div class="messenger-sidebar-header">
                        <h3 style="margin: 0;">Чаты</h3>
                        <button id="new-chat-btn" class="glow-btn" style="padding: 5px 15px; font-size: 0.9rem;">+ Новый чат</button>
                    </div>"""

new_sidebar_header = """<div class="messenger-sidebar-header" style="flex-direction: column; gap: 10px; align-items: stretch;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3 style="margin: 0;">Чаты</h3>
                        </div>
                        <div style="position: relative;">
                            <input type="text" id="user-search-input" placeholder="Поиск по юзернейму..." style="width: 100%; padding: 8px 12px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.3); color: white; box-sizing: border-box;">
                            <div id="search-results-container" style="display: none; position: absolute; top: 100%; left: 0; right: 0; background: rgba(15,15,20,0.95); border: 1px solid var(--neon-primary); border-radius: 10px; margin-top: 5px; max-height: 200px; overflow-y: auto; z-index: 100;">
                                <!-- Search results go here -->
                            </div>
                        </div>
                        <div class="messenger-tabs" style="display: flex; gap: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px;">
                            <span class="msgr-tab active" id="tab-chats" style="cursor: pointer; font-size: 0.9rem; color: var(--neon-primary);">Чаты</span>
                            <span class="msgr-tab" id="tab-contacts" style="cursor: pointer; font-size: 0.9rem; color: #888;">Контакты</span>
                        </div>
                    </div>"""

if 'id="user-search-input"' not in text:
    text = text.replace(old_sidebar_header, new_sidebar_header)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Modified HTML for Search and Contacts")
else:
    print("HTML already modified.")
