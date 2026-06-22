import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# The current block from <a href="#" id="open-auth" to the end of <div class="nav-account">
# and the discord button
old_html = """            <a href="#" id="open-auth" class="nav-auth-link" style="color: var(--neon-primary); font-weight: 600;">Вход / Регистрация</a>
            <div class="nav-account" id="nav-account" style="display: none; position: relative; cursor: pointer;">
                <div class="user-profile" id="user-profile">
                    <img src="{{ url_for('static', filename='assets/default-avatar.png') }}" alt="User" class="nav-avatar" id="nav-avatar-img">
                    <span id="nav-username">User</span>
                </div>
                <div class="dropdown-menu" id="account-dropdown">
                    <a href="#account" class="dropdown-item" id="go-profile-btn" style="text-decoration: none; display: block; padding: 8px 10px; color: white;">Мой профиль</a>
                    <a href="#settings" class="dropdown-item" id="go-settings-btn" style="text-decoration: none; display: block; padding: 8px 10px; color: white;">Настройки</a>
                    <a href="/admin" id="nav-admin-link" style="display: none; padding: 8px 10px; color: #ff0055; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 5px; font-weight: bold;">Панель</a>
                    <div class="dropdown-item" id="change-avatar-btn">Сменить аватар</div>
                    <div class="dropdown-item" id="logout-btn" style="color: #ff4444;">Выйти</div>
                </div>
            </div>
        </div>
        <a href="https://discord.gg/yourlink" target="_blank" class="discord-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                <path d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189Z"/>
            </svg>
            Наш Discord
        </a>"""

new_html = """        </div>
        <div class="nav-auth-section" style="display: flex; align-items: center;">
            <a href="#" id="open-auth" class="nav-auth-link" style="color: var(--neon-primary); font-weight: 600; text-decoration: none;">Вход / Регистрация</a>
            <div class="nav-account" id="nav-account" style="display: none; position: relative; cursor: pointer;">
                <div class="user-profile" id="user-profile">
                    <img src="{{ url_for('static', filename='assets/default-avatar.png') }}" alt="User" class="nav-avatar" id="nav-avatar-img">
                    <span id="nav-username">User</span>
                </div>
                <div class="dropdown-menu" id="account-dropdown">
                    <a href="#account" class="dropdown-item" id="go-profile-btn" style="text-decoration: none; display: block; padding: 8px 10px; color: white;">Мой профиль</a>
                    <a href="#settings" class="dropdown-item" id="go-settings-btn" style="text-decoration: none; display: block; padding: 8px 10px; color: white;">Настройки</a>
                    <a href="/admin" id="nav-admin-link" style="display: none; padding: 8px 10px; color: #ff0055; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 5px; font-weight: bold;">Панель</a>
                    <div class="dropdown-item" id="change-avatar-btn">Сменить аватар</div>
                    <div class="dropdown-item" id="logout-btn" style="color: #ff4444;">Выйти</div>
                </div>
            </div>
        </div>"""

if old_html in text:
    text = text.replace(old_html, new_html)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Navbar structure updated successfully.")
else:
    print("Could not find the exact old HTML block. Trying regex...")
    # fallback
    pass
