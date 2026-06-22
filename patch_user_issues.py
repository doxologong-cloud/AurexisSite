import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove Preloader delay
old_preloader = """    // Simulate loading time (e.g. 2.5 seconds)
    setTimeout(() => {
        welcomeScreen.style.opacity = '0';
        setTimeout(() => {
            welcomeScreen.style.visibility = 'hidden';
            // Show main elements after preloader finishes
            document.querySelector('.hero').classList.add('show');
            initScrollAnimations();
        }, 500);
    }, 5000);"""

new_preloader = """    // Instant load
    welcomeScreen.style.opacity = '0';
    setTimeout(() => {
        welcomeScreen.style.visibility = 'hidden';
        document.querySelector('.hero')?.classList.add('show');
        initScrollAnimations();
    }, 100);"""

text = text.replace(old_preloader, new_preloader)

# 2. Protect #account route
old_route = """        } else if (hash === '#account') {
            const accView = document.getElementById('view-account');
            if(accView) {
                accView.classList.remove('hidden-view');
                accView.classList.add('active');
            }"""

new_route = """        } else if (hash === '#account') {
            if (!window.currentUser) {
                showToast('Нет доступа, вы не зарегистрированы', 'error');
                window.location.hash = '#home';
                return;
            }
            const accView = document.getElementById('view-account');
            if(accView) {
                accView.classList.remove('hidden-view');
                accView.classList.add('active');
            }"""

text = text.replace(old_route, new_route)

# 3. Add validation to register form
old_reg_submit = """    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const nickname = document.getElementById('reg-nickname').value;
        const email = document.getElementById('reg-email').value;
        const pass = document.getElementById('reg-password').value;
        const err = document.getElementById('reg-error');
        
        if (pass.length < 8) {"""

new_reg_submit = """    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const nickname = document.getElementById('reg-nickname').value.trim();
        const email = document.getElementById('reg-email').value.trim();
        const pass = document.getElementById('reg-password').value;
        const err = document.getElementById('reg-error');
        
        if (!nickname || !email || !pass) {
            err.textContent = 'Заполните все поля!';
            return;
        }
        
        if (pass.length < 8) {"""

text = text.replace(old_reg_submit, new_reg_submit)

# Add validation to login form too
old_login_submit = """    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const pass = document.getElementById('login-password').value;
        const err = document.getElementById('login-error');
        err.textContent = 'Вход...';"""

new_login_submit = """    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('login-email').value.trim();
        const pass = document.getElementById('login-password').value;
        const err = document.getElementById('login-error');
        
        if (!email || !pass) {
            err.textContent = 'Заполните все поля!';
            return;
        }
        err.textContent = 'Вход...';"""

text = text.replace(old_login_submit, new_login_submit)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patched script.js successfully!")
