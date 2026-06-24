import os
import re

index_path = r"C:\Users\user\Desktop\сайт\templates\index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace tab-welcome with a cooler version
old_welcome = """            <!-- Default Welcome -->
            <div id="tab-welcome" class="vault-tab" style="display: flex; flex-direction: column; align-items: center; color: rgba(255,255,255,0.3); font-size: 1.2rem; letter-spacing: 2px; text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 20px;"><i class="fa-solid fa-shield-halved"></i></div>
                <div>СИСТЕМА АКТИВИРОВАНА.</div>
                <div style="font-size: 0.9rem; margin-top: 10px;">ВЫБЕРИТЕ РАЗДЕЛ В МЕНЮ СЛЕВА.</div>
            </div>"""

new_welcome = """            <!-- Default Welcome -->
            <div id="tab-welcome" class="vault-tab" style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; height: 100%;">
                
                <!-- Cool Animated Core -->
                <div style="position: relative; width: 200px; height: 200px; margin-bottom: 40px;">
                    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 50%; border: 2px dashed #00ffcc; animation: spinRight 10s linear infinite; opacity: 0.5;"></div>
                    <div style="position: absolute; top: 10px; left: 10px; width: 180px; height: 180px; border-radius: 50%; border: 2px solid #8774e1; animation: spinLeft 7s linear infinite; opacity: 0.3;"></div>
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 4rem; color: #fff; text-shadow: 0 0 20px #00ffcc;">
                        <i class="fa-solid fa-shield-virus"></i>
                    </div>
                </div>

                <style>
                    @keyframes spinRight { 100% { transform: rotate(360deg); } }
                    @keyframes spinLeft { 100% { transform: rotate(-360deg); } }
                    @keyframes pulseText { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; text-shadow: 0 0 15px #00ffcc; } }
                </style>

                <!-- Status Info -->
                <div style="color: #00ffcc; font-family: 'Consolas', monospace; font-size: 1.5rem; letter-spacing: 5px; animation: pulseText 2s infinite;">
                    СИСТЕМА АКТИВИРОВАНА
                </div>
                
                <div style="display: flex; gap: 40px; margin-top: 40px; font-family: 'Consolas', monospace;">
                    <div style="text-align: center;">
                        <div style="color: #7f91a4; font-size: 0.8rem; margin-bottom: 5px;">СТАТУС ЯДРА</div>
                        <div style="color: #4caf50; font-weight: bold;">ОНЛАЙН</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #7f91a4; font-size: 0.8rem; margin-bottom: 5px;">НЕЙРОСЕТЬ</div>
                        <div style="color: #ffbb33; font-weight: bold;">ОЖИДАНИЕ</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #7f91a4; font-size: 0.8rem; margin-bottom: 5px;">ЗАЩИТА</div>
                        <div style="color: #8774e1; font-weight: bold;">АКТИВНА</div>
                    </div>
                </div>

                <div style="color: rgba(255,255,255,0.3); font-size: 0.9rem; margin-top: 50px; letter-spacing: 2px;">
                    ОТКРОЙТЕ МЕНЮ СЛЕВА ДЛЯ УПРАВЛЕНИЯ
                </div>
            </div>"""

if old_welcome in html:
    html = html.replace(old_welcome, new_welcome)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Welcome screen updated successfully.")
else:
    print("Could not find the old welcome screen.")
