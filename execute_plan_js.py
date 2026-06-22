import re

# 1. Update CSS avatar
with open('static/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

old_css = """.chat-item-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(45deg, var(--neon-primary), var(--neon-secondary));
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: black;
}"""

new_css = """.chat-item-avatar {
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

if old_css in css:
    css = css.replace(old_css, new_css)
with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(css)


# 2. Update script.js
with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Hide email from search
old_search_ui = 'div.innerHTML = `<span style="color: white; font-weight: bold;">${u.username}</span> <br><span style="color: gray; font-size: 0.8rem;">${u.email}</span>`;'
new_search_ui = 'div.innerHTML = `<span style="color: white; font-weight: bold;">${u.username}</span>`;'

if old_search_ui in js:
    js = js.replace(old_search_ui, new_search_ui)
    
# Implement Fast Auth caching
old_check_auth = """    async function checkAuth() {
        try {
            const res = await fetch('/api/me');
            const data = await res.json();
            if(data.success && data.user) {
                window.loginUser(data.user, false);
            }
        } catch(e) {}
    }"""

new_check_auth = """    async function checkAuth() {
        const cachedUser = localStorage.getItem('currentUser');
        if (cachedUser) {
            window.loginUser(JSON.parse(cachedUser), false);
        }
        try {
            const res = await fetch('/api/me');
            const data = await res.json();
            if(data.success && data.user) {
                localStorage.setItem('currentUser', JSON.stringify(data.user));
                if (!cachedUser) window.loginUser(data.user, false);
            } else {
                localStorage.removeItem('currentUser');
                if (cachedUser) window.location.reload();
            }
        } catch(e) {}
    }"""

if old_check_auth in js:
    js = js.replace(old_check_auth, new_check_auth)

# Add localStorage logic to logout
old_logout = """        window.currentUser = null;
        document.getElementById('nav-account').style.display = 'none';"""

new_logout = """        window.currentUser = null;
        localStorage.removeItem('currentUser');
        document.getElementById('nav-account').style.display = 'none';"""

if old_logout in js:
    js = js.replace(old_logout, new_logout)


with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated JS successfully!")
