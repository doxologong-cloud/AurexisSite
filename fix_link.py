import re
with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('<a class="nav-link" href="#" onclick="switchView(\'view-editor\')">', '<a class="nav-link" href="#editor">')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed link')
