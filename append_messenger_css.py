import re

with open('static/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

messenger_css = """
/* ================= MESSENGER ================= */
.messenger-container {
    display: flex;
    height: 80vh;
    background: rgba(10, 10, 15, 0.8);
    border: 1px solid rgba(0, 255, 136, 0.2);
    border-radius: 15px;
    overflow: hidden;
    margin-top: 20px;
    box-shadow: 0 0 20px rgba(0,0,0,0.5);
}

.messenger-sidebar {
    width: 30%;
    min-width: 250px;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    flex-direction: column;
    background: rgba(0, 0, 0, 0.4);
}

.messenger-header {
    padding: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.messenger-header h2 {
    margin: 0;
    font-size: 1.2rem;
    color: var(--neon-primary);
}

.chats-list {
    flex: 1;
    overflow-y: auto;
}

.chat-item {
    padding: 15px 20px;
    cursor: pointer;
    border-bottom: 1px solid rgba(255,255,255,0.02);
    transition: background 0.2s;
    display: flex;
    align-items: center;
    gap: 15px;
}

.chat-item:hover, .chat-item.active {
    background: rgba(0, 255, 136, 0.1);
}

.chat-item-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(45deg, var(--neon-primary), var(--neon-secondary));
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: black;
}

.chat-item-info {
    display: flex;
    flex-direction: column;
}

.chat-item-name {
    font-weight: 600;
    font-size: 1rem;
}

.chat-item-type {
    font-size: 0.8rem;
    color: #888;
}

.messenger-main {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: rgba(5, 5, 10, 0.6);
}

.no-chat-selected {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #555;
    font-size: 1.2rem;
}

.active-chat {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.chat-header {
    padding: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    background: rgba(0,0,0,0.3);
}

.chat-header h3 {
    margin: 0;
    color: white;
}

.chat-messages {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.chat-msg {
    max-width: 70%;
    padding: 10px 15px;
    border-radius: 15px;
    font-size: 0.95rem;
    line-height: 1.4;
    word-break: break-word;
}

.chat-msg.sent {
    align-self: flex-end;
    background: rgba(0, 255, 136, 0.2);
    border-bottom-right-radius: 5px;
    border: 1px solid rgba(0, 255, 136, 0.3);
}

.chat-msg.received {
    align-self: flex-start;
    background: rgba(255, 255, 255, 0.05);
    border-bottom-left-radius: 5px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.chat-msg-sender {
    font-size: 0.75rem;
    color: #888;
    margin-bottom: 3px;
    display: block;
}

.chat-msg-time {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.4);
    display: block;
    text-align: right;
    margin-top: 5px;
}

.chat-input-area {
    padding: 15px;
    background: rgba(0,0,0,0.5);
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    align-items: center;
    gap: 10px;
    position: relative;
}

#messenger-input {
    flex: 1;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: white;
    padding: 12px 20px;
    border-radius: 25px;
    outline: none;
    transition: 0.3s;
}

#messenger-input:focus {
    border-color: var(--neon-primary);
    background: rgba(0, 255, 136, 0.05);
}

.stickers-panel {
    position: absolute;
    bottom: 70px;
    left: 15px;
    background: var(--bg-card);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 15px;
    padding: 15px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    box-shadow: 0 -5px 20px rgba(0,0,0,0.5);
    z-index: 10;
}

.sticker-item {
    width: 50px;
    height: 50px;
    cursor: pointer;
    transition: transform 0.2s;
}

.sticker-item:hover {
    transform: scale(1.2);
}

.chat-msg-sticker {
    width: 100px;
    height: 100px;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

.chat-msg-sticker img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}
"""

if '/* ================= MESSENGER ================= */' not in text:
    with open('static/style.css', 'a', encoding='utf-8') as f:
        f.write('\n' + messenger_css)
    print("Added Messenger CSS")
else:
    print("Messenger CSS already exists")
