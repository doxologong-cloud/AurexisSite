import re

index_path = r"C:\Users\user\Desktop\сайт\templates\index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Sidebar Items
new_sidebar = """        <div class="sidebar-menu">
            <div class="sidebar-item"><img src="/static/assets/default-avatar.png" id="sidebar-avatar-mini" style="width: 24px; height: 24px; border-radius: 50%; object-fit: cover;"> <span id="sidebar-name-mini">ДомадOX</span></div>
            <div class="sidebar-divider"></div>
            
            <div class="sidebar-item" onclick="openProfile()"><i class="fa-regular fa-user"></i> Мой профиль</div>
            <div class="sidebar-item" onclick="openTab('bots')"><i class="fa-solid fa-robot"></i> БОТЫ</div>
            <div class="sidebar-item" onclick="openTab('panel')"><i class="fa-solid fa-terminal"></i> ПАНЕЛЬ</div>
            <div class="sidebar-item" onclick="openTab('journal')"><i class="fa-solid fa-book"></i> Журнал</div>
            <div class="sidebar-divider"></div>
            <div class="sidebar-item" onclick="openSettings()"><i class="fa-solid fa-gear"></i> Настройки системы</div>
        </div>"""

text = re.sub(r'<div class="sidebar-menu">.*?</div>\s*</div>\s*</div>', new_sidebar + '\n    </div>\n</div>', text, flags=re.DOTALL)

# 2. Update Main Center Content with Tabs
tabs_html = """        <!-- Main Center Content -->
        <div style="flex-grow: 1; position: relative; pointer-events: auto; padding: 40px; display: flex; justify-content: center; align-items: center;">
            
            <!-- Default Welcome -->
            <div id="tab-welcome" class="vault-tab" style="display: flex; flex-direction: column; align-items: center; color: rgba(255,255,255,0.3); font-size: 1.2rem; letter-spacing: 2px; text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 20px;"><i class="fa-solid fa-shield-halved"></i></div>
                <div>СИСТЕМА АКТИВИРОВАНА.</div>
                <div style="font-size: 0.9rem; margin-top: 10px;">ВЫБЕРИТЕ РАЗДЕЛ В МЕНЮ СЛЕВА.</div>
            </div>

            <!-- Bots Tab -->
            <div id="tab-bots" class="vault-tab" style="display: none; width: 100%; max-width: 900px; background: rgba(20,28,36,0.9); border: 1px solid #2b3a4a; border-radius: 12px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); backdrop-filter: blur(10px);">
                <h2 style="margin-top: 0; color: #fff; border-bottom: 1px solid #2b3a4a; padding-bottom: 15px; display: flex; justify-content: space-between;">
                    <span><i class="fa-solid fa-robot"></i> УПРАВЛЕНИЕ БОТАМИ</span>
                    <button style="background: transparent; border: 1px dashed #7f91a4; color: #7f91a4; cursor: pointer; padding: 5px 15px; border-radius: 4px;">+ ДОБАВИТЬ</button>
                </h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                    <!-- Bot Card 1 -->
                    <div style="background: #1c242d; border: 1px solid #232e3c; border-radius: 8px; padding: 20px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <div style="font-weight: bold; font-size: 1.1rem; color: #fff;">AUREX_CORE</div>
                            <div style="color: #4caf50; font-size: 0.8rem; border: 1px solid #4caf50; padding: 2px 8px; border-radius: 10px;">ONLINE</div>
                        </div>
                        <p style="color: #7f91a4; font-size: 0.9rem; margin-bottom: 20px;">Главный нейро-модуль. Отвечает за логику и анализ данных.</p>
                        <div style="display: flex; gap: 10px;">
                            <button style="flex: 1; background: #2b3a4a; color: #fff; border: none; padding: 8px; border-radius: 4px; cursor: pointer; transition: 0.2s;" onmouseover="this.style.background='#ff4444'" onmouseout="this.style.background='#2b3a4a'">ОТКЛЮЧИТЬ</button>
                            <button style="background: #2b3a4a; color: #fff; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer;"><i class="fa-solid fa-gear"></i></button>
                        </div>
                    </div>
                    <!-- Bot Card 2 -->
                    <div style="background: #1c242d; border: 1px solid #232e3c; border-radius: 8px; padding: 20px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <div style="font-weight: bold; font-size: 1.1rem; color: #fff;">DOX_CRAWLER</div>
                            <div style="color: #ff4444; font-size: 0.8rem; border: 1px solid #ff4444; padding: 2px 8px; border-radius: 10px;">OFFLINE</div>
                        </div>
                        <p style="color: #7f91a4; font-size: 0.9rem; margin-bottom: 20px;">Сбор информации. Требует обновления конфигурации прокси.</p>
                        <div style="display: flex; gap: 10px;">
                            <button style="flex: 1; background: #8774e1; color: #fff; border: none; padding: 8px; border-radius: 4px; cursor: pointer; transition: 0.2s;" onmouseover="this.style.background='#7b68c9'" onmouseout="this.style.background='#8774e1'">ЗАПУСТИТЬ</button>
                            <button style="background: #2b3a4a; color: #fff; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer;"><i class="fa-solid fa-gear"></i></button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Panel (Console) Tab -->
            <div id="tab-panel" class="vault-tab" style="display: none; width: 100%; max-width: 800px; height: 60vh; background: rgba(5,10,15,0.95); border: 1px solid #00ffcc; border-radius: 8px; padding: 20px; box-shadow: 0 0 20px rgba(0,255,204,0.1); font-family: 'Consolas', monospace; color: #00ffcc; display: flex; flex-direction: column;">
                <div style="border-bottom: 1px dashed #00ffcc; padding-bottom: 10px; margin-bottom: 10px; font-size: 0.9rem; opacity: 0.7;">
                    AUREX OS TERMINAL v2.1 // ПРЯМОЙ ДОСТУП<br>
                    Введите 'help' для списка команд.
                </div>
                <div id="console-output" style="flex-grow: 1; overflow-y: auto; display: flex; flex-direction: column; justify-content: flex-end; padding-bottom: 10px; font-size: 0.9rem; line-height: 1.5;">
                    <div>> Инициализация консоли... Успешно.</div>
                    <div>> Ожидание ввода.</div>
                </div>
                <div style="display: flex; align-items: center; border-top: 1px dashed #00ffcc; padding-top: 10px;">
                    <span style="margin-right: 10px;">root@vault:~#</span>
                    <input type="text" id="console-input" style="flex-grow: 1; background: transparent; border: none; color: #fff; font-family: 'Consolas', monospace; font-size: 1rem; outline: none;" autocomplete="off" autofocus>
                </div>
            </div>

            <!-- Journal Tab -->
            <div id="tab-journal" class="vault-tab" style="display: none; width: 100%; max-width: 700px; height: 70vh; background: #1c242d; border: 1px solid #2b3a4a; border-radius: 12px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); overflow-y: auto;">
                <h2 style="margin-top: 0; color: #fff; border-bottom: 1px solid #2b3a4a; padding-bottom: 15px;"><i class="fa-solid fa-book-journal-whills"></i> Журнал Обновлений Системы</h2>
                
                <div style="margin-top: 20px; border-left: 2px solid #8774e1; padding-left: 15px; margin-bottom: 25px;">
                    <div style="color: #8774e1; font-size: 0.85rem; font-weight: bold; margin-bottom: 5px;">СЕГОДНЯ</div>
                    <div style="color: #fff; font-size: 1.05rem; margin-bottom: 5px;">Обновление UI Хранилища</div>
                    <div style="color: #7f91a4; font-size: 0.9rem; line-height: 1.5;">
                        - Добавлена новая боковая панель в стиле Telegram.<br>
                        - Добавлен профиль с возможностью редактирования данных.<br>
                        - Добавлена система вкладок (Боты, Консоль, Журнал).<br>
                        - Исправлена привязка настроек фона и звука.
                    </div>
                </div>

                <div style="border-left: 2px solid #2b3a4a; padding-left: 15px; margin-bottom: 25px; opacity: 0.6;">
                    <div style="color: #7f91a4; font-size: 0.85rem; font-weight: bold; margin-bottom: 5px;">РАНЕЕ</div>
                    <div style="color: #fff; font-size: 1.05rem; margin-bottom: 5px;">Инициализация Хранилища</div>
                    <div style="color: #7f91a4; font-size: 0.9rem; line-height: 1.5;">
                        - Удален старый сайт-визитка.<br>
                        - Настроена кодовая фраза "open".<br>
                        - Запущен генератор динамических фонов на Canvas.
                    </div>
                </div>
            </div>

        </div>"""

text = re.sub(r'<!-- Main Center Content Placeholder -->.*?</div>\s*</div>', tabs_html + '\n    </div>', text, flags=re.DOTALL)

# 3. Add JS for Tabs, Console logic, and fix settings bindings
js_updates = """
    // --- SETTINGS BINDINGS FIX ---
    document.getElementById('bg-selector').addEventListener('change', (e) => {
        bgTheme = e.target.value;
        particles = []; // clear old particles
    });

    document.getElementById('audio-toggle').addEventListener('change', (e) => {
        if(e.target.checked) startAudio();
        else stopAudio();
    });

    // --- TAB SYSTEM ---
    function openTab(tabId) {
        // Hide all tabs
        const tabs = document.querySelectorAll('.vault-tab');
        tabs.forEach(tab => tab.style.display = 'none');
        
        // Show selected tab
        const target = document.getElementById('tab-' + tabId);
        if(target) {
            target.style.display = tabId === 'panel' || tabId === 'welcome' ? 'flex' : 'block';
        }
        
        // Close sidebar
        sidebar.style.left = '-300px';
    }

    // --- CONSOLE LOGIC ---
    const consoleInput = document.getElementById('console-input');
    const consoleOutput = document.getElementById('console-output');

    consoleInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            const cmd = this.value.trim();
            this.value = '';
            
            // Print user command
            const userLine = document.createElement('div');
            userLine.innerHTML = `<span style="color: #fff;">root@vault:~#</span> ${cmd}`;
            consoleOutput.appendChild(userLine);
            
            // Process command
            processCommand(cmd);
            
            // Auto scroll to bottom
            consoleOutput.scrollTop = consoleOutput.scrollHeight;
        }
    });

    function processCommand(cmd) {
        const response = document.createElement('div');
        response.style.color = '#7f91a4';
        
        const lowerCmd = cmd.toLowerCase();
        if (lowerCmd === 'help') {
            response.innerHTML = "Доступные команды:<br>help - Показать это сообщение<br>clear - Очистить экран<br>history - Показать историю петли<br>glitch - Вызвать визуальные искажения";
        } else if (lowerCmd === 'clear') {
            consoleOutput.innerHTML = '';
            return;
        } else if (lowerCmd === 'history') {
            response.innerHTML = "Поиск записей...<br>[2021] Петля запущена.<br>[2024] Потеря связи с реальностью.<br>[2026] Хранилище восстановлено.";
        } else if (lowerCmd === 'glitch') {
            response.innerHTML = "Запуск протокола искажения...";
            document.body.style.animation = "glitchText 0.1s infinite";
            setTimeout(() => { document.body.style.animation = ""; }, 1000);
        } else if (cmd !== "") {
            response.innerHTML = `Команда не найдена: ${cmd}`;
        }
        
        if (cmd !== "") {
            consoleOutput.appendChild(response);
        }
    }
"""

text = text.replace('// --- VAULT LOGIC ---', js_updates + '\n\n    // --- VAULT LOGIC ---')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Tabs, Console, Journal and Settings bindings added successfully.")
