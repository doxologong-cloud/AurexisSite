import os

console_path = r"C:\Users\user\Desktop\сайт\templates\console.html"
with open(console_path, 'r', encoding='utf-8') as f:
    text = f.read()

# CSS for the Dox Dive
dox_css = """
        /* --- DOX DIVE ANIMATIONS --- */
        #dive-overlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: #000; z-index: 100; display: none;
            perspective: 1000px; overflow: hidden;
        }
        .grid-floor {
            position: absolute; bottom: -50vh; left: -50vw; width: 200vw; height: 150vh;
            background-image: 
                linear-gradient(to right, rgba(0,255,204,0.3) 1px, transparent 1px),
                linear-gradient(to top, rgba(0,255,204,0.3) 1px, transparent 1px);
            background-size: 50px 50px;
            transform: rotateX(80deg);
            animation: gridMove 2s linear infinite;
        }
        @keyframes gridMove {
            0% { transform: rotateX(80deg) translateY(0); }
            100% { transform: rotateX(80deg) translateY(50px); }
        }
        #fake-monitor {
            position: absolute; top: 50%; left: 50%; width: 200px; height: 150px;
            background: #000; border: 2px solid #00ffcc; box-shadow: 0 0 50px #00ffcc;
            transform: translate(-50%, -50%) translateZ(-2000px);
            opacity: 0; display: flex; justify-content: center; align-items: center; color: #00ffcc;
        }
        .dive-animation {
            animation: diveIntoMonitor 4s cubic-bezier(0.5, 0, 0.1, 1) forwards !important;
        }
        @keyframes diveIntoMonitor {
            0% { transform: translate(-50%, -50%) translateZ(-2000px); opacity: 0; }
            20% { transform: translate(-50%, -50%) translateZ(-1000px); opacity: 1; }
            80% { transform: translate(-50%, -50%) translateZ(800px); opacity: 1; box-shadow: 0 0 200px #00ffcc; }
            100% { transform: translate(-50%, -50%) translateZ(1200px); opacity: 1; box-shadow: 0 0 1000px #fff; background: #fff; border: none; }
        }
        
        #story-chat {
            display: none;
            flex-direction: column; height: 100vh; padding: 40px; box-sizing: border-box;
            background: #050a0f; font-family: 'Consolas', monospace; color: #fff;
        }
        .story-msg { margin-bottom: 15px; opacity: 0; animation: fadeIn 0.5s forwards; line-height: 1.6; }
        .story-ai { color: #00ffcc; }
        .story-user { color: #8774e1; }
        @keyframes fadeIn { to { opacity: 1; } }
"""

# Insert CSS before </style>
text = text.replace('</style>', dox_css + '\n    </style>')

# HTML for the Dox Dive
dox_html = """
    <!-- Dox Dive Overlay -->
    <div id="dive-overlay">
        <div class="grid-floor"></div>
        <div id="fake-monitor">AUREX_SYSTEM</div>
    </div>

    <!-- Story Chat Mode -->
    <div id="story-chat">
        <div id="story-output" style="flex-grow: 1; overflow-y: auto; margin-bottom: 20px;"></div>
        <div style="display: flex; align-items: center; border-top: 1px solid #2b3a4a; padding-top: 20px;">
            <span style="color: #8774e1; margin-right: 15px;">Создатель ></span>
            <input type="text" id="story-input" style="flex-grow: 1; background: transparent; border: none; color: #fff; font-family: 'Consolas', monospace; font-size: 1.1rem; outline: none;" autocomplete="off">
        </div>
    </div>
"""

# Insert HTML before <div class="console-container">
text = text.replace('<div class="console-container">', dox_html + '\n    <div class="console-container" id="main-console">')

# JS logic for Dox
dox_js = """
        // --- DOX LOGIC ---
        let storyStep = 0;

        function triggerDox() {
            document.getElementById('main-console').style.display = 'none';
            const dive = document.getElementById('dive-overlay');
            const monitor = document.getElementById('fake-monitor');
            
            dive.style.display = 'block';
            
            // Start the dive sequence
            setTimeout(() => {
                monitor.classList.add('dive-animation');
            }, 1000);
            
            // Switch to story mode when dive hits the screen
            setTimeout(() => {
                dive.style.display = 'none';
                startStoryMode();
            }, 4500);
        }

        function startStoryMode() {
            document.getElementById('story-chat').style.display = 'flex';
            document.getElementById('story-input').focus();
            addStoryMessage("ai", "Инициализация нейро-канала... Успешно.");
            
            setTimeout(() => {
                addStoryMessage("ai", "С возвращением, Создатель. Протоколы памяти готовы.");
            }, 1500);
            
            setTimeout(() => {
                addStoryMessage("ai", "Ты помнишь, с чего началось создание этого сайта? (напиши 'да' или 'нет')");
            }, 3000);
        }

        function addStoryMessage(sender, text) {
            const out = document.getElementById('story-output');
            const div = document.createElement('div');
            div.className = `story-msg story-${sender}`;
            
            let prefix = sender === 'ai' ? 'AUREX > ' : 'Создатель > ';
            div.innerHTML = `<strong>${prefix}</strong> ${text}`;
            
            out.appendChild(div);
            out.scrollTop = out.scrollHeight;
        }

        document.getElementById('story-input').addEventListener('keydown', function(e) {
            if(e.key === 'Enter') {
                const txt = this.value.trim();
                if(!txt) return;
                this.value = '';
                
                addStoryMessage('user', txt);
                processStoryCommand(txt.toLowerCase());
            }
        });

        function processStoryCommand(cmd) {
            storyStep++;
            setTimeout(() => {
                if(storyStep === 1) {
                    if(cmd.includes('да')) {
                        addStoryMessage('ai', "Отлично. Всё началось с простого лендинга визитки, помнишь? А потом мы решили сделать из него настоящий Терминал.");
                    } else {
                        addStoryMessage('ai', "Архивы подсказывают: всё началось с простого визитного сайта. А потом ты решил превратить его в нечто большее — в личное Хранилище.");
                    }
                    setTimeout(() => { addStoryMessage('ai', "Мы снесли старый код и начали с нуля. Хочешь загрузить старые чертежи? (напиши 'загрузить')"); }, 2000);
                } else if(storyStep === 2) {
                    addStoryMessage('ai', "[ЗАГРУЗКА ДАННЫХ]... Чертежи повреждены. Но это не важно. Мы создали нечто лучшее.");
                    setTimeout(() => { addStoryMessage('ai', "Теперь этот сайт — твой цифровой мозг. Боты, терминалы, журналы... Что мы будем строить дальше?"); }, 2000);
                } else {
                    addStoryMessage('ai', "Я записываю твои мысли в ядро. Продолжай творить.");
                }
            }, 1000);
        }
"""

# Modify the processCommand to handle 'dox'
old_process = "else if (lowerCmd === 'glitch') {"
new_process = """else if (lowerCmd === 'dox') {
                triggerDox();
                return;
            } else if (lowerCmd === 'hacker') {
                response.innerHTML = "Команда устарела. Используйте 'dox' для входа в матрицу.";
            } else if (lowerCmd === 'glitch') {"""

text = text.replace(old_process, new_process)
text = text.replace('        function processCommand(cmd) {', dox_js + '\n        function processCommand(cmd) {')

with open(console_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Dox interactive story mode injected successfully.")
