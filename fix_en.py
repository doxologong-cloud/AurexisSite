import re
import json

with open('static/translations.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Clean out the bad [EN] prefixes and actually translate them.
bad_to_good = {
    '[EN] Запрещено использование нецензурной лексики, оскорблений и 18+ контента.': 'Profanity, insults, and 18+ content are prohibited.',
    '[EN] Администрация оставляет за собой право удалить отзыв при нарушении правил.': 'Administration reserves the right to delete reviews violating the rules.',
    '[EN] Оценка (1-5)': 'Rating (1-5)',
    '[EN] Ваш отзыв': 'Your review',
    '[EN] Напишите, что вы думаете о нашем сайте...': 'Write what you think about our site...',
    '[EN] Отправить отзыв': 'Submit Review',
    "[EN] document.getElementById('toggle-review-btn').addEventListener('click', function() {\\n                            const container = document.getElementById('review-form-container');\\n                            if (container.style.display === 'none') {\\n                                container.style.display = 'block';\\n                                this.textContent = 'Свернуть';\\n                            } else {\\n                                container.style.display = 'none';\\n                                this.textContent = 'Развернуть';\\n                            }\\n                        });": "document.getElementById('toggle-review-btn').addEventListener('click', function() { const container = document.getElementById('review-form-container'); if (container.style.display === 'none') { container.style.display = 'block'; this.textContent = __('Свернуть'); } else { container.style.display = 'none'; this.textContent = __('Развернуть'); } });",
    '[EN] Поддержка (Тикеты)': 'Support (Tickets)',
    '[EN] Новый тикет': 'New Ticket',
    '[EN] Тема обращения': 'Subject',
    '[EN] Например: Проблема с ботом Economy': 'Example: Issue with Economy bot',
    '[EN] Опишите проблему': 'Describe the issue',
    '[EN] Здравствуйте, у меня возникла проблема...': 'Hello, I have an issue...',
    '[EN] Создать обращение': 'Create Ticket',
    '[EN] Загрузка тикетов...': 'Loading tickets...',
    "[EN] document.getElementById('toggle-ticket-btn').addEventListener('click', function() {\\n                            const container = document.getElementById('ticket-form-container');\\n                            if (container.style.display === 'none') {\\n                                container.style.display = 'block';\\n                                this.textContent = 'Скрыть';\\n                            } else {\\n                                container.style.display = 'none';\\n                                this.textContent = 'Новый тикет';\\n                            }\\n                        });": "document.getElementById('toggle-ticket-btn').addEventListener('click', function() { const container = document.getElementById('ticket-form-container'); if (container.style.display === 'none') { container.style.display = 'block'; this.textContent = __('Скрыть'); } else { container.style.display = 'none'; this.textContent = __('Новый тикет'); } });",
    '[EN] Выйти из аккаунта': 'Logout',
    '[EN] Внешний вид': 'Appearance',
    '[EN] Выбор темы:': 'Theme Selection:',
    '[EN] Матрица': 'Matrix',
    '[EN] Неоновый Желтый': 'Neon Yellow',
    '[EN] Синтвейв': 'Synthwave',
    '[EN] Розовый Неон': 'Pink Neon',
    '[EN] Киберпанк': 'Cyberpunk',
    '[EN] Токсичный Неон': 'Toxic Neon',
    '[EN] Язык интерфейса:': 'Interface Language:',
    '[EN] Русский (RU)': 'Russian (RU)',
    '[EN] НАШИ БОТЫ': 'OUR BOTS',
    '[EN] Лучшие Discord-боты для вашего сервера.': 'Best Discord bots for your server.',
    '[EN] Продвинутая система модерации и анти-спама для крупных серверов.': 'Advanced moderation and anti-spam system.',
    '[EN] Бесплатно': 'Free',
    '[EN] Добавить на сервер': 'Add to Server',
    '[EN] Музыкальный бот с поддержкой Spotify, YouTube и фильтрами звука.': 'Music bot with Spotify and YouTube support.',
    '[EN] $5 / месяц': '$5 / month',
    '[EN] Купить Premium': 'Buy Premium',
    '[EN] Экономика, мини-игры, казино и уровни активности.': 'Economy, minigames, casino, and levels.',
    '[EN] © 2026 Aurexis Studio. Все права защищены.': '© 2026 Aurexis Studio. All rights reserved.',
    '[EN] Discord Сервер': 'Discord Server',
}

for bad, good in bad_to_good.items():
    text = text.replace(bad, good)

# Also fix remaining [EN] manually via regex, though it might leave untranslated russian, it's better than [EN] prefix
text = re.sub(r'\"\[EN\] (.*?)\"', r'"\1"', text)

# Ensure dynamicTranslations has 'Тикет #' and 'Статус:'
extra = '''    "Тикет #": "Ticket #",
    "Статус:": "Status:"'''
text = text.replace('"Открыт": "Open",', '"Открыт": "Open",\n' + extra + ',')

with open('static/translations.js', 'w', encoding='utf-8') as f:
    f.write(text)

# 2. Fix script.js dynamic texts for tickets
with open('static/script.js', 'r', encoding='utf-8') as f:
    script_txt = f.read()

# Fix statuses
script_txt = script_txt.replace("const statusText = t.status === 'open' ? 'Открыт' : 'Закрыт';", "const statusText = __(t.status === 'open' ? 'Открыт' : 'Закрыт');")
script_txt = script_txt.replace("Тикет #${t.id}", "${__('Тикет #')}${t.id}")

# Replace string literal properly
script_txt = re.sub(r'statusEl\.innerHTML = \'Статус: <span style="color: #00ffaa;">Открыт</span>\';', 
                    r'statusEl.innerHTML = __(\'Статус:\') + \' <span style="color: #00ffaa;">\' + __(\'Открыт\') + \'</span>\';', script_txt)

script_txt = re.sub(r'statusEl\.innerHTML = \'Статус: <span style="color: #ff4444;">Закрыт</span>\';', 
                    r'statusEl.innerHTML = __(\'Статус:\') + \' <span style="color: #ff4444;">\' + __(\'Закрыт\') + \'</span>\';', script_txt)


with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(script_txt)

# Bust cache
import re
for path in ['templates/index.html', 'templates/admin.html']:
    with open(path, 'r', encoding='utf-8') as html_f:
        html = html_f.read()
    html = re.sub(r'\?v=\d+', '?v=70', html)
    with open(path, 'w', encoding='utf-8') as html_f:
        html_f.write(html)
