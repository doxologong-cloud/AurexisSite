import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

# 1. Fix the auth tabs unclickable/overlap issue
# Replace the old authTabs click listener with a better one
old_click_listener = """authTabs.forEach(tab => {
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
            if (googleAuthContainer) googleAuthContainer.style.display = 'block';
        });
    });"""

new_click_listener = """authTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            if (tab.classList.contains('active')) return;
            switchAuthTab(tab.dataset.tab);
        });
    });"""

if old_click_listener in js_text:
    js_text = js_text.replace(old_click_listener, new_click_listener)

# 2. Fix the router to ensure .auth-tabs is visible
router_old = """document.getElementById('profile-display').style.display = 'none';
                document.querySelector('.auth-content').style.display = 'block';"""

router_new = """document.getElementById('profile-display').style.display = 'none';
                document.querySelector('.auth-content').style.display = 'block';
                const tabsContainer = document.querySelector('.auth-tabs');
                if(tabsContainer) tabsContainer.style.display = 'flex';"""

if router_old in js_text:
    js_text = js_text.replace(router_old, router_new)

# 3. Fix the race condition in sendGlobalChat
send_old = """async function sendGlobalChat() {
    if(!window.currentUser) {
        showToast('"""

send_new = """async function sendGlobalChat() {
    if(!window.currentUser) await loadUserProfile();
    if(!window.currentUser) {
        showToast('"""

if send_old in js_text:
    js_text = js_text.replace(send_old, send_new)

# Fix the same for ticket submission
ticket_old = """async function submitTicket(e) {
    e.preventDefault();
    if(!window.currentUser) {"""

ticket_new = """async function submitTicket(e) {
    e.preventDefault();
    if(!window.currentUser) await loadUserProfile();
    if(!window.currentUser) {"""

if ticket_old in js_text:
    js_text = js_text.replace(ticket_old, ticket_new)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Fixed auth tab glitches and race condition.")
