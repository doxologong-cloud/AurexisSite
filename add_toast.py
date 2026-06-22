import os

css_toast = """
/* CUSTOM TOAST NOTIFICATION */
#custom-toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 99999999;
    display: flex;
    flex-direction: column;
    gap: 10px;
    pointer-events: none;
}

.custom-toast {
    background: rgba(10, 10, 10, 0.95);
    border-left: 4px solid var(--neon-primary);
    color: #fff;
    padding: 15px 20px;
    border-radius: 8px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    max-width: 350px;
    pointer-events: auto;
    animation: toast-slide-in 0.3s ease forwards;
    display: flex;
    align-items: center;
    gap: 12px;
}

.custom-toast.error {
    border-left-color: #ff0033;
}
.custom-toast.success {
    border-left-color: #00ffaa;
}

.custom-toast a {
    color: var(--neon-primary);
    text-decoration: underline;
    cursor: pointer;
    font-weight: bold;
}
.custom-toast.error a {
    color: #ff4444;
}

@keyframes toast-slide-in {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes toast-slide-out {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
}
"""

with open('static/style.css', 'a', encoding='utf-8') as f:
    f.write(css_toast)

js_toast = """
// CUSTOM TOAST SYSTEM
function showToast(htmlMsg, type='info') {
    let container = document.getElementById('custom-toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'custom-toast-container';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `custom-toast ${type}`;
    
    let icon = '🔔';
    if(type === 'error') icon = '⚠️';
    if(type === 'success') icon = '✅';
    
    toast.innerHTML = `<span style="font-size:18px">${icon}</span> <div>${htmlMsg}</div>`;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'toast-slide-out 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// Function to switch tab manually from links
window.switchAuthTab = function(tabName) {
    window.location.hash = '#account';
    setTimeout(() => {
        const authTabs = document.querySelectorAll('.auth-tab');
        authTabs.forEach(t => t.classList.remove('active'));
        const targetTab = document.querySelector(`.auth-tab[data-tab="${tabName}"]`);
        if(targetTab) targetTab.classList.add('active');
        
        // Hide/show forms
        const authForms = document.querySelectorAll('.auth-form');
        authForms.forEach(f => f.classList.remove('active'));
        const targetForm = document.getElementById(`${tabName}-form`);
        if(targetForm) targetForm.classList.add('active');
    }, 100);
};
"""

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the alert in sendGlobalChat
# The alert looks like: alert('Пожалуйста, авторизуйтесь (вкладка Вход / Регистрация) чтобы писать в чат!');
# But let's just find "alert" inside sendGlobalChat.
import re
text = re.sub(
    r"alert\(['\"].*?\(.*?Вход \/ Регистрация\).*?['\"]\);", 
    "showToast('Вы не <a onclick=\"switchAuthTab(\\'login\\')\">авторизованы</a> или не <a onclick=\"switchAuthTab(\\'register\\')\">зарегистрированы</a>. Пожалуйста, войдите в аккаунт, чтобы писать в чат!', 'error');", 
    text
)

text = js_toast + "\n\n" + text

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Toast system added successfully.")
