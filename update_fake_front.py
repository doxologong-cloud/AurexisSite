import os
import re

index_path = r"C:\Users\user\Desktop\сайт\templates\index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

old_fake_front_regex = r'<div id="fake-front" style="display: flex; justify-content: center; align-items: center; height: 100vh; width: 100vw; background: #000; color: #ff0000; font-family: \'Space Grotesk\', sans-serif; font-size: 3rem; text-shadow: 0 0 20px #ff0000; position: fixed; top: 0; left: 0; z-index: 9999; transition: opacity 1s, filter 1s;">\s*\(Ведутся РАБОТЫ\)\s*</div>'

new_fake_front = """<div id="fake-front" style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; width: 100vw; background: #050202; color: #ff0000; font-family: 'Consolas', monospace; position: fixed; top: 0; left: 0; z-index: 9999; overflow: hidden; transition: opacity 1s, filter 1s;">
        <!-- Matrix Rain or Grid Background -->
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle, rgba(255,0,0,0.15) 0%, rgba(0,0,0,1) 100%); z-index: -1;"></div>
        
        <!-- Scanning Line -->
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: rgba(255,0,0,0.8); box-shadow: 0 0 20px red; animation: scanLine 4s linear infinite;"></div>

        <style>
            @keyframes scanLine { 0% { top: -10%; } 100% { top: 110%; } }
            @keyframes pulseCursor { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
            .glitch-text { animation: glitch 0.3s infinite; text-shadow: 2px 0 blue, -2px 0 red; }
            @keyframes glitch { 0% { transform: translate(0) } 20% { transform: translate(-2px, 2px) } 40% { transform: translate(-2px, -2px) } 60% { transform: translate(2px, 2px) } 80% { transform: translate(2px, -2px) } 100% { transform: translate(0) } }
        </style>

        <i class="fa-solid fa-lock" style="font-size: 5rem; margin-bottom: 25px; color: #ff0000; text-shadow: 0 0 30px #ff0000;"></i>
        <div style="font-size: 3.5rem; font-weight: bold; letter-spacing: 12px; text-shadow: 0 0 20px #ff0000; margin-bottom: 15px; text-align: center;">ВЕДУТСЯ РАБОТЫ</div>
        <div style="font-size: 1.2rem; color: #aa0000; letter-spacing: 6px; margin-bottom: 40px; text-align: center;">СИСТЕМА БЛОКИРОВАНА // ВНЕШНИЙ ДОСТУП ЗАКРЫТ</div>
        
        <!-- Fake Console output -->
        <div style="width: 600px; height: 180px; background: rgba(15,0,0,0.9); border: 1px solid #880000; box-shadow: 0 0 20px rgba(255,0,0,0.2), inset 0 0 10px rgba(255,0,0,0.1); border-radius: 4px; padding: 20px; font-size: 0.95rem; line-height: 1.6; color: #ff4444; overflow: hidden; display: flex; flex-direction: column; justify-content: flex-end;">
            <div style="opacity: 0.5;">> Инициализация брандмауэра... [ОК]</div>
            <div style="opacity: 0.6;">> Сканирование входящих подключений... [0 угроз]</div>
            <div style="opacity: 0.8;">> Маршрутизация закрыта администратором.</div>
            <div style="color: #ff0000; font-weight: bold; margin-top: 10px;">> Ожидание ввода протокола авторизации<span style="animation: pulseCursor 1s infinite;">_</span></div>
        </div>
    </div>"""

# Try regex replacement first
new_html, count = re.subn(old_fake_front_regex, new_fake_front, html, flags=re.DOTALL)

# If regex failed (maybe slightly different spacing), try to replace manually
if count == 0:
    start_tag = '<div id="fake-front"'
    end_tag = '(Ведутся РАБОТЫ)\n    </div>'
    start_idx = html.find(start_tag)
    end_idx = html.find(end_tag) + len(end_tag)
    if start_idx != -1 and html.find(end_tag) != -1:
        new_html = html[:start_idx] + new_fake_front + html[end_idx:]
        count = 1

if count > 0:
    # Need to add FontAwesome to index.html if it's missing, since we added <i class="fa-solid fa-lock">
    if "font-awesome" not in new_html:
        head_end = new_html.find('</head>')
        fa_link = '\n    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">\n'
        new_html = new_html[:head_end] + fa_link + new_html[head_end:]
        
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Fake front updated to look super cool.")
else:
    print("Could not find fake front to replace.")
