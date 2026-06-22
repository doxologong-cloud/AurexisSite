import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

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
        
        if(aiSendBtn) aiSendBtn.style.display = 'none';
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
            if(aiSendBtn) aiSendBtn.style.display = 'block';
            if(aiStopBtn) aiStopBtn.style.display = 'none';
            aiAbortController = null;
        }
    }

    if (aiSendBtn) {"""

# Replace old sendToAI implementation
js_text = re.sub(r'async function sendToAI\(\) \{[\s\S]*?if\s*\(\s*aiSendBtn\s*\)\s*\{', new_js, js_text)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Properly replaced sendToAI")
