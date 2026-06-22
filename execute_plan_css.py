import re

with open('static/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Update chat bubbles
old_chat_msg = """.chat-msg {
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
}"""

new_chat_msg = """.chat-msg {
    max-width: 75%;
    padding: 10px 16px;
    border-radius: 18px;
    font-size: 0.95rem;
    line-height: 1.45;
    word-break: break-word;
    position: relative;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.chat-msg.sent {
    align-self: flex-end;
    background: var(--neon-primary);
    color: #000;
    border-bottom-right-radius: 4px;
}

.chat-msg.received {
    align-self: flex-start;
    background: rgba(255, 255, 255, 0.1);
    color: #fff;
    border-bottom-left-radius: 4px;
}

.chat-msg.sent .chat-msg-sender,
.chat-msg.sent .chat-msg-time {
    color: rgba(0,0,0,0.6);
}

.chat-msg.received .chat-msg-time {
    color: rgba(255,255,255,0.5);
}"""

if old_chat_msg in css:
    css = css.replace(old_chat_msg, new_chat_msg)
    print("Replaced chat bubbles")

# 2. Update feed avatars
old_chat_avatar = """.chat-item-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(255,255,255,0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 1.2rem;
    color: var(--neon-primary);
}"""

new_chat_avatar = """.chat-item-avatar {
    width: 45px;
    height: 45px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--neon-primary), var(--neon-purple));
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 1.3rem;
    color: #000;
    box-shadow: 0 0 10px rgba(229, 179, 34, 0.4);
    text-transform: uppercase;
}"""

if old_chat_avatar in css:
    css = css.replace(old_chat_avatar, new_chat_avatar)
    print("Replaced chat item avatars")

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
