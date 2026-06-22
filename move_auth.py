import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# We need to extract from '<a href="#" id="open-auth"' to '</div>\n</div>\n<a href="https://discord.gg/k9CGaGGtCx"'
# Let's just find the exact boundaries.

auth_section = """            <a href="#" id="open-auth" class="nav-auth-link" style="color: var(--neon-primary); font-weight: 600;">Вход / Регистрация</a>
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
            </div>"""

# Ensure we remove it from inside .nav-links
# and remove the discord btn
import re

# Match the end of nav-links and the discord button
old_block_pattern = re.compile(
    re.escape(auth_section) + r'\s*</div>\s*<a href="https://discord\.gg/k9CGaGGtCx" target="_blank" class="nav-discord-btn">[\s\S]*?</a>\s*</nav>'
)

new_block = """        </div>
        <div class="nav-auth-section" style="display: flex; align-items: center; gap: 15px;">
""" + auth_section + """
        </div>
    </nav>"""

if old_block_pattern.search(text):
    text = old_block_pattern.sub(new_block, text)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully moved auth section and removed Discord button.")
else:
    print("Could not find the block to replace. Pattern did not match.")
