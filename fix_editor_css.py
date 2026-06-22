import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('style="display: none; flex-direction: column;', 'style="flex-direction: column;')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('static/style.css', 'a', encoding='utf-8') as f:
    f.write('\n#view-editor.active { display: flex !important; }\n')

print('Fixed editor CSS visibility')
