import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

# Fix 1: Add isGenerating flag to prevent Enter spamming
if 'let isGenerating = false;' not in js_text:
    js_text = js_text.replace('let aiAbortController = null;', 'let aiAbortController = null;\n    let isGenerating = false;')

# Update the beginning of sendToAI
old_start = """async function sendToAI() {
        if(!aiInput || !aiInput.value.trim()) return;"""
new_start = """async function sendToAI() {
        if(isGenerating) return;
        if(!aiInput || !aiInput.value.trim()) return;
        isGenerating = true;"""
if old_start in js_text:
    js_text = js_text.replace(old_start, new_start)

# Update the finally block to reset isGenerating
old_finally = """} finally {
            if(aiSendBtn) aiSendBtn.style.display = 'block';"""
new_finally = """} finally {
            isGenerating = false;
            if(aiSendBtn) aiSendBtn.style.display = 'block';"""
if old_finally in js_text:
    js_text = js_text.replace(old_finally, new_finally)

# Fix 2: Better error reporting instead of hardcoded 'Ошибка подключения к серверу.'
old_err_handling = """} else {
                contentBox.textContent = 'Ошибка подключения к серверу.';
            }"""
new_err_handling = """} else {
                try {
                    const errData = await res.json();
                    contentBox.innerHTML = `<span style="color:#ff4444">Ошибка: ${errData.error || 'Сбой сервера'}</span>`;
                } catch(e) {
                    contentBox.innerHTML = '<span style="color:#ff4444">Ошибка подключения к серверу.</span>';
                }
            }"""
if old_err_handling in js_text:
    js_text = js_text.replace(old_err_handling, new_err_handling)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Fixed spamming bug and improved error messages")
