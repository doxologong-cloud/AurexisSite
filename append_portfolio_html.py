import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add link to navbar
if 'href="#portfolio"' not in text:
    text = text.replace('<a href="#about">О нас</a>', '<a href="#about">О нас</a>\n            <a href="#portfolio">Магазин Ботов</a>')

# Add portfolio view
portfolio_html = """
        <!-- Portfolio View -->
        <div id="view-portfolio" class="view" style="display: none;">
            <div class="hero" style="min-height: 40vh; padding-top: 100px;">
                <h1 class="glitch" data-text="НАШИ БОТЫ" style="font-size: 3.5rem;">НАШИ БОТЫ</h1>
                <p>Лучшие Discord-боты для вашего сервера.</p>
            </div>
            
            <div class="portfolio-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; padding: 50px;">
                <!-- Card 1 -->
                <div class="tilt-card" style="background: rgba(10,10,15,0.8); border: 1px solid var(--neon-primary); border-radius: 15px; padding: 30px; text-align: center; transition: transform 0.3s, box-shadow 0.3s; position: relative; overflow: hidden;">
                    <div style="font-size: 4rem; margin-bottom: 20px;">🛡️</div>
                    <h3 style="color: var(--neon-primary); margin-bottom: 10px;">Aurex Protect</h3>
                    <p style="color: #aaa; margin-bottom: 20px;">Продвинутая система модерации и анти-спама для крупных серверов.</p>
                    <div style="font-weight: bold; font-size: 1.2rem; margin-bottom: 20px;">Бесплатно</div>
                    <button class="glow-btn" style="width: 100%;">Добавить на сервер</button>
                </div>
                
                <!-- Card 2 -->
                <div class="tilt-card" style="background: rgba(10,10,15,0.8); border: 1px solid var(--neon-secondary); border-radius: 15px; padding: 30px; text-align: center; transition: transform 0.3s, box-shadow 0.3s; position: relative; overflow: hidden;">
                    <div style="font-size: 4rem; margin-bottom: 20px;">🎵</div>
                    <h3 style="color: var(--neon-secondary); margin-bottom: 10px;">Aurex Music</h3>
                    <p style="color: #aaa; margin-bottom: 20px;">Музыкальный бот с поддержкой Spotify, YouTube и фильтрами звука.</p>
                    <div style="font-weight: bold; font-size: 1.2rem; margin-bottom: 20px;">$5 / месяц</div>
                    <button class="glow-btn secondary" style="width: 100%;">Купить Premium</button>
                </div>
                
                <!-- Card 3 -->
                <div class="tilt-card" style="background: rgba(10,10,15,0.8); border: 1px solid #ff0055; border-radius: 15px; padding: 30px; text-align: center; transition: transform 0.3s, box-shadow 0.3s; position: relative; overflow: hidden;">
                    <div style="font-size: 4rem; margin-bottom: 20px;">🎲</div>
                    <h3 style="color: #ff0055; margin-bottom: 10px;">Aurex Economy</h3>
                    <p style="color: #aaa; margin-bottom: 20px;">Экономика, мини-игры, казино и уровни активности.</p>
                    <div style="font-weight: bold; font-size: 1.2rem; margin-bottom: 20px;">Бесплатно</div>
                    <button class="glow-btn" style="width: 100%; border-color: #ff0055; color: #ff0055; box-shadow: 0 0 10px rgba(255,0,85,0.2);">Добавить на сервер</button>
                </div>
            </div>
        </div>
"""

if 'id="view-portfolio"' not in text:
    text = text.replace('<!-- End of Main Content -->', portfolio_html + '\n<!-- End of Main Content -->')
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added Portfolio HTML")
else:
    print("Portfolio HTML already exists")
