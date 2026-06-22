import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

# Append ticks to message bubble
if "msgDiv.innerHTML = `<span class='msg-time'>" in js_text:
    js_text = js_text.replace(
        "msgDiv.innerHTML = `<span class='msg-time'>[${timeStr}]</span> <b>${sender}</b>: ${msg.text}`;",
        "msgDiv.innerHTML = `<span class='msg-time'>[${timeStr}]</span> <b>${sender}</b>: ${msg.text}` + (isMine ? ` <span style='color: var(--neon-color); font-size: 10px; margin-left: 5px;'>✔✔</span>` : '');"
    )

typing_js = """
// ==========================================
// TYPING INDICATOR & STATUSES
// ==========================================

function showTypingIndicator(username) {
    let indicator = document.getElementById('typing-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'typing-indicator';
        indicator.style.color = 'var(--neon-color)';
        indicator.style.fontStyle = 'italic';
        indicator.style.fontSize = '12px';
        indicator.style.padding = '5px 15px';
        indicator.style.animation = 'pulse 1s infinite alternate';
        
        const chatWindow = document.getElementById('chat-window');
        if (chatWindow) {
            chatWindow.parentNode.insertBefore(indicator, chatWindow.nextSibling);
        }
    }
    indicator.innerText = `${username} печатает...`;
    indicator.style.display = 'block';
    
    // Auto-hide after 3 seconds
    clearTimeout(window.typingTimeout);
    window.typingTimeout = setTimeout(() => {
        indicator.style.display = 'none';
    }, 3000);
}

// Hook into loadMessages to play receive sound
const originalLoadMessages = window.loadMessages;
if (typeof originalLoadMessages === 'function') {
    window.lastMessageCount = 0;
    window.loadMessages = async function() {
        await originalLoadMessages();
        const chatWindow = document.getElementById('chat-window');
        if (chatWindow && chatWindow.children.length > window.lastMessageCount) {
            if (window.lastMessageCount > 0) {
                // Only play sound if it's not the initial load
                // Check if the last message is NOT mine
                const lastMsg = chatWindow.lastChild;
                if (lastMsg && !lastMsg.classList.contains('my-message')) {
                    playSound('receive');
                }
            }
            window.lastMessageCount = chatWindow.children.length;
        }
    };
}
"""

if 'showTypingIndicator' not in js_text:
    js_text += "\n" + typing_js
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(js_text)
    print("Injected Ticks and Typing JS.")
else:
    print("Ticks and Typing JS already exists.")
