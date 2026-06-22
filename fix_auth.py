import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add ID to google container
text = text.replace('<div style="margin-top: 20px; text-align: center;">\n                        <div id="g_id_onload"', '<div id="google-auth-container" style="margin-top: 20px; text-align: center;">\n                        <div id="g_id_onload"')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

# Update switchAuthTab to handle forms and google auth correctly
js_new = """window.switchAuthTab = function(tabName) {
    window.location.hash = '#account';
    setTimeout(() => {
        const authTabs = document.querySelectorAll('.auth-tab');
        authTabs.forEach(t => t.classList.remove('active'));
        const targetTab = document.querySelector(`.auth-tab[data-tab="${tabName}"]`);
        if(targetTab) targetTab.classList.add('active');
        
        // Hide/show forms properly using style.display
        const authForms = document.querySelectorAll('.auth-form');
        authForms.forEach(f => f.style.display = 'none');
        const targetForm = document.getElementById(`${tabName}-form`);
        if(targetForm) {
            targetForm.style.display = 'flex';
        }
        
        // Hide google button for verification forms
        const googleBtn = document.getElementById('google-auth-container');
        if(googleBtn) {
            if(tabName === 'login' || tabName === 'register') {
                googleBtn.style.display = 'block';
            } else {
                googleBtn.style.display = 'none';
            }
        }
    }, 100);
};"""

# Replace the old switchAuthTab
js_text = re.sub(r'window\.switchAuthTab = function\(tabName\) \{.*?\};\n', js_new + '\n', js_text, flags=re.DOTALL)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Fixed auth tab switching and google button visibility")
