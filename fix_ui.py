import os
import re

# 1. CREATE console.html
console_path = r"C:\Users\user\Desktop\сайт\templates\console.html"
console_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>AUREX OS TERMINAL</title>
    <style>
        body, html { margin: 0; padding: 0; height: 100%; background: #000; color: #00ffcc; font-family: 'Consolas', monospace; overflow: hidden; }
        .console-container { display: flex; flex-direction: column; height: 100vh; padding: 20px; box-sizing: border-box; }
        .console-output { flex-grow: 1; overflow-y: auto; display: flex; flex-direction: column; justify-content: flex-end; padding-bottom: 20px; font-size: 1rem; line-height: 1.5; }
        .console-input-row { display: flex; align-items: center; border-top: 1px dashed #00ffcc; padding-top: 15px; }
        .console-input { flex-grow: 1; background: transparent; border: none; color: #fff; font-family: 'Consolas', monospace; font-size: 1.2rem; outline: none; margin-left: 10px; }
        
        @keyframes glitchText {
            0% { transform: translate(0); }
            20% { transform: translate(-2px, 1px); }
            40% { transform: translate(2px, -1px); color: #fff; }
            60% { transform: translate(-1px, 2px); }
            80% { transform: translate(1px, -2px); color: #ff0033; }
            100% { transform: translate(0); }
        }
    </style>
</head>
<body>
    <div class="console-container">
        <div style="border-bottom: 1px dashed #00ffcc; padding-bottom: 15px; margin-bottom: 20px; opacity: 0.7;">
            AUREX OS TERMINAL v2.1 // ПРЯМОЙ ДОСТУП<br>
            Введите 'help' для списка команд.
        </div>
        <div id="console-output" class="console-output">
            <div>> Инициализация консоли... Успешно.</div>
            <div>> Ожидание ввода.</div>
        </div>
        <div class="console-input-row">
            <span>root@vault:~#</span>
            <input type="text" id="console-input" class="console-input" autocomplete="off" autofocus>
        </div>
    </div>
    <script>
        const consoleInput = document.getElementById('console-input');
        const consoleOutput = document.getElementById('console-output');

        consoleInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                const cmd = this.value.trim();
                this.value = '';
                
                const userLine = document.createElement('div');
                userLine.innerHTML = `<span style="color: #fff;">root@vault:~#</span> ${cmd}`;
                consoleOutput.appendChild(userLine);
                
                processCommand(cmd);
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
            
            if (cmd !== "") consoleOutput.appendChild(response);
        }
    </script>
</body>
</html>
"""
with open(console_path, 'w', encoding='utf-8') as f:
    f.write(console_content)


# 2. UPDATE server.py to add /console route
server_path = r"C:\Users\user\Desktop\сайт\server.py"
with open(server_path, 'r', encoding='utf-8') as f:
    server_text = f.read()

if "@app.route('/console')" not in server_text:
    route_code = """
@app.route('/console')
def console():
    return render_template('console.html')
"""
    server_text = server_text.replace("if __name__ == '__main__':", route_code + "\nif __name__ == '__main__':")
    with open(server_path, 'w', encoding='utf-8') as f:
        f.write(server_text)


# 3. REPAIR index.html
index_path = r"C:\Users\user\Desktop\сайт\templates\index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Change the sidebar item to be a proper link opening in a new tab
html = html.replace("""<div class="sidebar-item" onclick="openTab('panel')"><i class="fa-solid fa-terminal"></i> ПАНЕЛЬ</div>""", """<a href="/console" target="_blank" class="sidebar-item" style="text-decoration:none;"><i class="fa-solid fa-terminal"></i> ПАНЕЛЬ</a>""")

# Fix the broken HTML structure
# Find the start of Profile Modal and move it to the end of the body to fix pointer-events and layout
modal_pattern = re.compile(r'(<!-- Profile Modal -->.*?<!-- Settings Modal -->.*?</div>\s*</div>)', re.DOTALL)
match = modal_pattern.search(html)

if match:
    modals_code = match.group(1)
    # Remove modals from their broken location inside the center content flexbox
    html = html.replace(modals_code, "")
    
    # Remove the tab-panel
    html = re.sub(r'<!-- Panel \(Console\) Tab -->.*?<!-- Journal Tab -->', '<!-- Journal Tab -->', html, flags=re.DOTALL)
    
    # Also clean up the orphaned closing divs that were causing overlapping
    html = re.sub(r'</div>\s*</div>\s*<div class="profile-actions">', '<div class="profile-actions">', html)
    
    # Put modals code cleanly right before <script> tags
    html = html.replace('<!-- Hidden file inputs -->', modals_code + '\n    <!-- Hidden file inputs -->')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("UI fixed successfully.")
