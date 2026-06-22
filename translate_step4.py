import re

# 1. Fix translations.js innerHTML vs value for textarea/input
with open('static/translations.js', 'r', encoding='utf-8') as f:
    t_js = f.read()

t_js = t_js.replace("el.innerHTML = translations[key][lang];", """
            if (el.tagName === 'TEXTAREA' || el.tagName === 'INPUT') {
                el.value = translations[key][lang];
            } else {
                el.innerHTML = translations[key][lang];
            }
""")
# Also add "Пока нет новостей." to translations.js dynamic dictionary
# we'll just inject it
t_js = t_js.replace('"Нет": "No"', '"Нет": "No",\n    "Пока нет новостей.": "No news yet."')
with open('static/translations.js', 'w', encoding='utf-8') as f:
    f.write(t_js)

# 2. Fix index.html textarea
with open('templates/index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

# Fix textarea
idx = re.sub(r'<span data-i18n=\"t_100\"># Пиши код бота здесь...\s*def on_message\(msg\):\s*if msg == \'ping\':\s*return \'pong\'</span>', 
             "# Пиши код бота здесь...\\ndef on_message(msg):\\n    if msg == 'ping':\\n        return 'pong'", idx)

idx = idx.replace('<textarea id="code-textarea"', '<textarea id="code-textarea" data-i18n="t_100"')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

# 3. Fix script.js
with open('static/script.js', 'r', encoding='utf-8') as f:
    s_js = f.read()

# Fix loadNews text
s_js = s_js.replace("'Пока нет новостей.'", "__('Пока нет новостей.')")
# Fix locale date in news
s_js = s_js.replace("'ru-RU'", "localStorage.getItem('aurex_lang') === 'en' ? 'en-US' : 'ru-RU'")

# Wrap bot status in __()
s_js = s_js.replace("${botData.status}", "${__(botData.status)}")

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(s_js)

print("Fixed editor placeholder, news translation, and bot statuses!")
