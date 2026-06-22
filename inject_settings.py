with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

settings_html = """
    <!-- Settings Window -->
    <div id="view-settings" class="window">
        <div class="window-header" onmousedown="startDrag(event, 'view-settings')">
            <div class="window-title">Настройки Web-OS</div>
            <div class="window-controls">
                <button class="window-btn btn-min" onclick="minimizeWindow('view-settings')"></button>
                <button class="window-btn btn-max" onclick="maximizeWindow('view-settings')"></button>
                <button class="window-btn btn-close" onclick="closeWindow('view-settings')"></button>
            </div>
        </div>
        <div class="window-content" style="padding: 20px;">
            <h3 style="color: var(--neon-color); text-transform: uppercase;">Внешний вид</h3>
            <div style="margin-top: 15px;">
                <label style="color: #fff; margin-right: 10px;">Тема оформления:</label>
                <select id="theme-selector" onchange="changeTheme(this.value)" style="background: rgba(0,0,0,0.5); border: 1px solid var(--neon-color); color: var(--neon-color); padding: 5px; border-radius: 5px; cursor: pointer;">
                    <option value="matrix">Матрица (Неоновый Желтый)</option>
                    <option value="synthwave">Синтвейв (Розово-Фиолетовый)</option>
                    <option value="cyberpunk">Киберпанк (Голубой/Розовый)</option>
                </select>
            </div>
            <div style="margin-top: 25px;">
                <label style="color: #fff; margin-right: 10px;">Язык интерфейса:</label>
                <select id="lang-selector" onchange="changeLang(this.value)" style="background: rgba(0,0,0,0.5); border: 1px solid var(--neon-color); color: var(--neon-color); padding: 5px; border-radius: 5px; cursor: pointer;">
                    <option value="ru">Русский (RU)</option>
                    <option value="en">English (EN)</option>
                </select>
            </div>
        </div>
    </div>
"""

if 'view-settings' not in html:
    html = html.replace('</main>', settings_html + '\n</main>')
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected Settings window HTML.")
else:
    print("Settings window already exists.")
