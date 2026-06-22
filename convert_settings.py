from bs4 import BeautifulSoup
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
soup = BeautifulSoup(html, 'html.parser')
view_div = soup.find('div', id='view-settings')
if view_div and 'window' not in view_div.get('class', []):
    window_div = soup.new_tag('div')
    window_div['id'] = 'view-settings'
    window_div['class'] = 'window'
    header_div = soup.new_tag('div')
    header_div['class'] = 'window-header'
    header_div['onmousedown'] = "startDrag(event, 'view-settings')"
    title_div = soup.new_tag('div')
    title_div['class'] = 'window-title'
    title_div.string = 'Настройки'
    controls_div = soup.new_tag('div')
    controls_div['class'] = 'window-controls'
    for btn_class, fn in [('btn-min', 'minimizeWindow'), ('btn-max', 'maximizeWindow'), ('btn-close', 'closeWindow')]:
        btn = soup.new_tag('button')
        btn['class'] = f'window-btn {btn_class}'
        btn['onclick'] = f"{fn}('view-settings')"
        controls_div.append(btn)
    header_div.append(title_div)
    header_div.append(controls_div)
    content_div = soup.new_tag('div')
    content_div['class'] = 'window-content'
    # we inject the settings options here because the old one might be empty
    content_div.append(BeautifulSoup("""
        <div style="padding: 20px;">
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
    """, 'html.parser'))
    window_div.append(header_div)
    window_div.append(content_div)
    view_div.replace_with(window_div)
    
    # Add a button to open settings in the navbar
    nav_right = soup.find('div', class_='nav-right')
    if nav_right:
        settings_btn = soup.new_tag('a')
        settings_btn['href'] = '#'
        settings_btn['onclick'] = "switchView('view-settings')"
        settings_btn['class'] = 'nav-link'
        settings_btn.string = '⚙️'
        nav_right.insert(0, settings_btn)

    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print('Converted view-settings to window')
