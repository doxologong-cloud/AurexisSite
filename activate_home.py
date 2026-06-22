with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = html.replace('<div id="view-home" class="window">', '<div id="view-home" class="window active">')
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Activated view-home')
