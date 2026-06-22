import re
import json

admin_file = 'templates/admin.html'
with open(admin_file, 'r', encoding='utf-8') as f:
    admin_html = f.read()

# Hardcoded translations for admin
admin_dict = {
    "Пользователи": "Users",
    "Статусы ботов": "Bot Statuses",
    "Новости": "News",
    "Тикеты": "Tickets",
    "Управление подписками Flora и пользователями платформы": "Manage Flora subscriptions and platform users",
    "Мониторинг и управление статусами проектов": "Monitor and manage project statuses",
    "Публикация обновлений на сайте": "Publish updates on the site",
    "Ответы на вопросы и техническая поддержка": "Answers to questions and technical support",
    "Вернуться на сайт": "Back to website",
    "Юзернейм": "Username",
    "Никнейм": "Nickname",
    "Почта": "Email",
    "Действия": "Actions",
    "Действие": "Action",
    "Бот ID": "Bot ID",
    "Текст Статуса": "Status Text",
    "Цвет (HEX)": "Color (HEX)",
    "Написать новость": "Write News",
    "Заголовок новости": "News Title",
    "Текст новости": "News Content",
    "Опубликовать новость": "Publish News",
    "Дата": "Date",
    "Заголовок": "Title",
    "Пользователь": "User",
    "Тема": "Topic",
    "Статус": "Status",
    "Загрузка...": "Loading...",
    "Открыт": "Open",
    "Закрыт": "Closed",
    "Сохранить": "Save",
    "Удалить": "Delete",
    "Чат": "Chat",
    "Ответить пользователю...": "Reply to user...",
    "Отправить": "Send",
    "Пометить как Решенный (Закрыть)": "Mark as Resolved (Close)",
    "Вы уверены?": "Are you sure?",
    "Да, уверен": "Yes, I am sure",
    "Отмена": "Cancel",
    "Активна": "Active",
    "Нет": "No",
    "Забрать Flora": "Revoke Flora",
    "Выдать Flora": "Grant Flora",
    "Ошибка соединения": "Connection error",
    "Ошибка:": "Error:",
    "Статус обновлен!": "Status updated!",
    "Заполните все поля": "Fill in all fields",
    "Ошибка публикации": "Publication error",
    "Точно удалить новость?": "Are you sure to delete this news?",
    "Закрыть тикет?": "Close ticket?",
    "Удалить тикет?": "Delete ticket?",
    "Нет новостей": "No news",
    "Нет тикетов": "No tickets",
    "Тикет пользователя": "User Ticket"
}

# Function to inject data-i18n into HTML tags
def inject_i18n(html):
    for ru, en in admin_dict.items():
        # Match >Text<
        html = re.sub(r'>\s*' + re.escape(ru) + r'\s*<', f'><span data-i18n="t_admin_{hash(ru)}">{ru}</span><', html)
        # Match placeholders
        html = re.sub(r'placeholder="'+re.escape(ru)+r'"', f'placeholder="{ru}" data-i18n-placeholder="t_admin_{hash(ru)}"', html)
        # Match button text (often innerHTML or inside script)
    return html

admin_html = inject_i18n(admin_html)

# Now for script.js
script_file = 'static/script.js'
with open(script_file, 'r', encoding='utf-8') as f:
    script_js = f.read()

# We need to find strings like showToast('...', ...)
# We will use a regex to find all Russian string literals in JS
ru_strings_in_js = set()
for match in re.finditer(r'[\'"`]([^\'"`]*[А-Яа-яЁё]+[^\'"`]*)[\'"`]', script_js):
    text = match.group(1)
    if not text.startswith('<') and '{' not in text: # ignore HTML templates for now
        ru_strings_in_js.add(text)

js_dict = {}
for text in ru_strings_in_js:
    # simple fallback translation dictionary
    js_dict[text] = text # We'll translate these manually via API or hardcode below if needed

# Let's write the strings to a JSON to translate them
with open('ru_js_strings.json', 'w', encoding='utf-8') as f:
    json.dump(list(ru_strings_in_js), f, ensure_ascii=False, indent=2)

with open(admin_file, 'w', encoding='utf-8') as f:
    f.write(admin_html)

print("Admin HTML injected. Extracted JS strings.")
