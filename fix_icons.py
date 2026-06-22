import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix cyrillic matching by using explicit strings
text = re.sub(r'>ГЛАВНАЯ.*?</a>', '><i class="fa-solid fa-house"></i> ГЛАВНАЯ</a>', text, flags=re.IGNORECASE)
text = re.sub(r'>О НАС.*?</a>', '><i class="fa-solid fa-circle-info"></i> О НАС</a>', text, flags=re.IGNORECASE)
text = re.sub(r'>Наши услуги.*?</a>', '><i class="fa-solid fa-tags"></i> НАШИ УСЛУГИ</a>', text, flags=re.IGNORECASE)
text = re.sub(r'>ИИ-ассистент.*?</a>', '><i class="fa-solid fa-robot"></i> ИИ-ассистент</a>', text, flags=re.IGNORECASE)
text = re.sub(r'>Лента.*?</a>', '><i class="fa-solid fa-comment-dots"></i> Лента</a>', text, flags=re.IGNORECASE)
text = re.sub(r'>Редактор.*?</a>', '><i class="fa-solid fa-pen-nib"></i> Редактор</a>', text, flags=re.IGNORECASE)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
