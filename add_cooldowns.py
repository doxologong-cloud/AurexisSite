import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

# 1. Add cooldown for AI Chat
if 'let lastAIChatTime = 0;' not in js_text:
    js_text = js_text.replace('let isGenerating = false;', 'let isGenerating = false;\n    let lastAIChatTime = 0;')

old_ai_start = """async function sendToAI() {
        if(isGenerating) return;
        if(!aiInput || !aiInput.value.trim()) return;"""

new_ai_start = """async function sendToAI() {
        if(isGenerating) return;
        if(!aiInput || !aiInput.value.trim()) return;
        
        const now = Date.now();
        if (now - lastAIChatTime < 5000) {
            const timeLeft = Math.ceil((5000 - (now - lastAIChatTime)) / 1000);
            showToast(`Подождите ${timeLeft} сек. перед следующим сообщением.`, 'error');
            return;
        }
        lastAIChatTime = now;
"""
if old_ai_start in js_text:
    js_text = js_text.replace(old_ai_start, new_ai_start)


# 2. Add cooldown for Global Chat
if 'let lastGlobalChatTime = 0;' not in js_text:
    # Find sendGlobalChat
    global_chat_start = js_text.find('async function sendGlobalChat()')
    if global_chat_start != -1:
        js_text = js_text[:global_chat_start] + "let lastGlobalChatTime = 0;\n" + js_text[global_chat_start:]

old_global_start = """async function sendGlobalChat() {
    if(!window.currentUser) await loadUserProfile();
    if(!window.currentUser) {
        showToast"""

new_global_start = """async function sendGlobalChat() {
    if(!window.currentUser) await loadUserProfile();
    if(!window.currentUser) {
        showToast"""

# We need to insert the cooldown check after the auth check but before sending
old_global_send = """const text = chatInput.value.trim();
    if(!text) return;"""

new_global_send = """const text = chatInput.value.trim();
    if(!text) return;
    
    const now = Date.now();
    if (now - lastGlobalChatTime < 5000) {
        const timeLeft = Math.ceil((5000 - (now - lastGlobalChatTime)) / 1000);
        showToast(`Подождите ${timeLeft} сек. перед отправкой.`, 'error');
        return;
    }
    lastGlobalChatTime = now;"""

if old_global_send in js_text:
    js_text = js_text.replace(old_global_send, new_global_send)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Added 5-second cooldown to AI and Global chat.")
