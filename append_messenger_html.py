import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add to navbar
nav_link = '<a href="#messenger" class="nav-feed-link">Лента 💬</a>'
if 'Лента 💬' not in text:
    text = text.replace('<a href="#builder" class="nav-ai-link">Нейро-Ассистент 🧠</a>', '<a href="#builder" class="nav-ai-link">Нейро-Ассистент 🧠</a>\n            ' + nav_link)

# Add Messenger view
messenger_html = """
        <!-- Messenger View -->
        <div id="view-messenger" class="view" style="display: none;">
            <div class="messenger-container">
                <div class="messenger-sidebar">
                    <div class="messenger-header">
                        <h2>Лента</h2>
                        <button id="new-chat-btn" class="glow-btn small-btn">Новый чат</button>
                    </div>
                    <div class="chats-list" id="chats-list">
                        <!-- Chats will be populated here -->
                        <div style="text-align: center; color: #888; margin-top: 20px;">Загрузка чатов...</div>
                    </div>
                </div>
                
                <div class="messenger-main" id="messenger-main">
                    <div class="no-chat-selected" id="no-chat-selected">
                        <p>Выберите чат или создайте новый</p>
                    </div>
                    
                    <div class="active-chat" id="active-chat" style="display: none;">
                        <div class="chat-header">
                            <h3 id="active-chat-name">Имя Чата</h3>
                            <span id="active-chat-status">В сети</span>
                        </div>
                        <div class="chat-messages" id="active-chat-messages">
                            <!-- Messages -->
                        </div>
                        <div class="chat-input-area">
                            <button id="stickers-btn" class="icon-btn">😊</button>
                            <input type="text" id="messenger-input" placeholder="Напишите сообщение..." autocomplete="off">
                            <button id="messenger-send-btn" class="icon-btn">➤</button>
                        </div>
                        
                        <div class="stickers-panel" id="stickers-panel" style="display: none;">
                            <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f60e/512.gif" class="sticker-item" alt="😎">
                            <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f92f/512.gif" class="sticker-item" alt="🤯">
                            <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f680/512.gif" class="sticker-item" alt="🚀">
                            <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f525/512.gif" class="sticker-item" alt="🔥">
                            <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f47d/512.gif" class="sticker-item" alt="👽">
                            <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f916/512.gif" class="sticker-item" alt="🤖">
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- New Chat Modal -->
            <div id="new-chat-modal" class="modal" style="display: none; align-items: center; justify-content: center; position: fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index:1000;">
                <div class="modal-content" style="background:var(--bg-card); padding:30px; border-radius:15px; border:1px solid rgba(255,255,255,0.1); width: 400px; text-align:center;">
                    <h3>Создать новый чат</h3>
                    <div style="margin: 20px 0;">
                        <button id="tab-dm" class="glow-btn" style="margin-right:10px;">Личный чат</button>
                        <button id="tab-group" class="glow-btn" style="opacity:0.5;">Группа</button>
                    </div>
                    
                    <div id="dm-form">
                        <input type="email" id="dm-email" placeholder="Email пользователя" class="chat-input" style="width:100%; padding:10px; margin-bottom:15px; background:rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.2); color:white; border-radius:5px;">
                    </div>
                    
                    <div id="group-form" style="display:none;">
                        <input type="text" id="group-name" placeholder="Название группы" class="chat-input" style="width:100%; padding:10px; margin-bottom:15px; background:rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.2); color:white; border-radius:5px;">
                        <input type="text" id="group-emails" placeholder="Email участников (через запятую)" class="chat-input" style="width:100%; padding:10px; margin-bottom:15px; background:rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.2); color:white; border-radius:5px;">
                    </div>
                    
                    <button id="create-chat-submit" class="glow-btn" style="width:100%;">Создать</button>
                    <button id="close-chat-modal" class="glow-btn" style="width:100%; margin-top:10px; background:rgba(255,0,0,0.2);">Отмена</button>
                </div>
            </div>
        </div>
"""

if 'id="view-messenger"' not in text:
    text = text.replace('<!-- End of Main Content -->', messenger_html + '\n<!-- End of Main Content -->')
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added Messenger view to HTML")
else:
    print("Messenger view already exists")
