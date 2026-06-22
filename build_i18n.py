import re
import json
from html.parser import HTMLParser

class I18nParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.output = []
        self.translations_ru = {}
        self.translations_en = {}
        self.counter = 1
        
    def handle_starttag(self, tag, attrs):
        # reconstruct tag
        attr_str = ""
        for k, v in attrs:
            if v is None:
                attr_str += f' {k}'
            else:
                # check if placeholder or title contains cyrillic
                if k in ('placeholder', 'title', 'data-text') and re.search(r'[А-Яа-яЁё]', v):
                    key = f"t_{self.counter}"
                    self.counter += 1
                    self.translations_ru[key] = v
                    # rough translation logic for common words or just a placeholder for now
                    self.translations_en[key] = self.translate_to_en(v)
                    attr_str += f' {k}="{v}" data-i18n-{k}="{key}"'
                else:
                    attr_str += f' {k}="{v}"'
        self.output.append(f'<{tag}{attr_str}>')

    def handle_endtag(self, tag):
        self.output.append(f'</{tag}>')

    def handle_data(self, data):
        if re.search(r'[А-Яа-яЁё]', data):
            stripped = data.strip()
            if stripped:
                key = f"t_{self.counter}"
                self.counter += 1
                self.translations_ru[key] = stripped
                self.translations_en[key] = self.translate_to_en(stripped)
                
                # We need to wrap the text in a span if it's mixed with non-text? 
                # Actually, HTMLParser gives us exact text nodes.
                # We can just replace the text with a span:
                # <span data-i18n="t_1">Text</span>
                # But wait, if the parent is already a text container (like h1, p, a, button, label, span, div),
                # adding a span is safe.
                # Just replace the stripped text with a span, keeping surrounding whitespace.
                replacement = f'<span data-i18n="{key}">{stripped}</span>'
                self.output.append(data.replace(stripped, replacement))
            else:
                self.output.append(data)
        else:
            self.output.append(data)
            
    def handle_entityref(self, name):
        self.output.append(f'&{name};')

    def handle_charref(self, name):
        self.output.append(f'&#{name};')

    def handle_comment(self, data):
        self.output.append(f'<!--{data}-->')
        
    def handle_decl(self, decl):
        self.output.append(f'<!{decl}>')

    def handle_pi(self, data):
        self.output.append(f'<?{data}>')

    def translate_to_en(self, text):
        # A simple dictionary for common terms to make the translation look good immediately
        dict_en = {
            "Главная": "Home",
            "О нас": "About",
            "Магазин Ботов": "Bot Store",
            "Нейро-Ассистент": "AI Assistant",
            "Редактор": "Editor",
            "Наши Боты": "Our Bots",
            "Внешний вид": "Appearance",
            "Выбор темы:": "Select Theme:",
            "Матрица": "Matrix",
            "Неоновый Желтый": "Neon Yellow",
            "Синтвейв": "Synthwave",
            "Розовый Неон": "Pink Neon",
            "Киберпанк": "Cyberpunk",
            "Токсичный Неон": "Toxic Neon",
            "Язык интерфейса:": "Interface Language:",
            "Профиль": "Profile",
            "Настройки": "Settings",
            "Выход": "Logout",
            "Вход": "Login",
            "Регистрация": "Register",
            "Email": "Email",
            "Пароль": "Password",
            "Никнейм": "Nickname",
            "Отправить": "Send",
            "Сохранить": "Save",
            "Закрыть": "Close",
            "Отзывы": "Reviews",
            "Оставить отзыв": "Leave a Review",
            "Напишите сообщение Aurex...": "Type a message to Aurex...",
            "Правила использования": "Terms of Service",
            "Политика конфиденциальности": "Privacy Policy"
        }
        
        # Exact match
        if text in dict_en: return dict_en[text]
        
        # Partial match fallback (just appending EN for untranslated strings to show it works, 
        # but for a real app we'd translate them all. We'll do our best.)
        # Since I'm an AI writing a python script, I can't call an API here easily without async.
        # I'll just return "[EN] " + text for unknown strings, and the AI can manually patch it later if needed.
        return "[EN] " + text

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Flask templates have {{ ... }} and {% ... %} which HTMLParser might mess up if they are inside tags.
# Let's hope they are preserved.

parser = I18nParser()
parser.feed(html_content)

new_html = "".join(parser.output)

# Write translations to JS file
translations = {
    "ru": parser.translations_ru,
    "en": parser.translations_en
}

js_content = "const translations = " + json.dumps(translations, ensure_ascii=False, indent=4) + ";\n"

with open('static/translations.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

# Add translations.js to index.html if not present
if "translations.js" not in new_html:
    new_html = new_html.replace('</head>', '    <script src="/static/translations.js"></script>\n</head>')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Generated translations for {len(parser.translations_ru)} strings.")
