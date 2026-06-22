import re

# 1. Update index.html to wrap the Google login cleanly
with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# We need to find the <div style="margin-top: 20px; text-align: center;"> that contains g_id_onload
# and change it to <div id="google-auth-container" style="margin-top: 20px; text-align: center;">
text = re.sub(
    r'<div style="margin-top: 20px; text-align: center;">\s*<div id="g_id_onload"',
    r'<div id="google-auth-container" style="margin-top: 20px; text-align: center;">\n<div id="g_id_onload"',
    text
)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

# 2. Update script.js to replace 'auth-social-wrap' with 'google-auth-container'
with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

js_text = js_text.replace("'auth-social-wrap'", "'google-auth-container'")
js_text = js_text.replace("authSocialWrap", "googleAuthContainer")

# Also, in the native tab click listener, hide/show the google auth container properly
# Let's find the native tab listener
native_listener = """authTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            if (tab.classList.contains('active')) return;
            
            authTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Reset forms and errors
            document.querySelectorAll('.auth-error').forEach(el => el.textContent = '');
            verifyForm.style.display = 'none';

            if (tab.dataset.tab === 'login') {
                loginForm.style.display = 'flex';
                registerForm.style.display = 'none';
            } else {
                loginForm.style.display = 'none';
                registerForm.style.display = 'flex';
            }
            
            if (googleAuthContainer) {
                googleAuthContainer.style.display = 'block';
            }
        });
    });"""

# We'll use regex to replace the old authTabs listener if needed, or just insert the visibility toggle
# Actually, replacing all `authSocialWrap` to `googleAuthContainer` might be enough to fix the crash.
# But let's make sure the googleAuthContainer is shown when clicking the tabs.

def inject_google_show(match):
    return match.group(0) + "\n            if (googleAuthContainer) googleAuthContainer.style.display = 'block';"

js_text = re.sub(r'registerForm\.style\.display = \'flex\';\s*\}', inject_google_show, js_text, count=1)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Fixed the crash and google button wrapping.")
