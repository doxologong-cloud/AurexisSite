import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add stop button in HTML
if 'ai-stop-btn' not in text:
    stop_btn_html = """
                        <button id="ai-stop-btn" style="display: none; background: #ff0033;">
                            <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
                                <rect x="6" y="6" width="12" height="12"></rect>
                            </svg>
                        </button>"""
    text = text.replace('</button>\n                    </div>', '</button>' + stop_btn_html + '\n                    </div>')
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(text)

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

# Replace sendToAI logic
old_send_logic_start = js_text.find('async function sendToAI() {')
if old_send_logic_start != -1:
    old_send_logic_end = js_text.find('// Load user profile', old_send_logic_start)
    if old_send_logic_end != -1:
        # We also need to add global history variable
        new_js = """let aiChatHistory = [];
    let aiAbortController = null;
    const aiStopBtn = document.getElementById('ai-stop-btn');
    if(aiStopBtn) {
        aiStopBtn.addEventListener('click', () => {
            if(aiAbortController) {
                aiAbortController.abort();
            }
        });
    }

    async function sendToAI() {
        if(!aiInput || !aiInput.value.trim()) return;
        const text = aiInput.value.trim();
        aiInput.value = '';
        
        // Add to history
        aiChatHistory.push({role: 'user', content: text});
        addMessageToTerminal('user', text);
        
        const contentBox = addMessageToTerminal('ai', '<div class="typing-indicator"></div><div class="typing-indicator" style="animation-delay:0.2s"></div><div class="typing-indicator" style="animation-delay:0.4s"></div>');
        
        const sendBtn = document.getElementById('ai-send-btn');
        if(sendBtn) sendBtn.style.display = 'none';
        if(aiStopBtn) aiStopBtn.style.display = 'block';
        
        aiAbortController = new AbortController();
        
        try {
            const res = await fetch('/api/ai/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, history: aiChatHistory }),
                signal: aiAbortController.signal
            });
            
            contentBox.innerHTML = '';
            
            if (res.ok && res.body) {
                const reader = res.body.getReader();
                const decoder = new TextDecoder('utf-8');
                let fullReply = '';
                
                while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;
                    
                    const chunk = decoder.decode(value, {stream: true});
                    fullReply += chunk;
                    contentBox.textContent = fullReply;
                    aiChatBox.scrollTop = aiChatBox.scrollHeight;
                }
                aiChatHistory.push({role: 'assistant', content: fullReply});
            } else {
                contentBox.textContent = 'Ошибка подключения к серверу.';
            }
        } catch (e) {
            if(e.name === 'AbortError') {
                // If user aborted, we just save what was generated so far
                const partialReply = contentBox.textContent;
                aiChatHistory.push({role: 'assistant', content: partialReply});
            } else {
                contentBox.textContent = 'Ошибка сети.';
            }
        } finally {
            if(sendBtn) sendBtn.style.display = 'block';
            if(aiStopBtn) aiStopBtn.style.display = 'none';
            aiAbortController = null;
        }
    }

    """
        js_text = js_text[:old_send_logic_start] + new_js + js_text[old_send_logic_end:]

        with open('static/script.js', 'w', encoding='utf-8') as f:
            f.write(js_text)
            
print("Frontend updated for AI streaming.")
